from api_run_simulation.simulation.query.queries import LogisticQueryResponse
from api_run_simulation.simulation.logic.rules import FilterRule


class DistanceFromProjectRule(FilterRule):
    def _filter_logistic(
        self, logistic: list[LogisticQueryResponse]
    ) -> list[LogisticQueryResponse]:
        return list(
            filter(
                lambda logistic_value: logistic_value["projectDistance"]
                <= logistic_value["vehicle"]["transportDistance"],
                logistic,
            )
        )
