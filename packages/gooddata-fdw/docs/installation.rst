Installation
************

You can build and run it as a service in your Docker environment (recommended) or install the package on your system directly using pip.

Requirements
=============

- Python 3.7 or newer
- GoodData.CN or GoodData Cloud

Install Using Docker (Recommended)
==================================

The Python SDK comes with a Dockerfile which, when started, will run PostgreSQL 12 with multicorn
and ``gooddata-fdw`` pre-installed. For an even better user experience there is a ``docker-compose.yaml`` file which contains
both the ``gooddata-fdw`` and ``gooddata-cn-ce`` services.

Build and Run the Service
^^^^^^^^^^^^^^^^^^^^^^^^^

Execute the following command in your repository root folder:

.. code-block:: shell

   docker-compose up --build -d

``gooddata-fdw`` image is built from the Dockerfile and both services are started in background.

.. note::
   Services in docker-compose.yaml contain a setup of various environment variables including ``POSTGRES_PASSWORD``.
   Feel free to set the variables in your environment, before you execute the above command.
   Default value for ``POSTGRES_PASSWORD`` is ``gooddata123``.

Maintenance
^^^^^^^^^^^

To rebuild the Foreign Data Wrapper image execute the following command:

.. code-block:: shell

   docker-compose build

If you would like to purge a container completely (including the volume) and start from scratch, run the following helper scripts:

.. code-block:: shell

   ./rebuild.sh gooddata-cn-ce
   ./rebuild.sh gooddata-fdw

Adding Your Own Data
^^^^^^^^^^^^^^^^^^^^

Before you start playing with the Foreign Data Wrapper, you will need a content in the ``gooddata-cn-ce``.

``docker-compose.yaml`` launches the `upload-layout` service. Its purpose is to bootstrap the demo and testing content
into gooddata-cn-ce. You can use this as a starting point.

But the ``gooddata-cn-ce`` service is not limited only to the demo content. You can fill the ``gooddata-cn-ce`` with your own
content (LDM, metrics, insights). Follow
our `Getting Started documentation <https://www.gooddata.com/developers/cloud-native/doc/1.6/getting-started/>`_ if you
need help with that.

Connect with existing GoddData.CN installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This use case is for users running a GoodData.CN image who want to connect it to the GoodData Foreign Data Wrapper. For connecting ``gooddata-fdw`` with GoodData.CN image both images have to run on the same network. You can create a new network and run both images there or use the default bridge network.

.. note::

   Default network bridge does not support accessing services by their name. You need to use an IP address in the host when defining the GoodData.CN server. The IP address can be found using command ``docker inspect <GoodData.CN container name>``.

1. Build the ``gooddata-fdw`` service from ``docker-compose.yaml``:

   .. code-block:: shell

      docker-compose build gooddata-fdw

2. Create a new network:

   .. code-block:: shell

      docker network create --driver bridge gd-cn-net

3. Run GoodData.CN on created network and name it ``gooddata-cn-ce``:

   .. code-block:: shell

      docker run --rm --name gooddata-cn-ce -p 3000:3000 -p 5432:5432 -v /data \
      --network gd-cn-net \
      -e LICENSE_AND_PRIVACY_POLICY_ACCEPTED=YES \
      -e APP_LOGLEVEL=INFO \
      gooddata/gooddata-cn-ce:latest

4. Run the ``gooddata-fdw`` service on created network and name it ``postgres-fdw``:

   .. code-block:: shell

      docker run --rm --name postgres-fdw -p 2543:5432 --network gd-cn-net \
      -e POSTGRES_DB=gooddata -e POSTGRES_USER=gooddata -e POSTGRES_PASSWORD=gooddata123 \
      gooddata-python-sdk_gooddata-fdw:latest \
      postgres -c "shared_preload_libraries=foreign_table_exposer" -c "log_statement=all" -c "client_min_messages=DEBUG1" -c "log_min_messages=DEBUG1"


Install Using Pip
=================

Run the following command to install the ``gooddata-fdw`` package on your system:

.. code-block:: shell

    pip install gooddata-fdw

.. warning::

    For this use case, you also need to install and run PostgreSQL together with multicorn.
