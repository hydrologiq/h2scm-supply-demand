from simulation.query.queries import StorageQueryResponse
from simulation.logic.rules import FilterRule
from simulation.query.query_input import QueryInput


class StorageAvailabilityRule(FilterRule):
    def _filter_storage(
        self, storage: list[StorageQueryResponse], query_input: QueryInput
    ) -> list[StorageQueryResponse]:
        return list(
            filter(
                lambda storage_value: storage_value.storage.availableQuantity
                * storage_value.storage.capacity
                >= query_input.total_fuel(),
                storage,
            )
        )
