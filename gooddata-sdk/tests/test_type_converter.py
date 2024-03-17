# (C) 2021 GoodData Corporation
import datetime
from unittest import mock

import gooddata_sdk.type_converter as conv
import pytest


class TestConverter:
    @mock.patch.object(conv.Converter, "to_type")
    def test_to_external_type(self, to_type_mock):
        test_value = "klikihak"
        to_type_mock.return_value = test_value
        c = conv.Converter()
        c.set_external_fnc(lambda obj, value: f"Test:{str(value)}")

        assert c.to_external_type(test_value) == f"Test:{test_value}"

    def test_subtype_external_type_fnc(self):
        test_value = "123"
        conv.StringConverter.set_external_fnc(lambda obj, value: f"String:{str(value)}")
        conv.IntegerConverter.set_external_fnc(lambda obj, value: f"Integer:{str(value)}")
        sc = conv.StringConverter()
        ic = conv.IntegerConverter()

        assert sc.to_external_type(test_value) == f"String:{str(test_value)}"
        assert ic.to_external_type(test_value) == f"Integer:{str(test_value)}"


class TestStringConverter:
    def test_to_type(self):
        test_value = "klikihak"
        c = conv.StringConverter()
        assert c.to_type(test_value) == test_value


class TestIntegerConverter:
    def test_to_type_ok(self):
        test_value = "123"
        c = conv.IntegerConverter()
        assert c.to_type(test_value) == 123

    def test_to_type_wrong_val(self):
        test_value = "klikihak"
        c = conv.IntegerConverter()
        with pytest.raises(ValueError):
            c.to_type(test_value)


class TestDateConverter:
    def test_to_type_ok(self):
        test_value = "2021"
        c = conv.DateConverter()
        assert c.to_type(test_value) == datetime.date(2021, 1, 1)

    def test_to_type_wrong_val(self):
        test_value = "2021xx"
        c = conv.DateConverter()
        with pytest.raises(ValueError):
            c.to_type(test_value)


class TestDatetimeConverter:
    def test_to_type_ok(self):
        test_value = "2021-10-20 11"
        c = conv.DatetimeConverter()
        assert c.to_type(test_value) == datetime.datetime(2021, 10, 20, 11, 0)

    def test_to_type_wrong_val(self):
        test_value = "2021-10-20"
        c = conv.DatetimeConverter()
        with pytest.raises(ValueError):
            c.to_type(test_value)


class TestTypeConverterRegistry:
    def test_register_default(self):
        dc = conv.StringConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc._register_default(dc)

        assert tc._default_converter == dc

        with pytest.raises(ValueError):
            tc._register_default(conv.IntegerConverter())

    def test_register_with_sub_type(self):
        sub_type = "test_sub_type"
        c = conv.StringConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc._register_with_sub_type(c, sub_type)

        assert sub_type in tc._converters
        assert tc._converters[sub_type] == c

        with pytest.raises(KeyError):
            tc._register_with_sub_type(c, sub_type)

    def test_register(self):
        sub_type = "test_sub_type"
        c = conv.StringConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc.register(c, sub_type)

        assert sub_type in tc._converters
        assert tc._converters[sub_type] == c

        tc.register(c, None)

        assert tc._default_converter == c

    def test_converter_no_setup(self):
        tc = conv.TypeConverterRegistry("dummy")
        with pytest.raises(ValueError):
            tc.converter(None)

        with pytest.raises(ValueError):
            tc.converter("some_sub_type")

    def test_converter_no_def(self):
        sub_type = "test_sub_type"
        c = conv.StringConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc.register(c, sub_type)

        assert tc.converter(sub_type) == c

        with pytest.raises(ValueError):
            tc.converter(None)

        with pytest.raises(ValueError):
            tc.converter("different_sub_type")

    def test_converter_only_def(self):
        c = conv.StringConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc.register(c, None)

        assert tc.converter("some_sub_type") == c
        assert tc.converter(None) == c

    def test_converter_full_reg(self):
        sub_type = "test_sub_type"
        c = conv.StringConverter()
        dc = conv.IntegerConverter()
        tc = conv.TypeConverterRegistry("dummy")
        tc.register(c, sub_type)
        tc.register(dc, None)

        assert tc.converter(sub_type) == c
        assert tc.converter(None) == dc
        assert tc.converter("different_sub_type") == dc


class TestConverterRegistryStore:
    data_type = "DATE"

    @pytest.mark.order(1)
    def test_reset_store(self):
        conv.ConverterRegistryStore._get_registry(self.data_type)
        assert len(conv.ConverterRegistryStore._TYPE_REGISTRIES) > 0

        conv.ConverterRegistryStore.reset()
        assert len(conv.ConverterRegistryStore._TYPE_REGISTRIES) == 0

    @pytest.mark.order(2)
    def test_get_registry(self):
        conv.ConverterRegistryStore._get_registry(self.data_type)

        assert self.data_type in conv.ConverterRegistryStore._TYPE_REGISTRIES
        assert isinstance(conv.ConverterRegistryStore._get_registry(self.data_type), conv.TypeConverterRegistry)

    @pytest.mark.order(3)
    def test_register_and_find(self):
        conv.ConverterRegistryStore.register(self.data_type, conv.DateConverter)
        assert isinstance(conv.ConverterRegistryStore.find_converter(self.data_type), conv.DateConverter)

        sub_type = "TEST"
        conv.ConverterRegistryStore.register(self.data_type, conv.IntegerConverter, [sub_type])
        assert isinstance(conv.ConverterRegistryStore.find_converter(self.data_type, sub_type), conv.IntegerConverter)

    @pytest.mark.order(4)
    def test_find_converter_default(self):
        assert isinstance(conv.ConverterRegistryStore.find_converter("no_type"), conv.StringConverter)

    @pytest.mark.order(5)
    def test_init_store_to_defaults(self):
        conv.ConverterRegistryStore.reset()
        assert len(conv.ConverterRegistryStore._TYPE_REGISTRIES) == 0

    @pytest.mark.order(6)
    def test_sub_stores_namespaces(self):
        assert len(conv.ConverterRegistryStore._TYPE_REGISTRIES) == 0
        assert len(conv.AttributeConverterStore._TYPE_REGISTRIES) > 0
        assert len(conv.DBTypeConverterStore._TYPE_REGISTRIES) > 0

        attr_keys = conv.AttributeConverterStore._TYPE_REGISTRIES.keys()
        db_type_keys = conv.DBTypeConverterStore._TYPE_REGISTRIES.keys()
        assert attr_keys != db_type_keys
