import axios from "axios"
import { getAPISimulationURL, getAPISimulationVersion, getAPISimulationRepo, getAPISimulationAccessToken } from "./envs"
import { SimulationResults } from "@custom/types/generated/SimulationResults"

export const simulation = async (data: Record<string, any>, instances: string[]): Promise<SimulationResults> => {
  return axios
    .post(
      `${getAPISimulationURL()}/${getAPISimulationVersion()}/repositories/${getAPISimulationRepo()}/simulation?instances=${instances.join(
        ","
      )}`,
      JSON.stringify(data),
      {
        headers: { Authorization: `Bearer ${await getAPISimulationAccessToken()}` },
      }
    )
    .then((data) => data.data)
}
