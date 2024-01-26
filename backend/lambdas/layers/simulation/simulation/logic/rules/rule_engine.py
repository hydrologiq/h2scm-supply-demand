import copy
from simulation.logic import LogicInput
from simulation.logic.rules import Rule
from simulation.query.query_input import QueryInput


class RuleEngine:
    rules: list[Rule]
    query_input: QueryInput

    def __init__(self, rules: list[Rule], query_input: QueryInput):
        self.rules = rules
        self.query_input = query_input

    def apply(self, input: LogicInput) -> LogicInput:
        input = copy.deepcopy(input)
        for rule in self.rules:
            input = rule.apply(input, self.query_input)
        return input
