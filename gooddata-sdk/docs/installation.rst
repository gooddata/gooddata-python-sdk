Installation
************

Requirements
=============

- Python 3.7 or newer
- GoodData.CN or GoodData Cloud

Installation
============

Run the following command to install the ``gooddata-sdk`` package on your system:

.. code-block:: shell

    pip install gooddata-sdk

Troubleshooting
===============

* On MacOS, I am getting an error containig following message:

    ``(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)')))``.

    This likely caused by Python and it occurs if you have installed Python installed directly from python.org.
    To mitigate this problem, please install your SSL certificates in *Macintosh HD -> Applications -> Python -> Install Certificates.command**.
