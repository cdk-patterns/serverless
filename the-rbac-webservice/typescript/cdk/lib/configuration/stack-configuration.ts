import { eRequestMethod } from "../enums/eRequestMethod";
import { iStackConfiguration } from "./config-interfaces";

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

const OIDC_ISSUER: string = '';

const OIDC_ATTRIBUTES_REQUEST_METHOD: eRequestMethod = eRequestMethod.GET;

/**
 * ============================================================================================
 *  EXTERNAL IDENTITY PROVIDER SAML CONFIGURATION
 * 
 *    If connecting to your IDP using SAML configure the properties prefixed SAML_
 *  
 * ============================================================================================
 */
const SAML_METADATA_URL: string = 'http://saml-metadataurl.com/example/url';

/**
 * ============================================================================================
 *   USER POOL ATTRIBUTE CONFIGURATION
 * 
 *  You will probably want to see some attributes stored within the External IDP in your Cognito UserPool
 * 
 *  https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html
 * 
 *  TODO The should put configured as MAP for a future extension of the pattern.
 * ============================================================================================
 */

// These are the attributes that you want to map from your external IDP
const CUSTOM_ROLES_ATTR_DETAILS = {
  schema: {
    name: "roles", // Once this attribute is added to the userpool it will be pre:fixed 'custom:' 
    attributeDataType: "String",
    mutable: true,
    required: false,
    stringAttributeConstraints: {
      maxLength: "2048",
      minLength: "1"
    }
  },
  saml_ns_ref: "http://schemas.auth0.com/roles",
  oidc_ns_ref: "",
  userPoolAttrRef: "custom:roles"
}

const EMAIL_SAML_REF = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
const EMAIL_MAP_TARGET_ATTR = "Email"
// This is where we take the Third Party Attribute and map ito the UserPooL Attribute we just created.
const IDENTITY_PROVIDER_ATTR_MAP = {
  [CUSTOM_ROLES_ATTR_DETAILS.userPoolAttrRef]: CUSTOM_ROLES_ATTR_DETAILS.saml_ns_ref,
  [EMAIL_MAP_TARGET_ATTR]: EMAIL_SAML_REF
}

/**
 * ============================================================================================
 *  COGNITO APP CLIENT CONFIGURATION
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
 *  TODO Shouldnt have to change the below config. Change the variables above.
 * ============================================================================================
 */
export const StackConfiguration: iStackConfiguration = {

  cognitoDomain: COGNITO_DOMAIN,

  userPoolConfig: {
    allowedOAuthFlowsUserPoolClient: CLIENT_ALLOWED_OAUTH_FLOW_USERPOOL_CLIENT,
    allowedOAuthFlows: CLIENT_ALLOWED_OAUTH_FLOWS,
    allowedOAuthScopes: CLIENT_ALLOWED_OAUTH_SCOPES,
    refreshTokenValidity: CLIENT_REFRESH_TOKEN_VALIDITY,
    writeAttributes: [CUSTOM_ROLES_ATTR_DETAILS.userPoolAttrRef, EMAIL_MAP_TARGET_ATTR], //We are updating these with values from the external IDP
    callbackUrLs: CLIENT_CALLBACKURLS,
    logoutUrLs: CLIENT_LOGOUTURLS,
  },

  userPoolAttrSchema: [CUSTOM_ROLES_ATTR_DETAILS.schema], // extend this with any other mappings

  cognitoDestAttr: CUSTOM_ROLES_ATTR_DETAILS.userPoolAttrRef, // Setting up the UserPoolAttr will prefix the attribute with custom:

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
      attributeMapping: IDENTITY_PROVIDER_ATTR_MAP,
    },
    samlProvider: {
      type: 'SAML',
      details: {
        MetaDataURL: SAML_METADATA_URL
      },
      attributeMapping: IDENTITY_PROVIDER_ATTR_MAP,
    }
  }
}

