from simulation import SimulationLayer
from simulation.business import BusinessOutput
from simulation.logic.outputs import Matched
from simulation.logic.outputs.matched import MatchedStorage
from simulation.logic.rules import RuleEngine, Rule
from simulation.logic.rules.filter import (
    VehicleAvailabilityRule,
    StorageAvailabilityRule,
)
from simulation.query.queries import (
    FuelQueryResponse,
    LogisticQueryResponse,
    StorageQueryResponse,
)
from simulation.logic import (
    LogicInput,
    LogicOutput,
)
from geopy.distance import distance


class LogicLayer(SimulationLayer):
    rules: list[Rule] = [
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
            fuel_matches = match_fuel(
                data, business_data, logistic.vehicle.transportDistance
            )
            for fuel_match, fuel_distance in fuel_matches:
                fuelUtilisation = round(
                    (
                        business_data.total_fuel()
                        / float(fuel_match.producer.dailyOfftakeCapacity)
                    )
                    * 100,
                    2,
                )
                for storage_rental in data.storageRental:
                    if not meets_service_exclusivity(
                        logistic, fuel_match, storage_rental
                    ):
                        break
                    price = round(
                        (float(logistic.quote.monetaryValue))
                        + (
                            float(fuel_match.quote.monetaryValue)
                            * business_data.total_fuel()
                        )
                        + float(storage_rental.quote.monetaryValue),
                        2,
                    )
                    CO2e = (
                        round(
                            (
                                business_data.total_fuel()
                                * float(fuel_match.producer.productionCO2e)
                            )
                            + fuel_distance * float(logistic.service.transportCO2e),
                            2,
                        )
                        if (
                            fuel_match.producer.productionCO2e is not None
                            and logistic.service.transportCO2e is not None
                        )
                        else None
                    )
                    matches.append(
                        Matched(
                            logistic.service.id,
                            fuel_match.service.id,
                            fuelUtilisation,
                            price,
                            fuel_distance,
                            MatchedStorage(
                                storage_rental.service.id, business_data.fuel[0].type
                            ),
                            CO2e,
                        )
                    )

        return matches


def meets_service_exclusivity(
    logistic: LogisticQueryResponse,
    fuel: FuelQueryResponse,
    storage_rental: StorageQueryResponse,
):
    valid = True
    # Downstream -> logistic -> fuel -> storage
    valid = (
        fuel.service.id in logistic.service.exclusiveDownstreamCompanies
        if valid and isinstance(logistic.service.exclusiveDownstreamCompanies, list)
        else valid
    )
    valid = (
        storage_rental.service.id in fuel.service.exclusiveDownstreamCompanies
        if valid and isinstance(fuel.service.exclusiveDownstreamCompanies, list)
        else valid
    )

    return valid


def match_fuel(
    data: LogicInput, business_data: BusinessOutput, transportDistance: float
):
    fuel_matches: list[tuple[FuelQueryResponse, float]] = []
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
        if fuel_distance <= transportDistance:
            fuel_matches.append((fuel, fuel_distance))
    return fuel_matches
