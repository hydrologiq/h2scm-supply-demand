from simulation.query.queries import LogisticQueryResponse
from simulation.logic.rules import FilterRule
from simulation.query.query_input import QueryInput


class VehicleAvailabilityRule(FilterRule):
    def _filter_logistic(
        self, logistic: list[LogisticQueryResponse], query_input: QueryInput
    ) -> list[LogisticQueryResponse]:
        return list(
            filter(
                lambda logistic_value: logistic_value.vehicle.availableQuantity
                >= query_input.required_no_vehicles(),
                logistic,
            )
        )
