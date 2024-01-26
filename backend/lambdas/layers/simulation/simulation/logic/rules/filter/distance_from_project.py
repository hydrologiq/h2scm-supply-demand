from simulation.query.queries import LogisticQueryResponse
from simulation.logic.rules import FilterRule
from simulation.query.query_input import QueryInput


class DistanceFromProjectRule(FilterRule):
    def _filter_logistic(
        self, logistic: list[LogisticQueryResponse], query_input: QueryInput
    ) -> list[LogisticQueryResponse]:
        return list(
            filter(
                lambda logistic_value: logistic_value.projectDistance
                <= logistic_value.vehicle.transportDistance,
                logistic,
            )
        )
