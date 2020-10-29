import { RoleMapping } from "../lib/interfaces/RoleMapping";
/**
 * Class for helping define the mapping JWT user Claims to IAM roles
 */
export class RoleMapper {

  rules: RoleMapping[];

  constructor(){
    this.rules = [];
  }

  /**
   * Use this class to collect the rules to support the role mapping for your IAM users.
   * 
   * @param rule @type RoleMapping
   * 
   * TODO Create some tests for this class that generates example configuration.
   */
  addMapping(rule: RoleMapping) {
    this.rules.push(rule);
  }

  getRules() {
    return this.rules;
  }
}