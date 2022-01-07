# (C) 2021 GoodData Corporation
FROM harbor.intgdc.com/tools/gdc-fossa-cli:c505bd0

RUN set -x \
    && yum update -y \
    && yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget make unzip \
    && yum clean all

RUN set -x \
  && wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz \
  && tar xzf Python-3.9.9.tgz \
  && cd Python-3.9.9 \
  && ./configure --enable-optimizations \
  && make altinstall \
  && rm -rf Python-3.9.9 Python-3.9.9.tgz \
  && python3.9 --version \
  && pip3.9 --version

USER fossa
ENV PATH /home/fossa/.local/bin:$PATH

RUN set -x \
  && sed -i'.bck' -e '1s|#!/usr/bin/env python3.6|#!/usr/bin/env python3.9|' $TOOL_DIR/fossa_scanning_tool \
  && pip3.9 install -r $TOOL_DIR/requirements.txt --user

USER root

# labels
LABEL image_name="GoodData FOSSA-CLI for gooddata-python-sdk"
LABEL maintainer="Tiger team <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk"
LABEL parent_image="harbor.intgdc.com/tools/gdc-fossa-cli:14be5ff"
