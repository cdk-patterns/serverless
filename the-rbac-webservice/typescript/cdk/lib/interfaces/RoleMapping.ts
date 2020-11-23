import { eMatchTypes } from '../enums/eMatchTypes';
export interface RoleMapping {
    claim: string;
    matchType: eMatchTypes;
    roleArn: string;
    value: string;
  }