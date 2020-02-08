from enum import Enum
from typing import (  # noqa: F401, imported for Mypy.
    Any,
    Callable,
    Dict,
    FrozenSet,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
)
from ._compat import (
    bytes,
    is_bare,
    is_frozenset,
    is_mapping,
    is_mutable_set,
    is_py2,
    is_sequence,
    is_tuple,
    is_union_type,
    lru_cache,
    unicode,
)
from .disambiguators import create_uniq_field_dis_func
from .multistrategy_dispatch import MultiStrategyDispatch


NoneType = type(None)
T = TypeVar("T")
V = TypeVar("V")


class UnstructureStrategy(Enum):
    """`attrs` classes unstructuring strategies."""

    AS_DICT = "asdict"
    AS_TUPLE = "astuple"


def _is_attrs_class(cls):
    return getattr(cls, "__attrs_attrs__", None) is not None


def _subclass(typ):
    """ a shortcut """
    return lambda cls: issubclass(cls, typ)


class Converter(object):
    """Converts between structured and unstructured data."""

    __slots__ = (
        "_dis_func_cache",
        "_unstructure_func",
        "_unstructure_attrs",
        "_structure_attrs",
        "_dict_factory",
        "_union_registry",
        "_structure_func",
    )

    def __init__(
        self, dict_factory=dict, unstruct_strat=UnstructureStrategy.AS_DICT
    ):
        unstruct_strat = UnstructureStrategy(unstruct_strat)

        # Create a per-instance cache.
        if unstruct_strat is UnstructureStrategy.AS_DICT:
            self._unstructure_attrs = self.unstructure_attrs_asdict
            self._structure_attrs = self.structure_attrs_fromdict
        else:
            self._unstructure_attrs = self.unstructure_attrs_astuple
            self._structure_attrs = self.structure_attrs_fromtuple

        self._dis_func_cache = lru_cache()(self._get_dis_func)

        self._unstructure_func = MultiStrategyDispatch(
            self._unstructure_identity
        )
        self._unstructure_func.register_cls_list(
            [
                (bytes, self._unstructure_identity),
                (unicode, self._unstructure_identity),
            ]
        )
        self._unstructure_func.register_func_list(
            [
                (_subclass(Mapping), self._unstructure_mapping),
                (_subclass(Sequence), self._unstructure_seq),
                (_subclass(Set), self._unstructure_seq),
                (_subclass(FrozenSet), self._unstructure_seq),
                (_subclass(Enum), self._unstructure_enum),
                (_is_attrs_class, self._unstructure_attrs),
            ]
        )

        # Per-instance register of to-attrs converters.
        # Singledispatch dispatches based on the first argument, so we
        # store the function and switch the arguments in self.loads.
        self._structure_func = MultiStrategyDispatch(self._structure_default)
        self._structure_func.register_func_list(
            [
                (is_sequence, self._structure_list),
                (is_mutable_set, self._structure_set),
                (is_frozenset, self._structure_frozenset),
                (is_tuple, self._structure_tuple),
                (is_mapping, self._structure_dict),
                (is_union_type, self._structure_union),
                (_is_attrs_class, self._structure_attrs),
            ]
        )
        # Strings are sequences.
        self._structure_func.register_cls_list(
            [
                (
                    unicode,
                    self._structure_unicode
                    if is_py2
                    else self._structure_call,
                ),
                (bytes, self._structure_call),
                (int, self._structure_call),
                (float, self._structure_call),
                (Enum, self._structure_call),
            ]
        )

        self._dict_factory = dict_factory

        # Unions are instances now, not classes. We use different registry.
        self._union_registry = {}

    def unstructure(self, obj):
        # type: (Any) -> Any
        return self._unstructure_func.dispatch(obj.__class__)(obj)

    @property
    def unstruct_strat(self):
        # type: () -> UnstructureStrategy
        """The default way of unstructuring ``attrs`` classes."""
        return (
            UnstructureStrategy.AS_DICT
            if self._unstructure_attrs == self.unstructure_attrs_asdict
            else UnstructureStrategy.AS_TUPLE
        )

    def register_unstructure_hook(self, cls, func):
        # type: (Type[T], Callable[[T], Any]) -> None
        """Register a class-to-primitive converter function for a class.

        The converter function should take an instance of the class and return
        its Python equivalent.
        """
        self._unstructure_func.register_cls_list([(cls, func)])

    def register_unstructure_hook_func(self, check_func, func):
        """Register a class-to-primitive converter function for a class, using
        a function to check if it's a match.
        """
        self._unstructure_func.register_func_list([(check_func, func)])

    def register_structure_hook(self, cl, func):
        """Register a primitive-to-class converter function for a type.

        The converter function should take two arguments:
          * a Python object to be converted,
          * the type to convert to

        and return the instance of the class. The type may seem redundant, but
        is sometimes needed (for example, when dealing with generic classes).
        """
        if is_union_type(cl):
            self._union_registry[cl] = func
        else:
            self._structure_func.register_cls_list([(cl, func)])

    def register_structure_hook_func(self, check_func, func):
        # type: (Callable[[Any], Any], Callable[[T], Any]) -> None
        """Register a class-to-primitive converter function for a class, using
        a function to check if it's a match.
        """
        self._structure_func.register_func_list([(check_func, func)])

    def structure(self, obj, cl):
        # type: (Any, Type[T]) -> T
        """Convert unstructured Python data structures to structured data."""

        return self._structure_func.dispatch(cl)(obj, cl)

    # Classes to Python primitives.
    def unstructure_attrs_asdict(self, obj):
        # type: (Any) -> Dict[str, Any]
        """Our version of `attrs.asdict`, so we can call back to us."""
        attrs = obj.__class__.__attrs_attrs__
        dispatch = self._unstructure_func.dispatch
        rv = self._dict_factory()
        for a in attrs:
            name = a.name
            v = getattr(obj, name)
            rv[name] = dispatch(v.__class__)(v)
        return rv

    def unstructure_attrs_astuple(self, obj):
        # type: (Any) -> Tuple
        """Our version of `attrs.astuple`, so we can call back to us."""
        attrs = obj.__class__.__attrs_attrs__
        return tuple(self.unstructure(getattr(obj, a.name)) for a in attrs)

    def _unstructure_enum(self, obj):
        """Convert an enum to its value."""
        return obj.value

    def _unstructure_identity(self, obj):
        """Just pass it through."""
        return obj

    def _unstructure_seq(self, seq):
        """Convert a sequence to primitive equivalents."""
        # We can reuse the sequence class, so tuples stay tuples.
        dispatch = self._unstructure_func.dispatch
        return seq.__class__(dispatch(e.__class__)(e) for e in seq)

    def _unstructure_mapping(self, mapping):
        """Convert a mapping of attr classes to primitive equivalents."""

        # We can reuse the mapping class, so dicts stay dicts and OrderedDicts
        # stay OrderedDicts.
        dispatch = self._unstructure_func.dispatch
        return mapping.__class__(
            (dispatch(k.__class__)(k), dispatch(v.__class__)(v))
            for k, v in mapping.items()
        )

    # Python primitives to classes.

    def _structure_default(self, obj, cl):
        """This is the fallthrough case. Everything is a subclass of `Any`.

        A special condition here handles ``attrs`` classes.

        Bare optionals end here too (optionals with arguments are unions.) We
        treat bare optionals as Any.
        """
        if cl is Any or cl is Optional:
            return obj
        # We don't know what this is, so we complain loudly.
        msg = (
            "Unsupported type: {0}. Register a structure hook for "
            "it.".format(cl)
        )
        raise ValueError(msg)

    def _structure_call(self, obj, cl):
        """Just call ``cl`` with the given ``obj``.

        This is just an optimization on the ``_structure_default`` case, when
        we know we can skip the ``if`` s. Use for ``str``, ``bytes``, ``enum``,
        etc.
        """
        return cl(obj)

    def _structure_unicode(self, obj, cl):
        """Just call ``cl`` with the given ``obj``"""
        if not isinstance(obj, (bytes, unicode)):
            return cl(str(obj))
        else:
            return obj

    # Attrs classes.

    def structure_attrs_fromtuple(self, obj, cl):
        # type: (Tuple, Type[T]) -> T
        """Load an attrs class from a sequence (tuple)."""
        conv_obj = []  # A list of converter parameters.
        for a, value in zip(cl.__attrs_attrs__, obj):  # type: ignore
            # We detect the type by the metadata.
            converted = self._structure_attr_from_tuple(a, a.name, value)
            conv_obj.append(converted)

        return cl(*conv_obj)  # type: ignore

    def _structure_attr_from_tuple(self, a, name, value):
        """Handle an individual attrs attribute."""
        type_ = a.type
        if type_ is None:
            # No type metadata.
            return value
        return self._structure_func.dispatch(type_)(value, type_)

    def structure_attrs_fromdict(self, obj, cl):
        # type: (Mapping[str, Any], Type[T]) -> T
        """Instantiate an attrs class from a mapping (dict)."""
        # For public use.
        conv_obj = {}  # Start with a fresh dict, to ignore extra keys.
        dispatch = self._structure_func.dispatch
        for a in cl.__attrs_attrs__:  # type: ignore
            # We detect the type by metadata.
            type_ = a.type
            name = a.name

            try:
                val = obj[name]
            except KeyError:
                continue

            if name[0] == "_":
                name = name[1:]

            conv_obj[name] = (
                dispatch(type_)(val, type_) if type_ is not None else val
            )

        return cl(**conv_obj)  # type: ignore

    def _structure_list(self, obj, cl):
        """Convert an iterable to a potentially generic list."""
        if is_bare(cl) or cl.__args__[0] is Any:
            return [e for e in obj]
        else:
            elem_type = cl.__args__[0]
            return [
                self._structure_func.dispatch(elem_type)(e, elem_type)
                for e in obj
            ]

    def _structure_set(self, obj, cl):
        """Convert an iterable into a potentially generic set."""
        if is_bare(cl) or cl.__args__[0] is Any:
            return set(obj)
        else:
            elem_type = cl.__args__[0]
            return {
                self._structure_func.dispatch(elem_type)(e, elem_type)
                for e in obj
            }

    def _structure_frozenset(self, obj, cl):
        """Convert an iterable into a potentially generic frozenset."""
        if is_bare(cl) or cl.__args__[0] is Any:
            return frozenset(obj)
        else:
            elem_type = cl.__args__[0]
            dispatch = self._structure_func.dispatch
            return frozenset(dispatch(elem_type)(e, elem_type) for e in obj)

    def _structure_dict(self, obj, cl):
        """Convert a mapping into a potentially generic dict."""
        if is_bare(cl) or cl.__args__ == (Any, Any):
            return dict(obj)
        else:
            key_type, val_type = cl.__args__
            if key_type is Any:
                val_conv = self._structure_func.dispatch(val_type)
                return {k: val_conv(v, val_type) for k, v in obj.items()}
            elif val_type is Any:
                key_conv = self._structure_func.dispatch(key_type)
                return {key_conv(k, key_type): v for k, v in obj.items()}
            else:
                key_conv = self._structure_func.dispatch(key_type)
                val_conv = self._structure_func.dispatch(val_type)
                return {
                    key_conv(k, key_type): val_conv(v, val_type)
                    for k, v in obj.items()
                }

    def _structure_union(self, obj, union):
        """Deal with converting a union."""
        # Unions with NoneType in them are basically optionals.
        # We check for NoneType early and handle the case of obj being None,
        # so disambiguation functions don't need to handle NoneType.
        union_params = union.__args__
        if NoneType in union_params:  # type: ignore
            if obj is None:
                return None
            if len(union_params) == 2:
                # This is just a NoneType and something else.
                other = (
                    union_params[0]
                    if union_params[1] is NoneType  # type: ignore
                    else union_params[1]
                )
                # We can't actually have a Union of a Union, so this is safe.
                return self._structure_func.dispatch(other)(obj, other)

        # Check the union registry first.
        handler = self._union_registry.get(union)
        if handler is not None:
            return handler(obj, union)

        # Getting here means either this is not an optional, or it's an
        # optional with more than one parameter.
        # Let's support only unions of attr classes for now.
        cl = self._dis_func_cache(union)(obj)
        return self._structure_func.dispatch(cl)(obj, cl)

    def _structure_tuple(self, obj, tup):
        """Deal with converting to a tuple."""
        tup_params = tup.__args__
        has_ellipsis = tup_params and tup_params[-1] is Ellipsis
        if tup_params is None or (has_ellipsis and tup_params[0] is Any):
            # Just a Tuple. (No generic information.)
            return tuple(obj)
        if has_ellipsis:
            # We're dealing with a homogenous tuple, Tuple[int, ...]
            tup_type = tup_params[0]
            conv = self._structure_func.dispatch(tup_type)
            return tuple(conv(e, tup_type) for e in obj)
        else:
            # We're dealing with a heterogenous tuple.
            return tuple(
                self._structure_func.dispatch(t)(e, t)
                for t, e in zip(tup_params, obj)
            )

    def _get_dis_func(self, union):
        # type: (Type) -> Callable[..., Type]
        """Fetch or try creating a disambiguation function for a union."""
        union_types = union.__args__
        if NoneType in union_types:  # type: ignore
            # We support unions of attrs classes and NoneType higher in the
            # logic.
            union_types = tuple(
                e for e in union_types if e is not NoneType  # type: ignore
            )

        if not all(hasattr(e, "__attrs_attrs__") for e in union_types):
            raise ValueError(
                "Only unions of attr classes supported "
                "currently. Register a loads hook manually."
            )
        return create_uniq_field_dis_func(*union_types)
