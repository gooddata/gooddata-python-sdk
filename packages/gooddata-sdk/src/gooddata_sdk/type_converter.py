# (C) 2021 GoodData Corporation
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Callable, Optional

from dateutil.parser import parse


class Converter:
    """
    Base Converter class. It defines Converter API and implements support for external type conversion.
    External type conversion provides ability to plug-in conversion function to Converter
    """

    DEFAULT_DB_DATA_TYPE = "VARCHAR(255)"

    _EXTERNAL_CONVERSION_FNC: Optional[Callable[[object, Any], Any]] = None

    @classmethod
    def set_external_fnc(cls, fnc: Callable[[object, Any], Any]) -> None:
        cls._EXTERNAL_CONVERSION_FNC = fnc

    def to_type(self, value: str) -> Any:
        raise NotImplementedError

    def to_external_type(self, value: str) -> Any:
        typed_value = self.to_type(value)
        if self._EXTERNAL_CONVERSION_FNC:
            return self._EXTERNAL_CONVERSION_FNC(typed_value)  # type: ignore
        else:
            return typed_value

    def db_data_type(self) -> str:
        raise NotImplementedError


class StringConverter(Converter):
    # noinspection PyMethodMayBeStatic
    def to_type(self, value: str) -> str:
        return value

    def db_data_type(self) -> str:
        return self.DEFAULT_DB_DATA_TYPE


class IntegerConverter(Converter):
    # noinspection PyMethodMayBeStatic
    def to_type(self, value: str) -> int:
        return int(value)

    def db_data_type(self) -> str:
        return "INTEGER"


class DateConverter(Converter):
    def to_type(self, value: str) -> date:
        return self.to_date(value)

    def db_data_type(self) -> str:
        return "DATE"

    @staticmethod
    def _to_components(value: str) -> list[int]:
        """Add first month and first date to incomplete iso date string.

        >>> assert DateConverter._to_components("2021-01") == [2021, 1, 1]
        >>> assert DateConverter._to_components("1992") == [1992, 1, 1]
        """
        parts = value.split("-")
        int_parts = list(map(int, parts))
        missing_count = 3 - len(int_parts)
        int_parts.extend([1] * missing_count)
        return int_parts

    @classmethod
    def to_date(cls, value: str) -> date:
        """Add first month and first date to incomplete iso date string.

        >>> assert DateConverter.to_date("2021-01") == date(2021, 1, 1)
        >>> assert DateConverter.to_date("1992") == date(1992, 1, 1)
        """
        return date(*cls._to_components(value))


class DatetimeConverter(Converter):
    def to_type(self, value: str) -> datetime:
        return self.to_datetime(value)

    def db_data_type(self) -> str:
        return "TIMESTAMP"

    @classmethod
    def to_datetime(cls, value: str) -> datetime:
        """Append minutes to incomplete datetime string.

        >>> from datetime import datetime
        >>> assert DatetimeConverter.to_datetime("2021-01-01 02") == datetime(2021, 1, 1, 2, 0)
        >>> assert DatetimeConverter.to_datetime("2021-01-01 12:34") == datetime(2021, 1, 1, 12, 34)
        """
        return parse(cls._sanitize_timestamp(value))

    @staticmethod
    def _sanitize_timestamp(value: str) -> str:
        """Append minutes to incomplete datetime string.

        >>>assert DatetimeConverter._sanitize_timestamp("2021-01-01 02") == "2021-01-01 02:00"
        >>>assert DatetimeConverter._sanitize_timestamp("2021-01-01 12:34") == "2021-01-01 12:34"
        """
        parts = value.split(":")
        if len(parts) == 1:
            value = value + ":00"
        return value


