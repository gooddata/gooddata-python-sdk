# GoodData FlexConnect

GoodData FlexConnect allows you to build your own data source for GoodData Cloud or Cloud Native.

FlexConnect works with a concept similar to 'table functions' that you may already know
from database technologies.

-  To build your own data source, you implement one or more FlexConnect functions. The
   functions compute and return tabular data - how they do it is completely up to you.
-  The functions are hosted and invoked inside a FlexConnect server (which is included in this package).
-  A running FlexConnect server can be added as a data source to your GoodData Cloud or GoodData Cloud Native.
-  The functions available on FlexConnect server will be mapped to data sets within GoodData's Semantic Model
   and from then on can be used during report computation.


## Getting Started using the FlexConnect

The easiest and recommended way to get started with FlexConnect is to use [the template repository](https://github.com/gooddata/gooddata-flexconnect-template).

The template repository is set up with project infrastructure and boilerplate related to testing, packaging and
running your FlexConnect functions. You can start building your own data source in under a minute.

The template also comes with extensive documentation which will guide you through all important steps and facets
of building production-ready FlexConnect functions.

If you are eager to get started, here is a short snippet to bootstrap a new FlexConnect project:

```shell
git clone https://github.com/gooddata/gooddata-flexconnect-template.git my-flexconnect
cd my-flexconnect
rm -rf .git && git init && git add . && git commit -m "Initial commit"
```
