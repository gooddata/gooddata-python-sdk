---
title: "Installation"
linkTitle: "Installation"
weight: 11
---

Before installing, ensure you are using Python `3.7` or newer.

To install the `gooddata-sdk` Python SDK package, run the following command:

```bash
pip install gooddata-sdk
```

### Requirements

* Python `3.7` or newer.
* GoodData.CN or GoodData Cloud


{{% alert color="warning" title="Known MacOS issue" %}}
If you are getting the following message:

__(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE\_VERIFY\_FAILED] certificate verify failed: unable to get local issuer certificate (\_ssl.c:1129)')))__

it is likely caused by Python and it occurs if you have installed Python directly from python.org.

To mitigate, please istall your SSL certificates in __HD -> Applications -> Python -> Install Certificates.command__.
{{% /alert %}}

To make use of the package, you need a running instance of GoodData. If you do not have GoodData yet, sign up for a [trial of GoodData Cloud](https://www.gooddata.com/trial/).

### Versioning

The Python SDK is versioned. The version you should be using depends on the type of GoodData distribution you are using.

#### GoodData Cloud

We recommend you always work with the newest (supported) Python available.

#### GoodData.CN & GoodData.CN Community Edition

Check the [release notes](https://github.com/gooddata/gooddata-python-sdk/releases) to see what version of Python SDK is supported in the version of GoodData.CN you are using.