class TypeConverterRegistry:
    """
    Class stores converters for given type with ability to distinguish converters based on sub-type granularity.
    """

    def __init__(self, type_name: str):
        """
        Initialize instance with type for which instance is going to be responsible

        :param type_name: type name
        """
        self._type_name = type_name
        self._converters: dict[str, Converter] = {}
        self._default_converter: Optional[Converter] = None

    def register(self, converter: Converter, sub_type: Optional[str]) -> None:
        """
        Register converter instance for given sub-type (granularity). If sub-type is not specified, converter is
        registered as the default one for the whole type. Default converter can be registered only once.

        Args:
            converter: converter instance
            sub_type: sub-type name
        """
        if sub_type is None:
            self._register_default(converter)
        else:
            self._register_with_sub_type(converter, sub_type)

    def _register_with_sub_type(self, converter: Converter, sub_type: str) -> None:
        """
        Register converter instance for given sub-type granularity.

        Args:
            converter: converter instance
            sub_type: sub-type name
        """
        if sub_type in self._converters:
            reg_converter_type = self._converters[sub_type].__class__.__name__
            new_converter_type = converter.__class__.__name__
            raise KeyError(
                f"{new_converter_type} registration failed for {self._type_name} with "
                f"sub_type {sub_type} - already registered as {reg_converter_type}"
            )
        self._converters[sub_type] = converter

    def _register_default(self, converter: Converter) -> None:
        """
        Register default converter instance for the type. Default type can be registered only once.

        :param converter: converter instance
        """
        if self._default_converter:
            reg_converter_type = self._default_converter.__class__.__name__
            new_converter_type = converter.__class__.__name__
            raise ValueError(
                f"Default converter {new_converter_type} registration failed for {self._type_name} - "
                f"already registered as {reg_converter_type}"
            )
        self._default_converter = converter

    def converter(self, sub_type: Optional[str]) -> Converter:
        """
        Find and return converter instance for a given sub-type. Default converter instance is returned
        if the sub-type is not found or not provided. When a default converter is not registered, ValueError
        exception is raised.

        Args:
            sub_type: sub-type name

        Returns:
            Converter instance
        """
        if sub_type is None:
            return self._get_default_converter()

        try:
            return self._converters[sub_type]
        except KeyError:
            return self._get_default_converter()

    def _get_default_converter(self) -> Converter:
        """
        Check if default converter is registered. If yes, return it. Otherwise raise ValueError exception.

        :return: default Converter instance
        """
        if not self._default_converter:
            raise ValueError(f"Default converter not registered for type {self._type_name}")
        return self._default_converter


class ConverterRegistryStore:
    """
    Class store TypeConverterRegistry instances for each registered type. It provides interface to register converters
    with type and sub-type and to find converter.
    The class is not meant to be used directly but as base class for child classes
    """

    _TYPE_REGISTRIES: dict[str, TypeConverterRegistry] = {}
    _DEFAULT_CONVERTOR: Converter = StringConverter()

    @classmethod
    def _get_registry(cls, type_name: str) -> TypeConverterRegistry:
        """
        Return TypeConverterRegistry instance registered for given type. If no such instance exists, it is created.

        :param type_name: type name
        :return: TypeConverterRegistry instance for given type name
        """
        try:
            return cls._TYPE_REGISTRIES[type_name]
        except KeyError:
            cls._TYPE_REGISTRIES[type_name] = TypeConverterRegistry(type_name)
            return cls._TYPE_REGISTRIES[type_name]

    @classmethod
    def register(cls, type_name: str, class_converter: type[Converter], sub_types: Optional[list[str]] = None) -> None:
        """
        Register Converter instance created from provided Converter class to given type and list of sub types.
        When sub types are not provided, converter is registered as the default one for given type.

        :param type_name: type name
        :param class_converter: Converter class
        :param sub_types: list of sub types or None (default type Converter)
        """
        registry = cls._get_registry(type_name)
        if sub_types is None:
            registry.register(class_converter(), None)
        else:
            for sub_type in sub_types:
                registry.register(class_converter(), sub_type)

    @classmethod
    def find_converter(cls, type_name: str, sub_type: Optional[str] = None) -> Converter:
        """
        Find Converter for given type and sub type.

        :param type_name: type name
        :param sub_type: sub type name
        """
        try:
            registry = cls._TYPE_REGISTRIES[type_name]
        except KeyError:
            return cls._DEFAULT_CONVERTOR

        return registry.converter(sub_type)

    @classmethod
    def reset(cls) -> None:
        """
        Reset converters setup
        """
        cls._TYPE_REGISTRIES = {}


class AttributeConverterStore(ConverterRegistryStore):
    """
    Store for conversion of attributes
    """

    _TYPE_REGISTRIES: dict[str, TypeConverterRegistry] = {}
    _DEFAULT_CONVERTOR: Converter = StringConverter()


class DBTypeConverterStore(ConverterRegistryStore):
    """
    Store for conversion of database types
    """

    _TYPE_REGISTRIES: dict[str, TypeConverterRegistry] = {}
    _DEFAULT_CONVERTOR: Converter = StringConverter()


def build_stores() -> None:
    """
    Initialize both AttributeConverterStore and DBTypeConverterStore with Convertors.
    """
    AttributeConverterStore.register("NORMAL", StringConverter)
    AttributeConverterStore.register("DATE", IntegerConverter)
    AttributeConverterStore.register("DATE", StringConverter, ["WEEK", "QUARTER"])
    AttributeConverterStore.register("DATE", DateConverter, ["DAY", "MONTH", "YEAR"])
    AttributeConverterStore.register("DATE", DatetimeConverter, ["MINUTE", "HOUR"])

    DBTypeConverterStore.register("date", DateConverter)
    DBTypeConverterStore.register("timestamp", DatetimeConverter)
    DBTypeConverterStore.register("timestamp without time zone", DatetimeConverter)


# Initialize store hardcoded for now as it seems to be enough
build_stores()
