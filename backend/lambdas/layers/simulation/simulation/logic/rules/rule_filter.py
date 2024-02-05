import copy
from simulation.logic import LogicInput
from simulation.query.queries import (
    LogisticQueryResponse,
    FuelQueryResponse,
    StorageQueryResponse,
)
from simulation.logic.rules import Rule
from simulation.query.query_input import QueryInput


class FilterRule(Rule):
    def apply(self, input: LogicInput, query_input: QueryInput) -> LogicInput:
        input = copy.copy(input)
        input.logistic = self._filter_logistic(input.logistic, query_input)
        input.fuel = self._filter_fuel(input.fuel, query_input)
        input.storageRental = self._filter_storage(input.storageRental, query_input)
        return input

    def _filter_logistic(
        self,
        logistic: list[LogisticQueryResponse],
        query_input: QueryInput,
    ) -> list[LogisticQueryResponse]:
        return logistic

    def _filter_fuel(
        self,
        fuel: list[FuelQueryResponse],
        query_input: QueryInput,
    ) -> list[FuelQueryResponse]:
        return fuel

    def _filter_storage(
        self,
        storage: list[StorageQueryResponse],
        query_input: QueryInput,
    ) -> list[StorageQueryResponse]:
        return storage
