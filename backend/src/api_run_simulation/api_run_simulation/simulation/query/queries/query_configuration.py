from dataclasses import dataclass


@dataclass
class QueryConfiguration:
    scm_api_id: str
    scm_api_region: str
    scm_api_stage: str
    scm_repo: str
    scm_access_token: str
