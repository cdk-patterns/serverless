import { iSAMLProviderConfig } from "../interfaces/ISAMLProviderConfig";
import { iOIDCProviderConfig } from "../interfaces/iOIDCProviderConfig";
import { iAttrSchema } from "../interfaces/iAttrSchema";
import { iUserPoolConfig } from "../interfaces/iUserPoolConfig";

export interface iStackConfiguration {
    userPoolConfig: iUserPoolConfig;
    cognitoDestAttr: string,
    userPoolAttrSchema: Array<iAttrSchema>;
    identityProviders: {
      providerName: string;
      oidcProvider?: iOIDCProviderConfig;
      samlProvider?: iSAMLProviderConfig;
    },
    cognitoDomain: string;
  }