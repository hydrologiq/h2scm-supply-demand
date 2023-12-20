from simulation.business import BusinessLayer, BusinessInput
from simulation.logic import LogicOutput
from simulation.logic import LogicLayer
from simulation.query.queries import QueryConfiguration
from simulation.query import QueryLayer


def run_simulation(
    input: BusinessInput, query_config: QueryConfiguration
) -> LogicOutput:
    business_output = BusinessLayer().run(input)
    query_output = QueryLayer(query_config).run(business_output)
    return LogicLayer().run(query_output, business_output)
