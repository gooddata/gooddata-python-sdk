# (C) 2022 GoodData Corporation
from __future__ import annotations

import time

import urllib3.exceptions as urllib3_ex
from gooddata_api_client import exceptions

from gooddata_sdk.client import GoodDataApiClient


class SupportService:
    def __init__(self, api_client: GoodDataApiClient) -> None:
        self._entities_api = api_client.entities_api

    @property
    def is_available(self) -> bool:
        """
        Checks if the GoodData instance is available.
        Can raise exceptions in case of authentication or authorization failure.

        :return: True - available, False - not available
        """
        try:
            self._entities_api.get_all_options()
            return True
        except (exceptions.ForbiddenException, exceptions.UnauthorizedException):
            # do not consider invalid credentials or missing rights "not available" state
            raise
        except exceptions.ApiException:
            # invalid response from GoodData - GoodData is still booting but endpoint is receiving connections already
            return False
        except urllib3_ex.MaxRetryError:
            # endpoint inactive - cannot connect
            return False

    def wait_till_available(self, timeout: int, sleep_time: float = 2.0) -> None:
        """
        Wait till GoodData service is available. When timeout is:

          - > 0 exception is raised after given number of seconds.
          - = 0 exception is raised whe service is not available immediately
          - < 0 no timeout

        Method propagates is_available exceptions.

        Args:
            timeout: seconds to wait to service to be available (see method description for details)
            sleep_time: seconds to wait between availability tests
        """
        start_time_sec = time.time()
        while True:
            if self.is_available:
                return

            if timeout < 0:
                time.sleep(sleep_time)
            else:
                to_timeout_sec = timeout - (time.time() - start_time_sec)
                # to_timeout_sec is a float number which can be close to zero but not zero because float cannot
                # represent some numbers exactly. This way, sleep method does not have to wait ridiculously small
                # timespan
                if to_timeout_sec < 0.0001:
                    raise TimeoutError(f"Timeout after {timeout} seconds waiting")

                if to_timeout_sec < sleep_time:
                    time.sleep(to_timeout_sec)
                else:
                    time.sleep(sleep_time)
