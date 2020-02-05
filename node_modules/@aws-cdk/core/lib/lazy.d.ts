import { IResolvable, IResolveContext } from "./resolvable";
/**
 * Interface for lazy string producers
 */
export interface IStringProducer {
    /**
     * Produce the string value
     */
    produce(context: IResolveContext): string | undefined;
}
/**
 * Interface for lazy list producers
 */
export interface IListProducer {
    /**
     * Produce the list value
     */
    produce(context: IResolveContext): string[] | undefined;
}
/**
 * Interface for lazy number producers
 */
export interface INumberProducer {
    /**
     * Produce the number value
     */
    produce(context: IResolveContext): number | undefined;
}
/**
 * Interface for lazy untyped value producers
 */
export interface IAnyProducer {
    /**
     * Produce the value
     */
    produce(context: IResolveContext): any;
}
/**
 * Options for creating a lazy string token
 */
export interface LazyStringValueOptions {
    /**
     * Use the given name as a display hint
     *
     * @default - No hint
     */
    readonly displayHint?: string;
}
/**
 * Options for creating a lazy list token
 */
export interface LazyListValueOptions {
    /**
     * Use the given name as a display hint
     *
     * @default - No hint
     */
    readonly displayHint?: string;
    /**
     * If the produced list is empty, return 'undefined' instead
     *
     * @default false
     */
    readonly omitEmpty?: boolean;
}
/**
 * Options for creating lazy untyped tokens
 */
export interface LazyAnyValueOptions {
    /**
     * Use the given name as a display hint
     *
     * @default - No hint
     */
    readonly displayHint?: string;
    /**
     * If the produced value is an array and it is empty, return 'undefined' instead
     *
     * @default false
     */
    readonly omitEmptyArray?: boolean;
}
/**
 * Lazily produce a value
 *
 * Can be used to return a string, list or numeric value whose actual value
 * will only be calculated later, during synthesis.
 */
export declare class Lazy {
    static stringValue(producer: IStringProducer, options?: LazyStringValueOptions): string;
    static numberValue(producer: INumberProducer): number;
    static listValue(producer: IListProducer, options?: LazyListValueOptions): string[];
    static anyValue(producer: IAnyProducer, options?: LazyAnyValueOptions): IResolvable;
    private constructor();
}
