Installation
************

You can build and run it as a service in your Docker environment (recommended) or install the package on your system directly using pip.

Requirements
=============

-  Python 3.7 or newer
-  GoodData.CN installation; either running on your cloud infrastructure or the free Community Edition running on your workstation

Install Using Docker (Recommended)
==================================

The GoodData.CN distribution comes with a Dockerfile which, when started, will run PostgreSQL 12 with multicorn
and ``gooddata-fdw`` pre-installed. For an even better user experience there is a ``docker-compose.yaml`` file which contains 
both the ``gooddata-fdw`` and ``gooddata-cn-ce`` services.

Build and Run the Service
^^^^^^^^^^^^^^^^^^^^^^^^^

Execute the following command in your repository root folder:

.. code-block:: shell

   docker-compose up -d

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

Install Using Pip
=================

Run the following command to install the ``gooddata-fdw`` package on your system:

.. code-block:: shell

    pip install gooddata-fdw