
"""
Publication helps you maintain public-api-friendly modules by preventing \
unintentional access to private implementation details via introspection.

It's easy to use::

    # yourmodule.py
    import dependency1
    import dependency2

    from publication import publish

    def implementation_detail():
        ...

    def stuff():
        ...
        implementation_detail()
        ...

    __all__ = [
        'stuff'
    ]

    publish()

Now, C{from yourmodule import dependency1} just raises an C{ImportError} - as
you would want; C{dependency1} isn't part of yourmodule!  So does C{from
yourmodule import dependency1} Only C{stuff} is I{supposed} to be in the public
interface you're trying to support, so only it can be imported.

All your implementation details are still accessible in a namespace called
C{_private}, which you can still use via C{from yourmodule._private import
dependency1}, for white-box testing and similar use-cases.
"""

from types import ModuleType
import sys

PRIVATE_NAME = "_private"

_nothing = object()


def publish():
    # type: () -> None
    """
    Publish the interface of the calling module as defined in C{__all__};
    relegate the rest of it to a C{_private} API module.

    Call it at the top level of your module after C{__all__} and all the names
    described in it are defined; usually the best place to do this is as the
    module's last line.
    """
    localvars = sys._getframe(1).f_locals
    name = localvars["__name__"]
    all = localvars["__all__"]
    public = ModuleType(name)
    private = sys.modules[name]
    sys.modules[name] = public
    names = all + [
        "__all__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__path__",
        "__spec__",
    ]
    for published in names:
        value = getattr(private, published, _nothing)
        if value is not _nothing:
            setattr(public, published, value)
    setattr(public, PRIVATE_NAME, private)
    sys.modules[".".join([name, PRIVATE_NAME])] = private


__version__ = "0.0.3"

__all__ = ["publish", "__version__"]
publish()
