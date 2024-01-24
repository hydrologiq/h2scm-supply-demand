import copy
from api_run_simulation.simulation.logic import LogicInput
from api_run_simulation.simulation.logic.rules import Rule


class RuleEngine:
    rules: list[Rule]

    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def apply(self, input: LogicInput) -> LogicInput:
        input = copy.copy(input)
        for rule in self.rules:
            input = rule.apply(input)
        return input
