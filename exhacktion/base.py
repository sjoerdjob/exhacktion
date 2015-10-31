"""
Defines the base `instance_checking_exception` creator.
"""

import sys


def instance_checking_exception(instance_checker):
    class TemporaryClass(Exception):
        class __metaclass__(type):
            def __instancecheck__(cls, inst):
                return instance_checker(inst)

            def __subclasscheck__(cls, classinfo):
                # This hook is called during the exception handling.
                # Unfortunately, we would rather have exception handling call
                # __instancecheck__, so we have to do that ourselves. But,
                # that's not how it currently is.  If you feel like proposing a
                # patch for Python, check the function
                # `PyErr_GivenExceptionMatches` in `Python/error.c`.
                value = sys.exc_info()[1]

                # Double-check that the exception given actually somewhat
                # matches the classinfo we received. If not, people are using
                # `issubclass` directly, which is of course prone to errors.
                assert value.__class__ == classinfo

                return isinstance(value, cls)
    TemporaryClass.__name__ = instance_checker.__name__
    TemporaryClass.__doc__ = instance_checker.__doc__
    return TemporaryClass
