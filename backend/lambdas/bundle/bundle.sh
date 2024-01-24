#!/bin/bash

rm -rf dist
mkdir dist

DIST_DIR=$(pwd)/dist
CWD=$(pwd)

for d in ../*/ ; do
    cd $CWD
    [[ "$d" == *"bundle"* || "$d" == *"layers"* ]] && continue
    FILE_NAME=$(echo "$d" | sed -r 's/[./]+//g')
    DIST_FILE_PATH=$DIST_DIR/$FILE_NAME
    cd $d
    rm -rf dist
    [[ -f "./pre-build.sh" ]] && . ./pre-build.sh
    poetry build
    poetry run pip install --upgrade -t $DIST_FILE_PATH dist/*.whl
    cd $DIST_FILE_PATH
    find . -exec touch -d "2023-06-01T09:00:00" {} +
    zip -rq -D -X -9 -A --compression-method deflate ../$FILE_NAME.zip . -x '*.pyc'
    touch -d "2023-06-01T09:00:00" ../$FILE_NAME.zip
done