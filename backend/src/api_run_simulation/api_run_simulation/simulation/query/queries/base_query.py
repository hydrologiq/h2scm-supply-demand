import requests
from simulation.query.queries import QueryConfiguration
from simulation.query.queries.base_response import BaseQueryResponse
from simulation.query.queries.hydrogen_nrmm_optional import YAMLRoot


class BaseQuery:
    config: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.config = config

    def query(self) -> BaseQueryResponse:
        response = requests.post(
            f"https://{self.config.scm_api_id}.execute-api.{self.config.scm_api_region}.amazonaws.com/{self.config.scm_api_stage}/repositories/{self.config.scm_repo}/query/select",
            self._get_query(),
            headers={
                "Authorization": f"Bearer {self.config.scm_access_token}",
            },
        )
        return self._parse_query(response.json())

    def _parse_query(self, resp_obj) -> BaseQueryResponse:
        pass

    def _get_matching_instances(self, bindings, class_types: dict) -> list[dict]:
        return [
            self._get_matching_instance(binding, class_types) for binding in bindings
        ]

    def _get_matching_instance(self, binding, prefixes: list[str]) -> dict:
        raw_instances = {}
        for item_name in binding:
            class_keys = list(filter(lambda key: item_name.startswith(key), prefixes))
            if isinstance(item_name, str) and len(class_keys) == 1:
                class_key = class_keys[0]
                if class_key not in raw_instances:
                    raw_instances[class_key] = {}
                item = binding[item_name]
                item_value = item["value"]
                if item["type"] == "uri":
                    raw_instances[class_key]["id"] = item_value.replace(
                        "https://w3id.org/hydrologiq/hydrogen/nrmm", "hydrogen_nrmm:"
                    )
                else:
                    attribute_name = item_name.replace(class_key, "")
                    if len(attribute_name) > 0:
                        attribute_name = attribute_name[0].lower() + attribute_name[1:]
                        raw_instances[class_key][attribute_name] = item_value
                    else:
                        raw_instances[class_key] = item_value

        return raw_instances

    def _get_query(self) -> str:
        pass
