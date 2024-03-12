import math
from simulation import SimulationLayer
from simulation.business import BusinessOutput
from simulation.business.inputs.location import Location
from simulation.logic.outputs import Matched
from simulation.logic.outputs.matched import (
    Breakdown,
    BreakdownItem,
    MatchedInstance,
    Production,
    ProductionCapacity,
    ServiceType,
)
from simulation.logic.rules import RuleEngine, Rule
from simulation.logic.rules.filter import (
    VehicleAvailabilityRule,
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
                for storage_rental in data.storageRental:
                    if (
                        len(fuel_match.producer.storedIn) > 0
                        and storage_rental.storage.class_name != "Storage"
                        and storage_rental.storage.class_class_curie
                        not in fuel_match.producer.storedIn
                    ):

                        continue
                    if not meets_service_exclusivity(
                        logistic, fuel_match, storage_rental
                    ):
                        continue

                    cost = calculate_cost_breakdown(
                        logistic=logistic,
                        fuel=fuel_match,
                        storage_rental=storage_rental,
                        total_fuel=business_data.total_fuel(),
                    )

                    CO2e = calculate_co2e_breakdown(
                        logistic=logistic,
                        fuel=fuel_match,
                        total_distance=fuel_distance,
                        total_fuel=business_data.total_fuel(),
                    )

                    matches.append(
                        Matched(
                            MatchedInstance(
                                logistic.service.id,
                                logistic.service.name,
                                logistic.has_exclusive_downstream(),
                                logistic.has_exclusive_upstream(),
                                logistic.instance,
                            ),
                            MatchedInstance(
                                fuel_match.service.id,
                                fuel_match.service.name,
                                fuel_match.has_exclusive_downstream(),
                                fuel_match.has_exclusive_upstream(),
                                fuel_match.instance,
                            ),
                            MatchedInstance(
                                storage_rental.service.id,
                                storage_rental.service.name,
                                storage_rental.has_exclusive_downstream(),
                                storage_rental.has_exclusive_upstream(),
                                storage_rental.instance,
                                storage_rental.storage.class_name,
                            ),
                            cost=cost,
                            production=Production(
                                capacity=ProductionCapacity(
                                    weekly=float(
                                        fuel_match.producer.weeklyProductionCapacity
                                    ),
                                    weeklyUsed=round(
                                        (
                                            business_data.total_fuel()
                                            / float(
                                                fuel_match.producer.weeklyProductionCapacity
                                            )
                                        )
                                        * 100,
                                        2,
                                    ),
                                ),
                                method=fuel_match.producer.class_name,
                                # Only return the first source
                                # TODO(AAS): Support multiple sources
                                source=(
                                    str(fuel_match.producer.source[0])
                                    if (
                                        fuel_match.producer.source is not None
                                        and len(fuel_match.producer.source) > 0
                                    )
                                    else None
                                ),
                                location=Location(
                                    lat=float(fuel_match.dispenser.lat),
                                    long=float(fuel_match.dispenser.long),
                                ),
                            ),
                            transportDistance=fuel_distance,
                            CO2e=CO2e,
                        )
                    )

        return matches


def meets_service_exclusivity(
    logistic: LogisticQueryResponse,
    fuel: FuelQueryResponse,
    storage_rental: StorageQueryResponse,
):
    valid = True
    # Downstream -> fuel -> storage -> logistic
    valid = (
        storage_rental.company.id in fuel.service.exclusiveDownstreamCompanies
        if valid
        and isinstance(fuel.service.exclusiveDownstreamCompanies, list)
        and len(fuel.service.exclusiveDownstreamCompanies) > 0
        else valid
    )
    valid = (
        logistic.company.id in storage_rental.service.exclusiveDownstreamCompanies
        if valid
        and isinstance(storage_rental.service.exclusiveDownstreamCompanies, list)
        and len(storage_rental.service.exclusiveDownstreamCompanies) > 0
        else valid
    )

    # Upstream -> logistic -> storage -> fuel
    valid = (
        fuel.company.id in storage_rental.service.exclusiveUpstreamCompanies
        if valid
        and isinstance(storage_rental.service.exclusiveUpstreamCompanies, list)
        and len(storage_rental.service.exclusiveUpstreamCompanies) > 0
        else valid
    )
    valid = (
        storage_rental.company.id in logistic.service.exclusiveUpstreamCompanies
        if valid
        and isinstance(logistic.service.exclusiveUpstreamCompanies, list)
        and len(logistic.service.exclusiveUpstreamCompanies) > 0
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


def calculate_cost_breakdown(
    logistic: LogisticQueryResponse,
    fuel: FuelQueryResponse,
    storage_rental: StorageQueryResponse,
    total_fuel: int,
) -> Breakdown:
    breakdown = [
        BreakdownItem(
            ServiceType.fuel,
            fuel.service.id,
            total_fuel,
            perUnit=fuel.quote.monetaryValuePerUnit,
            unit=fuel.quote.unit,
            value=fuel.quote.currency,
        ),
        BreakdownItem(
            ServiceType.storageRental,
            storage_rental.service.id,
            math.ceil(total_fuel / float(storage_rental.storage.capacity)),
            perUnit=storage_rental.quote.monetaryValuePerUnit,
            unit=storage_rental.quote.unit,
            value=storage_rental.quote.currency,
        ),
        BreakdownItem(
            ServiceType.logistic,
            logistic.service.id,
            1,
            perUnit=logistic.quote.monetaryValuePerUnit,
            unit=logistic.quote.unit,
            value=logistic.quote.currency,
        ),
    ]
    total = sum(map(lambda item: item.quantity * item.perUnit, breakdown))
    return Breakdown(total, breakdown)


def calculate_co2e_breakdown(
    logistic: LogisticQueryResponse,
    fuel: FuelQueryResponse,
    total_distance: float,
    total_fuel: int,
) -> Breakdown | None:
    if (
        fuel.producer.productionCO2e is not None
        and logistic.service.transportCO2e is not None
    ):
        breakdown = [
            BreakdownItem(
                ServiceType.fuel,
                fuel.service.id,
                total_fuel,
                perUnit=fuel.producer.productionCO2e,
                unit="kg",
                value="kg",
            ),
            BreakdownItem(
                ServiceType.logistic,
                logistic.service.id,
                total_distance,
                perUnit=logistic.service.transportCO2e,
                unit="km",
                value="kg",
            ),
        ]
        total = sum(map(lambda item: item.quantity * item.perUnit, breakdown))
        return Breakdown(total, breakdown)
    else:
        return None
