---
title: "Installation"
linkTitle: "Installation"
weight: 11
---

Before installing, ensure you are using:

* Python `3.7` or newer
* [GoodData.CN](https://www.gooddata.com/developers/cloud-native/doc/cloud/deploy-and-install/cloud-native/) or [GoodData Cloud](https://www.gooddata.com/developers/cloud-native/doc/cloud/deploy-and-install/cloud/)
* The [pip](https://pypi.org/project/pip/) package management tool



To install the `gooddata-sdk` Python SDK package, run the following command:

```bash
pip3 install gooddata-sdk
```

{{% alert color="warning" title="Known MacOS issue" %}}
If you are getting the following message:

__(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE\_VERIFY\_FAILED] certificate verify failed: unable to get local issuer certificate (\_ssl.c:1129)')))__

it is likely caused by Python and it occurs if you have installed Python directly from python.org.

To mitigate, please install your SSL certificates in __HD -> Applications -> Python -> Install Certificates.command__.
{{% /alert %}}

To make use of the package, you need a running instance of GoodData. If you do not have GoodData yet, sign up for a [trial of GoodData Cloud](https://www.gooddata.com/trial/).

### Versioning

The Python SDK is versioned. The version you should be using depends on the type of GoodData distribution you are using.

#### GoodData Cloud

We recommend you always work with the newest (supported) Python available.

#### GoodData.CN

Here is a mapping table of compatibility, which version of Python SDK to use with each version of GoodData.CN

| Gooddata.CN | Python SDK  |
|---|---|
| v2.5 | v1.5 |
| v2.4 | v1.4 |
| v2.3 | v1.3 |
