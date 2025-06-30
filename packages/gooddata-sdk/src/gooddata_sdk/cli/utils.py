# (C) 2024 GoodData Corporation
import time
from functools import wraps
from typing import Any

_SUPPORTED = ("data_sources", "user_groups", "users", "workspaces_data_filters", "workspaces")


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def measure_clone(step: str) -> Any:
    def decorate(func: Any) -> Any:
        @wraps(func)
        def timeit_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f"Clone '{step}' finished. It took {total_time:.4f} seconds")
            return result

        return timeit_wrapper

    return decorate


def measure_deploy(step: str) -> Any:
    def decorate(func: Any) -> Any:
        @wraps(func)
        def timeit_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f"Deploy '{step}' finished. It took {total_time:.4f} seconds")
            return result

        return timeit_wrapper

    return decorate
