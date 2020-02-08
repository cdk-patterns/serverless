from typing import Any, Callable, Dict, Sequence, Type, TypeVar

import attr

from ._compat import is_sequence
from cattr.converters import Converter

T = TypeVar("T")


@attr.s(slots=True)
class AttributeOverride(object):
    omit_if_default = attr.ib(default=False, type=bool)


def override(omit_if_default=False):
    return AttributeOverride(omit_if_default=omit_if_default)


_neutral = AttributeOverride()


def make_dict_unstructure_fn(cl, converter, **kwargs):
    # type: (Type[T], Converter, **AttributeOverride) -> Callable[[T], Dict[str, Any]]  # noqa:E501
    """Generate a specialized dict unstructuring function for a class."""
    cl_name = cl.__name__
    fn_name = "unstructure_" + cl_name
    globs = {"__c_u": converter.unstructure}
    lines = []
    post_lines = []

    attrs = cl.__attrs_attrs__  # type: ignore

    lines.append("def {}(i):".format(fn_name))
    lines.append("    res = {")
    for a in attrs:
        attr_name = a.name
        override = kwargs.pop(attr_name, _neutral)
        d = a.default
        if a.type is None:
            # No type annotation, doing runtime dispatch.
            if d is not attr.NOTHING and override.omit_if_default:
                def_name = "__cattr_def_{}".format(attr_name)

                if isinstance(d, attr.Factory):
                    globs[def_name] = d.factory
                    if d.takes_self:
                        post_lines.append(
                            "    if i.{name} != {def_name}(i):".format(
                                name=attr_name, def_name=def_name
                            )
                        )
                    else:
                        post_lines.append(
                            "    if i.{name} != {def_name}():".format(
                                name=attr_name, def_name=def_name
                            )
                        )
                    post_lines.append(
                        "        res['{name}'] = i.{name}".format(
                            name=attr_name
                        )
                    )
                else:
                    globs[def_name] = d
                    post_lines.append(
                        "    if i.{name} != {def_name}:".format(
                            name=attr_name, def_name=def_name
                        )
                    )
                    post_lines.append(
                        "        res['{name}'] = __c_u(i.{name})".format(
                            name=attr_name
                        )
                    )

            else:
                # No default or no override.
                lines.append(
                    "        '{name}': __c_u(i.{name}),".format(name=attr_name)
                )
        else:
            # Do the dispatch here and now.
            type = a.type
            if is_sequence(type):
                type = Sequence
            conv_function = converter._unstructure_func.dispatch(type)
            if d is not attr.NOTHING and override.omit_if_default:
                def_name = "__cattr_def_{}".format(attr_name)

                if isinstance(d, attr.Factory):
                    # The default is computed every time.
                    globs[def_name] = d.factory
                    if d.takes_self:
                        post_lines.append(
                            "    if i.{name} != {def_name}(i):".format(
                                name=attr_name, def_name=def_name
                            )
                        )
                    else:
                        post_lines.append(
                            "    if i.{name} != {def_name}():".format(
                                name=attr_name, def_name=def_name
                            )
                        )
                    if conv_function == converter._unstructure_identity:
                        # Special case this, avoid a function call.
                        post_lines.append(
                            "        res['{name}'] = i.{name}".format(
                                name=attr_name
                            )
                        )
                    else:
                        unstruct_fn_name = "__cattr_unstruct_{}".format(
                            attr_name
                        )
                        globs[unstruct_fn_name] = conv_function
                        post_lines.append(
                            "        res['{name}'] = {fn}(i.{name}),".format(
                                name=attr_name, fn=unstruct_fn_name
                            )
                        )
                else:
                    # Default is not a factory, but a constant.
                    globs[def_name] = d
                    post_lines.append(
                        "    if i.{name} != {def_name}:".format(
                            name=attr_name, def_name=def_name
                        )
                    )
                    if conv_function == converter._unstructure_identity:
                        post_lines.append(
                            "        res['{name}'] = i.{name}".format(
                                name=attr_name
                            )
                        )
                    else:
                        unstruct_fn_name = "__cattr_unstruct_{}".format(
                            attr_name
                        )
                        globs[unstruct_fn_name] = conv_function
                        post_lines.append(
                            "        res['{name}'] = {fn}(i.{name})".format(
                                name=attr_name, fn=unstruct_fn_name
                            )
                        )
            else:
                # No omitting of defaults.
                if conv_function == converter._unstructure_identity:
                    # Special case this, avoid a function call.
                    lines.append(
                        "    '{name}': i.{name},".format(name=attr_name)
                    )
                else:
                    unstruct_fn_name = "__cattr_unstruct_{}".format(attr_name)
                    globs[unstruct_fn_name] = conv_function
                    lines.append(
                        "    '{name}': {fn}(i.{name}),".format(
                            name=attr_name, fn=unstruct_fn_name
                        )
                    )
    lines.append("    }")

    total_lines = lines + post_lines + ["    return res"]

    eval(compile("\n".join(total_lines), "", "exec"), globs)

    fn = globs[fn_name]

    return fn
