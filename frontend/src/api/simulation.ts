import axios from "axios"
import { getAPISimulationURL, getAPISimulationVersion, getAPISimulationRepo, getAPISimulationAccessToken } from "./envs"
import { SimulationResults } from "@custom/types/generated/SimulationResults"

export const simulation = async (data: any): Promise<SimulationResults> => {
  return axios
    .post(
      `${getAPISimulationURL()}/${getAPISimulationVersion()}/repositories/${getAPISimulationRepo()}/simulation`,
      JSON.stringify(data),
      {
        headers: { Authorization: `Bearer ${await getAPISimulationAccessToken()}` },
      }
    )
    .then((data) => data.data)
}
