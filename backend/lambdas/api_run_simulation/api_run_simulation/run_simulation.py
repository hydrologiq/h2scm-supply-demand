import os
from api_run_simulation.simulation.business import BusinessLayer, BusinessInput
from api_run_simulation.simulation.logic import LogicOutput
from api_run_simulation.simulation.logic import LogicLayer
from api_run_simulation.simulation.query.queries import QueryConfiguration
from api_run_simulation.simulation.query import QueryLayer


def run_simulation(
    input: BusinessInput, query_config: QueryConfiguration
) -> LogicOutput:
    business_output = BusinessLayer().run(input)
    query_output = QueryLayer(query_config).run(business_output)
    return LogicLayer().run(query_output, business_output)


def run_simulation_with_env(input: BusinessInput) -> LogicOutput:
    query_config = QueryConfiguration(
        scm_api_id=os.environ["SCM_API_ID"],
        scm_api_region=os.environ["SCM_API_REGION"],
        scm_api_stage=os.environ["SCM_API_STAGE"],
        scm_repo=os.environ["SCM_REPO"],
        scm_access_token=os.environ["SCM_ACCESS_TOKEN"],
    )
    business_output = BusinessLayer().run(input)
    query_output = QueryLayer(query_config).run(business_output)
    return LogicLayer().run(query_output, business_output)
