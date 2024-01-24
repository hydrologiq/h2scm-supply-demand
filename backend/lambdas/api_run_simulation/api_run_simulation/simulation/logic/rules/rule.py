from api_run_simulation.simulation.query import QueryInput
from api_run_simulation.simulation.logic import LogicInput


class Rule:
    _query_input: QueryInput

    def __init__(self, query_input: QueryInput):
        self._query_input = query_input

    def apply(input: LogicInput) -> LogicInput:
        pass
