export interface iSAMLProviderConfig {
    type: string;
    details: {
        MetaDataURL: string;
    }
    attributeMapping: object;
}