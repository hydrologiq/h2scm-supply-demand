from simulation import SimulationLayer
from simulation.business import BusinessOutput
from simulation.logic.outputs import Matched
from simulation.logic.outputs.matched import MatchedStorage
from simulation.logic.rules import RuleEngine, Rule
from simulation.logic.rules.filter import (
    FillingStationAvailabilityRule,
    VehicleAvailabilityRule,
    StorageAvailabilityRule,
)
from simulation.query.queries import (
    FuelQueryResponse,
)
from simulation.logic import (
    LogicInput,
    LogicOutput,
)
from geopy.distance import distance


class LogicLayer(SimulationLayer):
    rules: list[Rule] = [
        FillingStationAvailabilityRule(),
        VehicleAvailabilityRule(),
        StorageAvailabilityRule(),
    ]

    def run(self, data: LogicInput, business_data: BusinessOutput) -> LogicOutput:
        data = self.__apply_rules(data, business_data)
        matches = self.__match(data, business_data)
        return LogicOutput(**{**data.__dict__, "matches": matches})

    def __apply_rules(
        self, data: LogicInput, business_data: BusinessOutput
    ) -> LogicInput:
        engine = RuleEngine(self.rules, business_data)
        return engine.apply(data)

    def __match(self, data: LogicInput, business_data: BusinessOutput) -> list[Matched]:
        matches: list[Matched] = []
        for logistic in data.logistic:
            fuel_matches: list[FuelQueryResponse] = []
            fuel_distances: list[float] = []
            for fuel in data.fuel:
                fuel_distance = round(
                    distance(
                        (fuel.dispenser.lat, fuel.dispenser.long),
                        (
                            business_data.project.location.lat,
                            business_data.project.location.long,
                        ),
                    ).km
                    * 2,
                    2,
                )
                if fuel_distance <= logistic.vehicle.transportDistance:
                    fuel_matches.append(fuel)
                    fuel_distances.append(fuel_distance)
            if len(fuel_matches) > 0:
                fuel_match = fuel_matches[0]
                fuel_distance = fuel_distances[0]
                fuelUtilisation = round(
                    (
                        business_data.total_fuel()
                        / float(fuel_match.producer.dailyOfftakeCapacity)
                    )
                    * 100,
                    2,
                )
                CO2e = (
                    round(
                        (
                            business_data.total_fuel()
                            * float(fuel.producer.productionCO2e)
                        )
                        + fuel_distance * float(logistic.service.transportCO2e),
                        2,
                    )
                    if (
                        fuel.producer.productionCO2e is not None
                        and logistic.service.transportCO2e is not None
                    )
                    else None
                )
                for storage_rental in data.storageRental:
                    price = round(
                        (float(logistic.quote.monetaryValue))
                        + (
                            float(fuel_match.quote.monetaryValue)
                            * business_data.total_fuel()
                        )
                        + float(storage_rental.quote.monetaryValue),
                        2,
                    )

                    matches.append(
                        Matched(
                            logistic.service.id,
                            fuel_matches[0].service.id,
                            fuelUtilisation,
                            price,
                            fuel_distance,
                            MatchedStorage(
                                storage_rental.service.id, business_data.fuel[0].type
                            ),
                            CO2e,
                        )
                    )
                    break
        return matches
