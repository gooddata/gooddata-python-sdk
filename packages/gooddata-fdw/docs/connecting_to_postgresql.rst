Get Started With PostgreSQL
***************************

Connect to PostgreSQL
=====================

After the ``gooddata-fdw`` container starts, you can connect to the running PostgreSQL:

-   From console using ``psql --host localhost --port 2543 --user gooddata gooddata``

    You will be asked to enter the password that you have specified when starting the script.

-   From any other client using JDBC string: ``jdbc:postgresql://localhost:2543/gooddata``

    You will be asked to enter username (gooddata) and password.

Once connected you will be able to work with the GoodData.CN Foreign Data Wrapper.
At first, you need to define your GoodData.CN server in PostgreSQL:

.. code-block:: postgresql

   CREATE SERVER multicorn_gooddata FOREIGN DATA WRAPPER multicorn
   OPTIONS (
       wrapper 'gooddata_fdw.GoodDataForeignDataWrapper',
       host 'https://gooddata-cn-ce:3000', -- host equal to name of container with GoodData.CN.CE
       token 'YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz' -- default gooddata-cn-ce token, documented in public DOC as well
   );

As of now the GoodData.CN community edition (single container deployment) supports only ``localhost`` as the target host.
If you spin-up GoodData.CN and FDW using docker-compose, GoodData.CN host name is the service name in the docker-compose, e.g. ``gooddata-cn-ce``.
To enable such setup, we provide an option ``header_host``:

.. code-block:: postgresql

   CREATE SERVER multicorn_gooddata FOREIGN DATA WRAPPER multicorn
     OPTIONS (
       wrapper 'gooddata_fdw.GoodDataForeignDataWrapper',
       host 'http://gooddata-cn-ce:3000', -- host equal to name of container with GoodData.CN.CE
       token 'YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz', -- default gooddata-cn-ce token, documented in public DOC as well
       headers_host 'localhost'
     );

Typically, you have to do this once per GoodData.CN installation. You may add as many servers as you need.

**IMPORTANT**: Do not forget to specify host including the schema (http or https).
