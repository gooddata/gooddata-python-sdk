---
title: "Installation"
linkTitle: "Installation"
weight: 11
---

Before installing, ensure you are using:

* Python `3.9` or newer
* [GoodData.CN](https://www.gooddata.com/docs/cloud-native/latest/install/) or [GoodData Cloud](https://www.gooddata.com/docs/cloud/getting-started/)
* The [pip](https://pypi.org/project/pip/) package management tool



To install the `gooddata-sdk` Python SDK package, run the following command:

```bash
pip3 install gooddata-sdk
```

{{% alert color="warning" title="Known macOS issue" %}}
If you are getting the following message:

__(Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE\_VERIFY\_FAILED] certificate verify failed: unable to get local issuer certificate (\_ssl.c:1129)')))__

it is likely caused by Python, and it occurs if you have installed Python directly from python.org.

To mitigate, please install your SSL certificates in __HD -> Applications -> Python -> Install Certificates.command__.
{{% /alert %}}

To make use of the package, you need a running instance of GoodData. If you do not have GoodData yet, sign up for a [trial of GoodData Cloud](https://www.gooddata.com/trial/).

### Versioning

The Python SDK is versioned and usually released in tandem with GoodData Cloud.

#### GoodData Cloud

When working with GoodData Cloud, we recommend you always work with the newest Python SDK available.

### Troubleshooting

In case of any issues with Python SDK, feel free to reach out to us on our [community slack](https://www.gooddata.com/slack/) or create a [GitHub issue](https://github.com/gooddata/gooddata-python-sdk/issues).
