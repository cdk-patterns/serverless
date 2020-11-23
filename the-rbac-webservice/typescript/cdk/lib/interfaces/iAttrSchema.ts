export interface iAttrSchema {
    name: string;
    attributeDataType: string;
    mutable: boolean;
    required: boolean,
    stringAttributeConstraints: {
      maxLength: string;
      minLength: string;
    }
  }