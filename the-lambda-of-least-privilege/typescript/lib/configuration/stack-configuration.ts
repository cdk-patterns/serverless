export const StackConfiguration = {
  provider: {
    name: '{ provider name like auth0, ping, azure}',
    type: '{ provider type i.e. SAML or OIDC}',
    clientId: '{ Client Secret - for your approved application }',
    clientSecret: '{ Client Secret - for your approved application}', // Please never commit this value into a cfg management system.. we will adopt a secrets impl for this in future.
    issuerEnpoint: '{ Provider Issuer URL - Retrieve from the OIDC Configuration endpoint}',
    callbackUrls: '{http://localhost:3000/callback - call back urls for your endpoint }',
    logoutUrls: '{http://localhost:3000 - The logout URL for your client application }',
    authorize_url: '{ OIDC Authorise endpoint }', // TODO
    token_url: '{ OIDC Token endpoint }', //TODO
    attributes_url: '{ Attributes endpoint }',
    jwks_uri: '{ JSON Webtoken Key Service endpoint }',
    claimsAttrRef: '{ custom grouping of user claims reference, i.e. groups }', 
  },
  cognitoDomainName: '{ The name of your Cognito Domain}'
};
