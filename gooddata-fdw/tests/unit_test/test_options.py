# (C) 2022 GoodData Corporation

import pytest
from gooddata_fdw import options


class DummyOk(options.BaseOptions):
    PUBLIC_CLS_VALUE = 1

    def __init__(self):
        self._dummy = 2
        super().__init__(validate=True, skip_attributes=["wrong", "wrong_params"])

    ###################
    # Validated methods
    def public_no_params(self):
        return self._dummy

    def public_def_params(self, xyz=10):
        return xyz + self.public_no_params()

    @property
    def public_property(self):
        return self._dummy + 100

    ###################
    # Methods excluded from validation by skip_attributes
    def wrong(self):
        raise ValueError()

    def wrong_params(self, x, y):
        raise ValueError()

    ###################
    # Methods ignored by validations
    def _protected(self):
        raise ValueError()

    def _protected_params(self, x, y):
        raise ValueError()

    def __ne__(self, other):
        raise ValueError()


class DummyFailFetch(options.BaseOptions):
    def __init__(self):
        self._dummy = 2
        super().__init__(validate=True)

    ##################
    # Validated method - check on existence of value
    def public_no_params(self):
        raise ValueError()


class DummyFailValue(options.BaseOptions):
    DUMMY = 2

    def __init__(self):
        super().__init__(validate=True)

    ##################
    # Validated method - check on value content
    def public_no_params(self):
        return self.DUMMY

    def _validate_public_no_params(self, value):
        raise ValueError(value)


class TestBaseOptions:
    def test_allowed_options(self):
        # Validations are executed as part of constructor.
        # No exception is raised and options class can be used
        dummy = DummyOk()
        assert dummy.public_no_params() == dummy._dummy

    def test_fail_fetch_value(self):
        with pytest.raises(ValueError):
            DummyFailFetch()

    def test_fail_test_value(self):
        with pytest.raises(ValueError) as exc:
            DummyFailValue()

        assert exc.value.args[0] == DummyFailValue.DUMMY


class TestServerOptions:
    def test_options_with_optional(self):
        config = dict(host="https://abc", token="123", headers_host="abc")
        so = options.ServerOptions(config)

        assert so.host == config["host"]
        assert so.token == config["token"]
        assert so.headers_host == config["headers_host"]

    def test_options_without_optional(self):
        config = dict(host="https://abc", token="123")
        so = options.ServerOptions(config)

        assert so.host == config["host"]
        assert so.token == config["token"]
        assert so.headers_host is None

    @pytest.mark.parametrize(
        "config",
        [
            dict(token="123"),
            dict(host="https://abc"),
        ],
        ids=["no_host", "no_token"],
    )
    def test_options_missing_mandatory(self, config):
        with pytest.raises(ValueError):
            options.ServerOptions(config)

    def test_options_invalid_host(self):
        config = dict(host="xyz://abc", token="123")
        with pytest.raises(ValueError):
            options.ServerOptions(config)


class TestTableOptions:
    def test_options_with_optional(self):
        config = dict(workspace="ws", insight="123", compute="abc")
        to = options.TableOptions(config)

        assert to.workspace == config["workspace"]
        assert to.insight == config["insight"]
        assert to.compute == config["compute"]

    def test_options_without_optional(self):
        config = dict(workspace="ws")
        to = options.TableOptions(config)

        assert to.workspace == config["workspace"]
        assert to.insight is None
        assert to.compute is None


class TestImportSchemaOptions:
    def test_options_with_optional(self):
        config = dict(object_type="all", numeric_max_size="123")
        iso = options.ImportSchemaOptions(config)
        default_digits_after = options.ImportSchemaOptions.METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT

        assert iso.object_type == config["object_type"]
        assert iso.numeric_max_size == config["numeric_max_size"]
        assert iso.metric_data_type() == f"DECIMAL({config['numeric_max_size']}, {default_digits_after})"

    def test_options_without_optional(self):
        config = dict(object_type="insights")
        iso = options.ImportSchemaOptions(config)
        default_digits_before = options.ImportSchemaOptions.METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT
        default_digits_after = options.ImportSchemaOptions.METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT

        assert iso.object_type == config["object_type"]
        assert iso.numeric_max_size == default_digits_before
        assert iso.metric_data_type() == f"DECIMAL({default_digits_before}, {default_digits_after})"

    def test_options_invalid_object_type(self):
        config = dict(object_type="invalid")
        with pytest.raises(ValueError):
            options.ImportSchemaOptions(config)
