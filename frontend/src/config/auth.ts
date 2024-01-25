export const AwsConfigAuth = {
  region: import.meta.env.VITE_AWS_AUTH_REGION,
  userPoolId: import.meta.env.VITE_AWS_AUTH_USER_POOL_ID,
  userPoolClientId: import.meta.env.VITE_AWS_AUTH_USER_POOL_WEB_CLIENT_ID,
  cookieStorage: {
    domain: import.meta.env.VITE_AWS_AUTH_COOKIE_STORAGE_DOMAIN,
    path: "/",
    expires: 365,
    sameSite: "strict",
    secure: true,
  },
  authenticationFlowType: "USER_SRP_AUTH",
}
