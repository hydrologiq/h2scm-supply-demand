from simulation import SimulationLayer
from simulation.business import BusinessOutput
from simulation.logic.outputs import Matched
from simulation.logic.rules import RuleEngine, Rule
from simulation.query.queries import (
    FuelQueryResponse,
    LogisticQueryResponse,
)
from simulation.logic import (
    LogicInput,
    LogicOutput,
)
from geopy.distance import distance


class LogicLayer(SimulationLayer):
    rules: list[Rule] = []

    def run(self, data: LogicInput, business_data: BusinessOutput) -> LogicOutput:
        data = self.__apply_rules(data)
        matches = self.__match(data, business_data)
        return LogicOutput(**{**data.__dict__, "matches": matches})

    def __apply_rules(self, data: LogicInput) -> LogicInput:
        engine = RuleEngine(self.rules)
        return engine.apply(data)

    def __match(self, data: LogicInput, business_data: BusinessOutput) -> list[Matched]:
        matches: list[Matched] = []
        for logistic in data.logistic:
            fuel_matches: list[FuelQueryResponse] = []
            for fuel in data.fuel:
                if (
                    distance(
                        (logistic.distro.lat, logistic.distro.long),
                        (fuel.dispenser.lat, fuel.dispenser.long),
                    ).miles
                    <= logistic.vehicle.transportDistance
                ):
                    fuel_matches.append(fuel)
            if len(fuel_matches) > 0:
                fuel_match = fuel_matches[0]
                redundancy = round(
                    (
                        float(fuel_match.producer.dailyOfftakeCapacity)
                        / business_data.total_fuel()
                        - 1
                    )
                    * 100,
                    2,
                )
                matches.append(
                    Matched(
                        logistic.service.id,
                        fuel_matches[0].service.id,
                        redundancy,
                    )
                )
        return matches
