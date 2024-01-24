import copy
from api_run_simulation.simulation.logic import LogicInput
from api_run_simulation.simulation.query.queries import (
    LogisticQueryResponse,
    FuelQueryResponse,
)
from api_run_simulation.simulation.logic.rules import Rule


class FilterRule(Rule):
    def apply(self, input: LogicInput) -> LogicInput:
        input = copy.copy(input)
        input.logistic = self._filter_logistic(input.logistic)
        input.fuel = self._filter_fuel(input.fuel)
        return input

    def _filter_logistic(
        self, logistic: list[LogisticQueryResponse]
    ) -> list[LogisticQueryResponse]:
        return logistic

    def _filter_fuel(self, fuel: list[FuelQueryResponse]) -> list[FuelQueryResponse]:
        return fuel
