#!/usr/bin/env bash

set -ev

SCRIPT_DIR=`dirname "$0"`
SCRIPT_NAME=`basename "$0"`
SSH_OPTS=-oStrictHostKeyChecking=no

if [[ "$(uname)" == "Darwin" ]]; then
    DOCKER_CMD=docker
else
    DOCKER_CMD="sudo docker"
fi

if [[ -z $($DOCKER_CMD images | grep test-container) ]] ; then
    echo "Building test container"
    docker build -t test-container $SCRIPT_DIR > /dev/null
fi

echo "Testing $1"
CODE_DIR=$(cd $SCRIPT_DIR/..; pwd)
echo "$@"
$DOCKER_CMD run \
	    --rm \
	    --name test \
	    -v /var/run/docker.sock:/var/run/docker.sock \
	    -v $CODE_DIR:$CODE_DIR -w $CODE_DIR \
	    -e COMMIT=$COMMIT \
	    test-container \
	    sh -c "export PYTHONPATH=\$PYTHONPATH:\$PWD/test ; python test/$@"
