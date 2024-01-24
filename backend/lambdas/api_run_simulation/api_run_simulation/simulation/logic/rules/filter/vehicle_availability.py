from api_run_simulation.simulation.query.queries import LogisticQueryResponse
from api_run_simulation.simulation.logic.rules import FilterRule


class VehicleAvailabilityRule(FilterRule):
    def _filter_logistic(
        self, logistic: list[LogisticQueryResponse]
    ) -> list[LogisticQueryResponse]:
        return list(
            filter(
                lambda logistic_value: logistic_value["vehicle"]["availableQuantity"]
                >= self._query_input.required_no_vehicles(),
                logistic,
            )
        )
