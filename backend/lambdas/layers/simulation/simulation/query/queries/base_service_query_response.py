from simulation.query.queries.hydrogen_nrmm_optional import Service
from simulation.simulation_data import BaseQueryResponse


class BaseServiceQueryResponse(BaseQueryResponse):
    service: Service

    def has_exclusive_upstream(self):
        return len(self.service.exclusiveUpstreamCompanies) > 0

    def has_exclusive_downstream(self):
        return len(self.service.exclusiveDownstreamCompanies) > 0
