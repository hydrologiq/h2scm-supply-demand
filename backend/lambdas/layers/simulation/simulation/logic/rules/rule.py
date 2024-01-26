from simulation.query import QueryInput
from simulation.logic import LogicInput


class Rule:
    _query_input: QueryInput

    def __init__(self, query_input: QueryInput):
        self._query_input = query_input

    def apply(input: LogicInput) -> LogicInput:
        pass
