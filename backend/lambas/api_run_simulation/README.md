# Setup

In order to build this API there is a dependency on a version of the ontology (currently v2.1.0).

## Ontology dependency

To retrieve this dependency we require the use of a github person access token which is exported as an environment variable or in a .env file. This token needs read access for the `Content` permission within the `hydrologiq/h2scm-ontology` repository.

Once the above token is set, you will need to run the `pre-build.sh` script which will download the release set within the script and copy the relevant files (`hydrogen_nrmm_optional.py`) to the source for this API.
