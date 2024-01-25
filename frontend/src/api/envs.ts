import { fetchAuthSession } from "aws-amplify/auth"

export const getAPISimulationURL = () => import.meta.env.VITE_API_SIMULATION_URL
export const getAPISimulationVersion = () => import.meta.env.VITE_API_SIMULATION_VERSION
export const getAPISimulationRepo = () => import.meta.env.VITE_API_SIMULATION_REPO
export const getAPISimulationAccessToken = async () =>
  await fetchAuthSession({ forceRefresh: true }).then((session) => {
    return session.tokens?.accessToken?.toString()
  })
