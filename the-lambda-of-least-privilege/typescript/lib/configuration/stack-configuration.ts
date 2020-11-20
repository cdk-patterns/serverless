import { eRequestMethod } from "../enums/eRequestMethod";
import { iStackConfiguration} from "./config-interfaces";

    const EXTERNAL_IDENTITY_PROVIDER_NAME = "Auth0";

/**
 * ============================================================================================
 *  EXTERNAL IDENTITY PROVIDER OIDC CONFIGURATION
 * 
 *    If connecting via OIDC Configure the properties prefixed OIDC_
 * 
 * ============================================================================================
 */
    const OIDC_AUTHORIZE_SCOPE: string = 'openid profile';

    const OIDC_CLIENT_ID: string = '';

    const OIDC_CLIENT_SECRET: string = ''; // DONOT COMMIT THIS POPULATED INTO SOURCE CONTROL

    const OIDC_ISSUER:string = '';

    const OIDC_ATTRIBUTES_REQUEST_METHOD: eRequestMethod = eRequestMethod.GET;

/**
 * ============================================================================================
 *  EXTERNAL IDENTITY PROVIDER SAML CONFIGURATION
 * 
 *    If connecting to your IDP using SAML configure the properties prefixed SAML_
 *  
 * ============================================================================================
 */
    const SAML_METADATA_URL: string = 'https://dev-a4bk90gw.us.auth0.com/samlp/metadata/s2OaAj303YeD8KUGSUfmCpVnQWwjBQyR';

/**
 * ============================================================================================
 * ATTRIBUTE DEFINITION FOR USER POOL
 * 
 *  You will probably want to see some attributes stored within the External IDP in your Cognito UserPool
 * 
 *  https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
 * 
 * ============================================================================================
 */
    const IDP_CLAIM_ATTRIBUTE: string = "groups";

    const IDP_CLAIM_ATTRIBUTE_NS: string = "http://schemas.auth0.com/roles"; //SAML NS

    const COGNITO_CLAIM_ATTRIBUTE: string = "custom:" + IDP_CLAIM_ATTRIBUTE;

    const ATTRIBUTE_DATA_TYPE: string = "String";

    const ATTRIBUTE_MUTABILITY: boolean =  true;

    const ATTRIBUTE_REQUIRED: boolean = false;

    const ATTRIBUTE_MAX_LENGTH: string = "2048";
    
    const ATTRIBUTE_MIN_LENGTH: string = "1";
/**
 * ============================================================================================
 *  YOUR APPLICATION WILL AUTHENTICATE AGAINST A COGNITO IDENTITY POOL Using OIDC
 * 
 *  OIDC Configuration for the Cognito APP Client
 *  
 *  https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
 * 
 * ============================================================================================
 */

    const COGNITO_DOMAIN: string = "swa-hits";

    const CLIENT_CALLBACKURLS: Array<string> = ['http://localhost:8080/callback'];

    const CLIENT_LOGOUTURLS: Array<string> = ['http://localhost:8080/logout'];

    const CLIENT_ALLOWED_OAUTH_FLOW_USERPOOL_CLIENT: boolean = true;

    const CLIENT_ALLOWED_OAUTH_FLOWS: Array<string> = ['code'];

    const CLIENT_ALLOWED_OAUTH_SCOPES: Array<string> = ["openid", "profile", "aws.cognito.signin.user.admin"];

    const CLIENT_REFRESH_TOKEN_VALIDITY: number = 1;

/**
 * ============================================================================================
 * 
 * Setup the configuration for your Configuration for your Cognito Identity Pool
 * 
 * ============================================================================================
 */
export const StackConfiguration: iStackConfiguration = {
 
  cognitoDomain: COGNITO_DOMAIN,

  userPoolConfig: {
    allowedOAuthFlowsUserPoolClient: CLIENT_ALLOWED_OAUTH_FLOW_USERPOOL_CLIENT,
    allowedOAuthFlows: CLIENT_ALLOWED_OAUTH_FLOWS,
    allowedOAuthScopes: CLIENT_ALLOWED_OAUTH_SCOPES,
    refreshTokenValidity: CLIENT_REFRESH_TOKEN_VALIDITY,
    writeAttributes: [COGNITO_CLAIM_ATTRIBUTE],
    callbackUrLs: CLIENT_CALLBACKURLS,
    logoutUrLs: CLIENT_LOGOUTURLS,
  },

  userPoolAttrSchema: [{
    name: IDP_CLAIM_ATTRIBUTE,
    attributeDataType: ATTRIBUTE_DATA_TYPE,
    mutable: ATTRIBUTE_MUTABILITY,
    required: ATTRIBUTE_REQUIRED,
    stringAttributeConstraints: {
      maxLength: ATTRIBUTE_MAX_LENGTH,
      minLength: ATTRIBUTE_MIN_LENGTH
    }
  }],

  identityProviders: {
    providerName: EXTERNAL_IDENTITY_PROVIDER_NAME,
    oidcProvider: {
      type: 'OIDC',
      details: {
        attributes_request_method: OIDC_ATTRIBUTES_REQUEST_METHOD,
        authorize_scopes: OIDC_AUTHORIZE_SCOPE,
        client_id: OIDC_CLIENT_ID,
        client_secret: OIDC_CLIENT_SECRET,
        oidc_issuer: OIDC_ISSUER,
      },
      attributeMapping: {
        [IDP_CLAIM_ATTRIBUTE_NS]: IDP_CLAIM_ATTRIBUTE
      },
    },
    samlProvider: {
      type: 'SAML',
      details: {
        MetaDataURL: SAML_METADATA_URL
      },
      attributeMapping: {
        [IDP_CLAIM_ATTRIBUTE_NS]: IDP_CLAIM_ATTRIBUTE
      }
    }
  }
}

