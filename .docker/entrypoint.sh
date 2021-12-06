#!/bin/bash
set -e
set -x

USER_NAME=tox
GROUP_NAME=tox

# fail if USER_GID or USER_UID is not set
: ${USER_GID:?}
: ${USER_UID:?}

if [ "${USER_UID}" == "0" ]; then
  # execute command as root
  exec "$@"
else
  # create tox user and group
  grep -q ":${USER_GID}:" /etc/group || groupadd -g ${USER_GID} ${GROUP_NAME}
  id -u ${USER_NAME} || useradd -m -u ${USER_UID} -g ${USER_GID} ${USER_NAME}

  # execute command as tox user
  gosu ${USER_NAME} $@
fi
