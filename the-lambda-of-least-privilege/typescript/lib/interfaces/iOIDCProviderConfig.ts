import { eRequestMethod } from "../enums/eRequestMethod";
export interface iOIDCProviderConfig {
    type: string;
    details: {
        attributes_request_method: eRequestMethod;
        authorize_scopes: string;
        client_id: string;
        client_secret: string;
        oidc_issuer: string;
    }
    attributeMapping: object;
}