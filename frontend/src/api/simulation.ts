import axios, { AxiosResponse } from "axios"
import { getAPISimulationURL, getAPISimulationVersion, getAPISimulationRepo, getAPISimulationAccessToken } from "./envs"

export const simulation = async (data: any): Promise<AxiosResponse<any, any>> => {
  return axios.post(
    `${getAPISimulationURL()}/${getAPISimulationVersion()}/repositories/${getAPISimulationRepo()}/simulation`,
    JSON.stringify(data),
    {
      headers: { Authorization: `Bearer ${await getAPISimulationAccessToken()}` },
    }
  )
}
