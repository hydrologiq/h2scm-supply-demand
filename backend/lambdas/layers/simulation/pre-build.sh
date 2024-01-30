#!/usr/bin/env bash

set -e

#
# Source: https://gist.github.com/maxim/6e15aa45ba010ab030c4
# gh-dl-release! It works!
# 
# This script downloads an asset from latest or specific Github release of a
# private repo. Feel free to extract more of the variables into command line
# parameters.
#
# PREREQUISITES
#
# curl, jq
#
# USAGE
#
# Set all the variables but the personal token inside the script, make sure you chmod +x it.
# 
#  GITHUB_PERSONAL_TOKEN - is an environment variable
#
# If your version/tag doesn't match, the script will exit with error.
H2SCM_VERSION="v3.0.0"

TOKEN=$GITHUB_PERSONAL_TOKEN
REPO="hydrologiq/h2scm-ontology"
FILE="ontology.zip"
VERSION=$H2SCM_VERSION
GITHUB="https://api.github.com"

alias errcho='>&2 echo'

function gh_curl() {
  curl -H "Authorization: token $TOKEN" \
       -H "Accept: application/vnd.github.v3.raw" \
       $@
}


if [ "$VERSION" = "latest" ]; then
  # Github should return the latest release first.
  parser=".[0].assets | map(select(.name == \"$FILE\"))[0].id"
else
  parser=". | map(select(.tag_name == \"$VERSION\"))[0].assets | map(select(.name == \"$FILE\"))[0].id"
fi;

asset_id=`gh_curl -s $GITHUB/repos/$REPO/releases | jq "$parser"`
if [ "$asset_id" = "null" ]; then
  errcho "ERROR: version not found $VERSION"
  exit 1
fi;

curl -sL --header "Authorization: token $TOKEN" --header 'Accept: application/octet-stream' \
  https://api.github.com/repos/$REPO/releases/assets/$asset_id \
  -o $FILE

mkdir ontology
unzip ontology -d ontology
cp ontology/hydrogen_nrmm_optional.py simulation/query/queries/.
rm -rf ontology
rm ontology.zip