# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional, Union


class BaseOptions:
    def __init__(self, validate: bool = True, skip_attributes: Optional[list[str]] = None) -> None:
        if skip_attributes is None:
            self._skip_attributes = []
        else:
            self._skip_attributes = skip_attributes

        if validate:
            self._validate_options()

    def _no_mandatory_value_msg(self, attribute: str) -> str:
        return f"'{self.__class__.__name__}' mandatory key '{attribute}' is not defined"

    def _list_public_attributes(self) -> list[str]:
        # find object's public attributes without magic methods
        return [attr for attr in dir(self.__class__) if not attr.startswith("_") and attr not in self._skip_attributes]

    def _attribute_value(self, attribute: str) -> Any:
        try:
            attribute_value = getattr(self, attribute)
            if callable(attribute_value):
                # if it is callable, it is an option getter which must be able to call without parameters
                attribute_value = attribute_value()
            return attribute_value
        except Exception:
            raise ValueError(self._no_mandatory_value_msg(attribute))

    def _validate_options(self) -> None:
        for attr in self._list_public_attributes():
            attribute_value = self._attribute_value(attr)

            # try to find optional private validation method and use it
            try:
                validation_func = getattr(self, f"_validate_{attr}")
                if callable(validation_func):
                    validation_func(attribute_value)
            except AttributeError:
                pass

    def __repr__(self) -> str:
        attr_to_value = {attr: self._attribute_value(attr) for attr in self._list_public_attributes()}
        return f"{self.__class__.__name__}({str(attr_to_value)})"


class ServerOptions(BaseOptions):
    def __init__(self, options: dict[str, str]) -> None:
        self._options = options
        super().__init__()

    def _no_mandatory_value_msg(self, attribute: str) -> str:
        return f"FOREIGN SERVER mandatory option '{attribute}' is not defined"

    @property
    def host(self) -> str:
        return self._options["host"]

    @staticmethod
    def _validate_host(value: str) -> None:
        if not value.startswith("https://") and not value.startswith("http://"):
            raise ValueError(
                f"FOREIGN SERVER 'host' option must start with 'https://' or 'http://'. Instead got '{value}'"
            )

    @property
    def token(self) -> str:
        return self._options["token"]

    @property
    def headers_host(self) -> Union[str, None]:
        return self._options.get("headers_host")


class TableOptions(BaseOptions):
    def __init__(self, options: dict[str, str]) -> None:
        self._options = options
        super().__init__()

    def _no_mandatory_value_msg(self, attribute: str) -> str:
        return f"FOREIGN TABLE mandatory option '{attribute}' is not defined"

    @property
    def workspace(self) -> str:
        return self._options["workspace"]

    @property
    def insight(self) -> Union[str, None]:
        return self._options.get("insight")

    @property
    def compute(self) -> Union[str, None]:
        return self._options.get("compute")


class ImportSchemaOptions(BaseOptions):
    METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT = "18"
    METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT = "2"

    def __init__(self, options: dict[str, str]) -> None:
        self._options = options
        super().__init__()

    def _no_mandatory_value_msg(self, attribute: str) -> str:
        return f"IMPORT SCHEMA mandatory mandatory option '{attribute}' is not defined"

    @property
    def object_type(self) -> str:
        return self._options["object_type"]

    @staticmethod
    def _validate_object_type(value: str) -> None:
        if value not in ["insights", "compute", "all"]:
            raise ValueError(
                f"IMPORT SCHEMA option 'object_type' contains unsupported value '{value}'. "
                f"Supported values are: 'insights', 'compute', 'all'"
            )

    @property
    def numeric_max_size(self) -> str:
        return self._options.get("numeric_max_size", self.METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT)

    def metric_data_type(self, precision: Optional[str] = None) -> str:
        digits_after = precision if precision else self.METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT
        return f"DECIMAL({self.numeric_max_size}, {digits_after})"
