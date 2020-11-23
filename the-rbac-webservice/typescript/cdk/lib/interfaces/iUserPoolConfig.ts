export interface iUserPoolConfig {
    allowedOAuthFlowsUserPoolClient: boolean;
    allowedOAuthFlows: Array<string>;
    allowedOAuthScopes: Array<string>;
    refreshTokenValidity: number;
    writeAttributes: Array<string>;
    callbackUrLs: Array<string>;
    logoutUrLs: Array<string>;
}