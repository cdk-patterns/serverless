export const StackConfiguration = {
  provider: {
    name: 'auth0',
    configuration: {
      oidc: {
        type: 'OIDC',
        clientId: 's2OaAj303YeD8KUGSUfmCpVnQWwjBQyR',
        clientSecret: 'LWTIrj6-WQe9SWNRvRBCknmnuttXSUc0x-f6SbuRWisCgu45WCqXXBuyrwyWnhQz', // Please never commit this value into a cfg management system.. we will adopt a secrets impl for this in future.
        issuerEnpoint: 'https://dev-a4bk90gw.us.auth0.com',
        callbackUrls: 'http://localhost:8080/callback',
        logoutUrls: 'http://localhost:8080/logout',
        claimsAttrRef: 'roles'//auth0 },       
      },
      saml: {
        type: 'SAML',
        metadataURL: 'https://dev-a4bk90gw.us.auth0.com/samlp/metadata/s2OaAj303YeD8KUGSUfmCpVnQWwjBQyR',
        claimsAttrRef: 'http://schemas.auth0.com/roles', 
        callbackUrls: 'http://localhost:8080/callback',
        logoutUrls: 'http://localhost:8080/logout',  
      },
    },
  },
  cognitoDomainName: 'swa-hits'
}
