#!/bin/bash

rm -rf dist_layers
mkdir dist_layers

DIST_DIR=$(pwd)/dist_layers
CWD=$(pwd)

for d in ../layers/*/ ; do
    cd $CWD
    FILE_NAME=$(echo "$d" | sed -r 's/[./]|layers+//g')
    DIST_FILE_PATH=$DIST_DIR/$FILE_NAME
    DIST_PYTHON_TMP=$DIST_FILE_PATH/tmp
    DIST_PYTHON_OUT=$DIST_FILE_PATH/python
    mkdir $DIST_FILE_PATH
    mkdir $DIST_PYTHON_OUT
    rm -rf .venv
    python -m venv .venv
    source .venv/bin/activate
    cd $d
    rm -rf dist
    

    [[ -f "./pre-build.sh" ]] && . ./pre-build.sh

    poetry build    
    poetry run pip install --upgrade -t $DIST_PYTHON_TMP dist/*.whl
    cd $DIST_PYTHON_TMP
    rsync -av --progress . /$DIST_PYTHON_OUT --exclude __pycache__ --exclude dist
    cd $DIST_FILE_PATH
    rm -rf $DIST_PYTHON_TMP

    find . -exec touch -d "2023-06-01T09:00:00" {} +
    zip -rq -D -X -9 -A --compression-method deflate ../$FILE_NAME.zip . -x '*.pyc'
    touch -d "2023-06-01T09:00:00" ../$FILE_NAME.zip
done
