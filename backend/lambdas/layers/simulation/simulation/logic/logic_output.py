from simulation.query import QueryOutput
from dataclasses import dataclass

from simulation.logic.outputs import Matched


@dataclass
class LogicOutput(QueryOutput):
    matches: list[Matched]

    def post_clean(self, cleaned, just_matches: bool = False) -> dict:
        if not just_matches:
            if "fuel" not in cleaned:
                cleaned["fuel"] = []
            if "logistic" not in cleaned:
                cleaned["logistic"] = []
            if "storageRental" not in cleaned:
                cleaned["storageRental"] = []
        if "matches" not in cleaned:
            cleaned["matches"] = []
        return cleaned
