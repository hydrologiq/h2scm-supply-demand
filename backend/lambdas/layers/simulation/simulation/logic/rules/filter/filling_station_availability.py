from simulation.query.queries import (
    FuelQueryResponse,
)
from simulation.logic.rules import FilterRule
from simulation.query.query_input import QueryInput


class FillingStationAvailabilityRule(FilterRule):
    def _filter_fuel(
        self, fuel: list[FuelQueryResponse], query_input: QueryInput
    ) -> list[FuelQueryResponse]:
        return list(
            filter(
                lambda fuel_value: fuel_value.dispenser.fillingStationCapacity
                >= query_input.required_no_vehicles(),
                fuel,
            )
        )
