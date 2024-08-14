#  (C) 2024 GoodData Corporation
import abc
from typing import Optional

import pyarrow

from gooddata_flight_server.server.base import ServerContext
from gooddata_flight_server.tasks.base import ArrowData


class FlexFun(abc.ABC):
    """
    Interface for pluggable functions which can generate flights based on a
    set of parameters sent by the GoodData Cloud and its FlexQuery.

    The generator functions have semantics similar to table functions
    known from databases:

    - a full schema of the result and all it's columns must be known up-front

    - the function may return only subset of columns if the caller only
      asks for certain columns

      NOTE: this is only about trimming columns - the result cardinality is
      the same just that some columns are not returned.

    Programming detail: a new instance of the FlexFun will be created
    for every call using the `create` method.

    TODO: rename the class... i'm not very creative right now
    """

    Name: Optional[str] = None
    """
    Function MUST define a unique name
    """

    Schema: Optional[pyarrow.Schema] = None
    """
    Function MUST define schema describing its data.
    """

    Metadata: Optional[dict] = None
    """
    Function MAY provide additional metadata about themselves. These then
    influence how the FlexFun is used by and called from GoodData Cloud & FlexQuery.
    """

    @classmethod
    def create(cls) -> "FlexFun":
        """
        This method is called by FlexFun server in order to create a new instance
        of FlexFun which should be used to service the call.

        If your FlexFun implementation has default constructor with no parameters or
        variable parameters, then you do not have to implement this method.

        Overriding this method is typically needed when the instance of FlexFun needs
        to receive dependencies created during the one-off initialization done in
        `on_load`.

        IMPORTANT: this method should be fast and non-blocking. It needs to avoid any
        expensive initialization and any one-off initialization. One-off initialization
        should be done in `on_load` method; all expensive operations should be done
        within the `call` itself.

        :return: an instance of concrete FlexFun
        """
        return cls()

    @abc.abstractmethod
    def call(
        self,
        parameters: dict,
        columns: Optional[tuple[str, ...]],
        headers: dict[str, list[str]],
    ) -> ArrowData:
        """
        Function call.

        :param parameters: parameters sent from the GoodData Cloud / FlexQuery.
        :param columns: hints which columns SHOULD be returned; the FlexFun may decide to ignore
         this and always return all columns. The extraneous columns will be trimmed when received
         by FlexQuery.
        :param headers: Flight RPC headers
        :return: result of the call
        """
        raise NotImplementedError

    def cancel(self) -> bool:
        """
        A FlexFun call may be cancelled by the server. It usually happens when the call takes
        a long time to complete and the GoodData Cloud and its FlexQuery are no longer
        interested in the result.

        Implementing the cancellation is optional. If not implemented, the FlexFun server will
        still pretend the entire call was cancelled - it's just that it will wait for the `call`
        to finish and then throw the results away.

        :return: True if the call was cancelled, False otherwise.
        """
        return False

    @staticmethod
    def on_load(ctx: ServerContext) -> None:
        """
        This method is called by FlexFun server at the time it discovers this FlexFun and
        wants to load it and prepare it for calls.

        This method is called exactly once for each discovered FlexFun; it is guaranteed that this
        method will be called before first call to this FlexFun. If this method raises an error,
        it will interrupt the server startup.

        The intention of this method is to allow FlexFun perform one-off initialization of
        some shared, reusable internals (usually some singletons).

        A very typical use of this method is to inspect the `settings` included in the context -
        this contains the settings loaded from config files/env variables provided to the server
        at startup. If the FlexFun needs some external (custom) settings, the user can code
        those into config files or env variables -> this method can act on them.

        :param ctx: context of the server which hosts this FlexFun
        :return: nothing
        """
        return
