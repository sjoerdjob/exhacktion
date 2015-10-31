"""
Defines the base `instance_checking_exception` creator.
"""

import re
import sys


def instance_checking_exception(instance_checker):
    """
    Create an exception class which inspects the exception being raised.

    This is most easily used as a decorator:

    >>> @instance_checking_exception
    ... def Foo(inst):
    ...     return "Foo" in inst.message
    >>> try:
    ...     raise Exception("Something Fooish")
    ... except Foo as e:
    ...     print "True"
    ... except Exception:
    ...     print "False"
    True

    This is quite a powerful tool, mind you.

    Arguments:
        instance_checker (callable): A function which checks if the given
            instance should be treated as an instance of a (subclass) of this
            exception.

    Returns:
        Exception: (Actually: a new subclass of it), which calls the argument
            `instance_checker` when it is checked against during exception
            handling logic.
    """
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


def message_checking_exception(regex, classname=None):
    """
    Create exception class which matches message against regular expression.

    >>> Foo = message_checking_exception("Fooish", "Foo")
    >>> Foo.__class__.__name__
    'Foo'
    >>> try:
    ...     raise Exception("Something Fooish")
    ... except Foo:
    ...     print "True"
    ... except Exception:
    ...     print "False"
    True

    Arguments:
        regex (string|RE): A regular expression which will be matched against
            the `.message` attribute of the exception raised. Note that it uses
            `re.search`, so if you want to match the beginning you have to
            explicitly anchor the string (using `\A` or `^`).

    Returns:
        Exception: (Actually: a new subclass of it), which checks the message
            of the exception against the supplied regex.
    """
    @instance_checking_exception
    def check_message(inst):
        return re.search(regex, inst.message)
    if classname is not None:
        check_message.__class__.__name__ = classname
    return check_message
