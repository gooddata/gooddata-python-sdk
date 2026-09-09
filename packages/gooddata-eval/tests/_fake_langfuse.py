# (C) 2026 GoodData Corporation
"""In-process fake Langfuse HTTP server: a pytest fixture and a runnable wire-watching script.

A `threading.Thread`-hosted `http.server` answering the Langfuse v4 endpoints the package
uses, plus the three legacy ones, with canned/synthesised data recorded on `requests`.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import signal
import sys
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit

_DATASET_ITEMS_PATH = "/api/public/dataset-items"
_OBSERVATIONS_PATH = "/api/public/v2/observations"
_OTLP_PATH = "/api/public/otel/v1/traces"
_SCORES_PATH = "/api/public/scores"
_TRACES_PATH = "/api/public/traces"
_INGESTION_PATH = "/api/public/ingestion"
_DATASET_RUN_ITEMS_PATH = "/api/public/dataset-run-items"

_ROOT_LATENCY_SECONDS = 12.5
_CHILD_COSTS = (0.01, 0.02)


def _short_hash(value: str, length: int) -> str:
    return hashlib.md5(value.encode()).hexdigest()[:length]


def observation_rows(session_id: str) -> list[dict]:
    """A gen-ai-shaped root row plus two child rows for one conversation session."""
    trace_id = _short_hash(session_id, 32)
    root_id = _short_hash(f"{session_id}:root", 16)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    times = {"startTime": start.isoformat(), "endTime": (start + timedelta(seconds=_ROOT_LATENCY_SECONDS)).isoformat()}
    shared = {"traceId": trace_id, "type": "GENERATION", "sessionId": session_id, **times}
    root = {
        "id": root_id,
        "name": "conversation.send_message",
        "parentObservationId": None,
        "isRootObservation": True,
        "latency": _ROOT_LATENCY_SECONDS,
        "totalCost": None,
        "metadata": {"conversation_id": session_id},
        **shared,
    }
    children = [
        {
            "id": _short_hash(f"{session_id}:child{i}", 16),
            "name": f"model.call.{i}",
            "parentObservationId": root_id,
            "isRootObservation": False,
            "latency": None,
            "totalCost": cost,
            "metadata": {},
            **shared,
        }
        for i, cost in enumerate(_CHILD_COSTS, start=1)
    ]
    return [root, *children]


def _canned_item(item_id: str, dataset_name: str) -> dict:
    return {
        "id": item_id,
        "datasetName": dataset_name,
        "input": {"question": f"Canned question for {item_id}"},
        "expectedOutput": f"Rubric: the answer for {item_id} must directly address the question.",
        "metadata": {},
    }


class FakeLangfuse:
    """A fake Langfuse server on `127.0.0.1:0`, configurable per test before each request."""

    def __init__(self, *, port: int = 0, verbose: bool = False) -> None:
        self.dataset_name = "fake"
        self.dataset_id = "ds-fake"
        self.items: list[dict] = []
        self.missing: set[str] = set()
        self.first_observations_call_empty = False
        self.observations_pages = 1
        self.otlp_status = 200
        self.otlp_body: dict = {}
        self.scores_429_once = False
        self.ingestion_body: dict = {"successes": [], "errors": []}
        self.verbose = verbose
        self.requests: list[dict] = []
        self.on_request = None
        handler = self._make_handler()
        self._httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
        self._thread = Thread(target=self._httpd.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()

    def __enter__(self) -> FakeLangfuse:
        self.start()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.stop()

    def calls(self, method: str, path_prefix: str) -> list[dict]:
        return [r for r in self.requests if r["method"] == method and r["path"].startswith(path_prefix)]

    def _make_handler(self) -> type[BaseHTTPRequestHandler]:
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                if server.verbose:
                    super().log_message(format, *args)

            def do_GET(self) -> None:
                server._handle(self, "GET")

            def do_POST(self) -> None:
                server._handle(self, "POST")

        return Handler

    def _handle(self, handler: BaseHTTPRequestHandler, method: str) -> None:
        try:
            self._route(handler, method)
        except Exception as exc:  # never let a bad request kill the server thread
            self._respond(handler, 400, {"message": f"fake_langfuse error: {exc}"})

    def _route(self, handler: BaseHTTPRequestHandler, method: str) -> None:
        parts = urlsplit(handler.path)
        path = parts.path
        query = {k: v[0] for k, v in parse_qs(parts.query).items()}
        body = self._read_json_body(handler)
        record = {
            "method": method,
            "path": path,
            "query": query,
            "headers": {k.lower(): v for k, v in handler.headers.items()},
            "json": body,
        }
        self.requests.append(record)
        if self.on_request is not None:
            self.on_request(record)

        if method == "GET" and path == _DATASET_ITEMS_PATH:
            self._get_dataset_items(handler, query)
        elif method == "GET" and path.startswith(f"{_DATASET_ITEMS_PATH}/"):
            self._get_dataset_item(handler, path.rsplit("/", 1)[-1])
        elif method == "GET" and path == _OBSERVATIONS_PATH:
            self._get_observations(handler, query)
        elif method == "POST" and path == _OTLP_PATH:
            self._respond(handler, self.otlp_status, self.otlp_body)
        elif method == "POST" and path == _SCORES_PATH:
            self._post_scores(handler)
        elif method == "GET" and path == _TRACES_PATH:
            self._get_traces(handler, query)
        elif method == "POST" and path == _INGESTION_PATH:
            self._respond(handler, 200, self.ingestion_body)
        elif method == "POST" and path == _DATASET_RUN_ITEMS_PATH:
            self._respond(handler, 200, {})
        else:
            self._respond(handler, 404, {"message": f"fake_langfuse: no route for {method} {path}"})

    @staticmethod
    def _read_json_body(handler: BaseHTTPRequestHandler) -> dict | None:
        length = int(handler.headers.get("Content-Length") or 0)
        if not length:
            return None
        raw = handler.rfile.read(length)
        return json.loads(raw) if raw else None

    def _get_dataset_items(self, handler: BaseHTTPRequestHandler, query: dict) -> None:
        if query.get("datasetName") != self.dataset_name:
            self._respond(handler, 404, {"message": "Dataset not found"})
            return
        meta = {"page": 1, "limit": 100, "totalItems": len(self.items), "totalPages": 1}
        self._respond(handler, 200, {"data": self.items, "meta": meta})

    def _get_dataset_item(self, handler: BaseHTTPRequestHandler, item_id: str) -> None:
        if item_id in self.missing:
            self._respond(handler, 404, {"message": "Dataset item not found"})
            return
        self._respond(handler, 200, {"id": item_id, "datasetId": self.dataset_id, "datasetName": self.dataset_name})

    def _post_scores(self, handler: BaseHTTPRequestHandler) -> None:
        if self.scores_429_once:
            self.scores_429_once = False
            self._respond(handler, 429, {"message": "rate limited"}, headers={"Retry-After": "0"})
            return
        self._respond(handler, 200, {})

    def _get_observations(self, handler: BaseHTTPRequestHandler, query: dict) -> None:
        session_id = query.get("sessionId", "")
        if self.first_observations_call_empty:
            self.first_observations_call_empty = False
            self._respond(handler, 200, {"data": [], "meta": {}})
            return
        rows = observation_rows(session_id)
        if self.observations_pages == 2 and query.get("cursor") is None:
            self._respond(handler, 200, {"data": rows[:1], "meta": {"cursor": "page-2"}})
            return
        if self.observations_pages == 2:
            self._respond(handler, 200, {"data": rows[1:], "meta": {}})
            return
        self._respond(handler, 200, {"data": rows, "meta": {}})

    def _get_traces(self, handler: BaseHTTPRequestHandler, query: dict) -> None:
        session_id = query.get("sessionId", "")
        legacy_trace = {
            "id": _short_hash(session_id, 32),
            "sessionId": session_id,
            "latency": _ROOT_LATENCY_SECONDS,
            "totalCost": sum(_CHILD_COSTS),
            "metadata": {"conversation_id": session_id},
        }
        self._respond(handler, 200, {"data": [legacy_trace]})

    def _respond(
        self, handler: BaseHTTPRequestHandler, status: int, body: dict, *, headers: dict | None = None
    ) -> None:
        payload = json.dumps(body).encode()
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(payload)))
        for key, value in (headers or {}).items():
            handler.send_header(key, value)
        handler.end_headers()
        handler.wfile.write(payload)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a fake Langfuse server and watch the wire.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--dataset", default="fake")
    parser.add_argument("--items", nargs="*", default=[])
    parser.add_argument("--record", type=Path, default=None, help="Directory to write each request body to.")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def _make_recorder(record_dir: Path):
    record_dir.mkdir(parents=True, exist_ok=True)
    numbers = itertools.count(1)

    def _record(record: dict) -> None:
        safe_path = record["path"].replace("/", "_")
        out = record_dir / f"{next(numbers):03d}-{record['method']}-{safe_path}.json"
        out.write_text(json.dumps(record.get("json"), indent=2, default=str))

    return _record


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    server = FakeLangfuse(port=args.port, verbose=args.verbose)
    server.dataset_name = args.dataset
    server.items = [_canned_item(item_id, args.dataset) for item_id in args.items]

    recorder = _make_recorder(args.record) if args.record else None

    def _on_request(record: dict) -> None:
        print(json.dumps(record, indent=2, default=str))
        if recorder is not None:
            recorder(record)

    server.on_request = _on_request
    with server:
        print(f"fake Langfuse server listening on {server.base_url}", file=sys.stderr)
        try:
            signal.pause()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
