from simulation.query.queries import FuelQueryResponse, LogisticQueryResponse
from simulation.logic.rules import FilterRule


class FillingStationAvailabilityRule(FilterRule):
    def _filter_fuel(self, fuel: list[FuelQueryResponse]) -> list[FuelQueryResponse]:
        return list(
            filter(
                lambda fuel_value: fuel_value["dispenser"]["fillingStationCapacity"]
                >= self._query_input.required_no_vehicles(),
                fuel,
            )
        )
