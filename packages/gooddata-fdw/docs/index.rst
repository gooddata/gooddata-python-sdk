GoodData Foreign Data Wrapper Documentation
*******************************************

GoodData Foreign Data Wrapper delivers PostgreSQL foreign data wrapper extension built on top of `multicorn <https://multicorn.org/>`_.
The extension makes GoodData.CN insights, computations and ad-hoc report data available in PostgreSQL as tables.
It can be selected like any other table using the SQL language.

Limitations
===========
FDW is suitable for small to medium insights results or scheduled reports created in the third party tools. Carefully consider use in a production environment.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   connecting_to_postgresql
   foreign_tables
   api
