from decimal import Decimal
import requests
from simulation import BaseQueryResponse
import simulation
from simulation.query.queries import (
    QueryConfiguration,
    BaseQueryInput,
)
from simulation.query.queries.hydrogen_nrmm_optional import YAMLRoot


class BaseQuery:
    config: QueryConfiguration

    def __init__(self, config: QueryConfiguration):
        self.config = config

    def query(
        self, config: BaseQueryInput | None = None, graphs: list[str] = ["default"]
    ) -> list[BaseQueryResponse]:
        response = requests.post(
            f"https://{self.config.scm_api_id}.execute-api.{self.config.scm_api_region}.amazonaws.com/{self.config.scm_api_stage}/repositories/{self.config.scm_repo}/query/select?graphs={','.join(graphs)}&named=true",
            self._get_query(config),
            headers={
                "Authorization": f"Bearer {self.config.scm_access_token}",
            },
        )
        response.raise_for_status()
        try:
            return self._parse_query(response.json())
        except Exception as e:
            print(f"ERROR: Failed to query SCM with error {str(e)}")
            raise Exception("failed to transform JSON from query")

    def _parse_query(self, resp_obj) -> list[BaseQueryResponse]:
        return []

    def _convert_matched_instances(self, matching_instances, class_types: dict):
        for i in range(len(matching_instances)):
            for instance in matching_instances[i]:
                if instance in class_types:
                    class_type = class_types[instance]

                    if issubclass(class_type, Decimal):
                        matching_instances[i][instance] = Decimal(
                            matching_instances[i][instance]
                        )
                    else:
                        instance_data = matching_instances[i][instance]
                        if "type" in instance_data:
                            class_type = getattr(
                                simulation.query.queries.hydrogen_nrmm_optional,
                                instance_data["type"].replace("hydrogen_nrmm:", ""),
                            )
                            del instance_data["type"]
                        if not class_type in [str]:
                            matching_instances[i][instance] = class_type(
                                **instance_data
                            )

    def _get_matching_instances(self, bindings, class_types: dict) -> list[dict]:
        instances: list[dict] = []
        for binding in bindings:
            raw_instance = self._get_matching_instance(binding, class_types)
            existing = False
            index = 0
            for instance in instances:
                instance_data = instance[list(instance.keys())[0]]
                raw_instance_data = raw_instance[list(raw_instance.keys())[0]]
                if (
                    "id" in instance_data
                    and "id" in raw_instance_data
                    and instance_data["id"] == raw_instance_data["id"]
                ):
                    existing = True
                    break
                index += 1
            if existing:
                self._update_existing_instance(
                    raw_instance[list(raw_instance.keys())[0]],
                    instances[index][list(instances[index].keys())[0]],
                )
            else:
                instances.append(raw_instance)
        return instances

    def _update_existing_instance(self, raw_instance, new_data) -> None:
        array_properties = ["storedIn"]
        for prop in array_properties:
            if prop in raw_instance and prop in new_data:
                new_value = new_data[prop]
                if isinstance(raw_instance[prop], list):
                    raw_instance[prop] = [
                        ...(raw_instance[prop]),
                        ...(new_value) if isinstance(new_value, list) else new_value,
                    ]
                else:
                    raw_instance[prop] = [
                        raw_instance[prop],
                        ...(new_value) if isinstance(new_value, list) else new_value,
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
                attribute_name = item_name.replace(class_key, "")

                if class_key == "instance":
                    raw_instances[class_key] = item_value.replace(
                        "https://w3id.org/hydrologiq/hydrogen/nrmm", "hydrogen_nrmm:"
                    )
                else:
                    if item["type"] == "uri" and len(attribute_name) == 0:
                        raw_instances[class_key]["id"] = item_value.replace(
                            "https://w3id.org/hydrologiq/hydrogen/nrmm",
                            "hydrogen_nrmm:",
                        )
                    else:
                        if len(attribute_name) > 0:
                            attribute_name = (
                                attribute_name[0].lower() + attribute_name[1:]
                                if (not attribute_name.startswith("CO2e"))
                                else attribute_name
                            )
                            attr_value = (
                                item_value.replace(
                                    "https://w3id.org/hydrologiq/hydrogen/nrmm",
                                    "hydrogen_nrmm:",
                                )
                                if (item["type"] == "uri")
                                else item_value
                            )

                            if attribute_name == "type":
                                raw_instances[class_key][attribute_name] = attr_value
                            else:
                                raw_instances[class_key][attribute_name] = attr_value

                        else:
                            raw_instances[class_key] = item_value

        return raw_instances

    def _get_query(self, config: BaseQueryInput | None) -> str:
        return "blank"
