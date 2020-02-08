from ._compat import lru_cache


class FunctionDispatch(object):
    """
    FunctionDispatch is similar to functools.singledispatch, but
    instead dispatches based on functions that take the type of the
    first argument in the method, and return True or False.

    objects that help determine dispatch should be instantiated objects.
    """

    __slots__ = ("_handler_pairs", "dispatch")

    def __init__(self):
        self._handler_pairs = []
        self.dispatch = lru_cache(64)(self._dispatch)

    def register(self, can_handle, func):
        self._handler_pairs.insert(0, (can_handle, func))
        self.dispatch.cache_clear()

    def _dispatch(self, typ):
        """
        returns the appropriate handler, for the object passed.
        """
        for can_handle, handler in self._handler_pairs:
            # can handle could raise an exception here
            # such as issubclass being called on an instance.
            # it's easier to just ignore that case.
            try:
                if can_handle(typ):
                    return handler
            except Exception:
                pass
        raise KeyError("unable to find handler for {0}".format(typ))
