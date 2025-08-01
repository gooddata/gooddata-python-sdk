# GoodData Foreign Data Wrapper

This project delivers PostgreSQL foreign data wrapper extension built on top of [multicorn](https://multicorn.org/).
The extension makes [GoodData](https://www.gooddata.com/docs/cloud/) insights, computations and ad-hoc report data available in PostgreSQL as tables.
It can be selected like any other table using SQL language.

See [DOCUMENTATION](https://gooddata-fdw.readthedocs.io/en/latest/) for more details.

## Requirements

-  [GoodData](https://www.gooddata.com/docs/cloud/) installation; either running on your cloud
   infrastructure or the free Community Edition running on your workstation

-  Python 3.9 or newer

-  The GoodData Cloud Foreign Data Wrapper is tested with the latest version of multicorn (1.4.0) and PostgreSQL 12

## Installation

Refer to the [documentation](https://gooddata-fdw.readthedocs.io/en/latest/).

## Bugs & Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues) to submit bugs
or request features.

## Changelog

Consult [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for a released versions
and list of changes.

## Limitations

FDW is suitable for small to medium insights results or scheduled reports created in the third party tools. Carefully consider use in a production environment.
