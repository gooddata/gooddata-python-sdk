#  (C) 2024 GoodData Corporation
import importlib
from collections.abc import Iterable

import structlog
from gooddata_flight_server import ErrorInfo, ServerContext

from gooddata_flexconnect.function.function import FlexConnectFunction


class FlexConnectFunctionRegistry:
    """
    Registry for supported FlexConnect functions.
    """

    def __init__(self) -> None:
        self._logger = structlog.get_logger("gooddata_flexconnect.registry")
        self._fun_by_name: dict[str, type[FlexConnectFunction]] = {}
        self._fun_names: tuple[str, ...] = ()
        self._loaded_modules: list[str] = []

    @property
    def function_names(self) -> tuple[str, ...]:
        """
        :return: names of available functions
        """
        return self._fun_names

    @property
    def functions(self) -> dict[str, type[FlexConnectFunction]]:
        """
        :return: mapping of fun names to their classes
        """
        return self._fun_by_name.copy()

    @property
    def loaded_modules(self) -> list[str]:
        """
        :return: list of packages from which the registry loaded operations
        """
        return self._loaded_modules

    def _check_function(self, fun: type[FlexConnectFunction]) -> str:
        # TODO: add name validation using regex
        if fun.Name is None or not len(fun.Name):
            raise ValueError(
                f"FlexConnect function implemented in class {fun.__name__} "
                f"does not specify name or specifies an empty name."
            )
        elif fun.Name in self._fun_by_name:
            raise ValueError(
                f"FlexConnect function implemented in class {fun.__name__} specifies same name as "
                f"already registered fun from class {self._fun_by_name[fun.Name].__name__}."
            )

        if fun.Schema is None:
            raise ValueError(
                f"FlexConnect function '{fun.Name}' implemented in class {fun.__name__} does not specify schema."
            )

        return fun.Name

    def _initialize_and_register(self, ctx: ServerContext, fun: type[FlexConnectFunction]) -> None:
        # this should be verified earlier and raise proper error
        assert fun.Name is not None

        fun.on_load(ctx)
        self._fun_by_name[fun.Name] = fun
        self._fun_names = tuple(self._fun_by_name.keys())

    def register(self, ctx: ServerContext, *funs: type[FlexConnectFunction]) -> "FlexConnectFunctionRegistry":
        """
        Register one or more FlexConnect functions.

        :param ctx: server context to pass to the function's on_load
        :param funs: functions to register
        :return:
        """
        for fun in funs:
            self._check_function(fun)
            self._initialize_and_register(ctx, fun)

        return self

    def load(self, ctx: ServerContext, modules: Iterable[str]) -> "FlexConnectFunctionRegistry":
        """
        Loads FlexConnect functions from the provided python packages. The packages must be installed and
        importable.

        :param ctx: server context to pass to the function's on_load
        :param modules: python modules that contain the FlexConnect function implementations
        :return: self, for call chaining sakes
        :raises ModuleNotFoundError: when some package cannot be imported
        """
        for module in modules:
            self._logger.info("load_flexconnect_funs", op_module=module)
            op_module = importlib.import_module(module)
            loaded_funs: list[str] = []

            for member in op_module.__dict__.values():
                if not isinstance(member, type) or not issubclass(member, FlexConnectFunction):
                    # filter out module members which are not classes that implement the
                    # FlexConnectFunction interface
                    continue

                if member == FlexConnectFunction:
                    # the FlexConnectFunction class is likely imported in the module -
                    # don't want that to interfere
                    continue

                # verify the function's metadata (stored in static fields) fulfills the
                # contract in regards
                fun_name = self._check_function(member)

                # trigger function's on-load -> this gives function the opportunity to
                # perform any one-time initialization. if there is a problem during
                # init, the whole load will be interrupted.
                self._initialize_and_register(ctx, member)
                loaded_funs.append(fun_name)

            if not len(loaded_funs):
                # log as warning just so that it stands out somewhat better
                self._logger.warning("load_flexconnect_funs_done", module=module, loaded_funs=[])
            else:
                self._logger.info(
                    "load_flexconnect_funs_done",
                    module=module,
                    loaded_funs=loaded_funs,
                )

            self._loaded_modules.append(module)

        return self

    def create_function(self, name: str) -> FlexConnectFunction:
        """
        Creates a new instance of FlexConnect function with the provided name.
        If there is no function matching the name, this method will raise error containing ErrorInfo.bad_argument.

        :return: an instance of FlexConnect function, ready to be called
        """
        fun = self._fun_by_name.get(name)

        if fun is None:
            raise ErrorInfo.bad_argument(f"Unsupported FlexConnect function '{name}'.")

        return fun.create()
