"""
Contains Python3-like EnvironmentError 'subclasses', except that it performs
a lot of under-the-hood magic to make it look like the standard library is
actually throwing these more specific versions instead of just OSError, IOError
and such.
"""

import errno

from exhacktion.base import instance_checking_exception


@instance_checking_exception
def BlockingIOError(inst):
    """I/O operation would block."""
    errnos = {errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK,
              errno.EINPROGRESS}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception
def BrokenPipeError(inst):
    """Broken pipe."""
    errnos = {errno.EPIPE, errno.ESHUTDOWN}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception
def ChildProcessError(inst):
    """Child process error."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECHILD


@instance_checking_exception
def ConnectionError(inst):
    """Connection error."""
    errnos = {errno.EPIPE, errno.ESHUTDOWN, errno.ECONNABORTED,
              errno.ECONNREFUSED, errno.ECONNRESET}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception
def ConnectionAbortedError(inst):
    """Connection aborted."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNABORTED


@instance_checking_exception
def ConnectionRefusedError(inst):
    """Connection refused."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNREFUSED


@instance_checking_exception
def ConnectionResetError(inst):
    """Connection reset."""
    return hasattr(inst, 'errno') and inst.errno == errno.ECONNRESET


@instance_checking_exception
def FileExistsError(inst):
    """File already exists."""
    return hasattr(inst, 'errno') and inst.errno == errno.EEXIST


@instance_checking_exception
def FileNotFoundError(inst):
    """File not found."""
    return hasattr(inst, 'errno') and inst.errno == errno.ENOENT


@instance_checking_exception
def InterruptedError(inst):
    """Interrupted by signal."""
    return hasattr(inst, 'errno') and inst.errno == errno.EINTR


@instance_checking_exception
def IsADirectoryError(inst):
    """Operatino doesn't work on directories."""
    return hasattr(inst, 'errno') and inst.errno == errno.EISDIR


@instance_checking_exception
def NotADirectoryError(inst):
    """Operation only works on directories."""
    return hasattr(inst, 'errno') and inst.errno == errno.ENOTDIR


@instance_checking_exception
def PermissionErrror(inst):
    """Not enough permissions."""
    errnos = {errno.EACCES, errno.EPERM}
    return hasattr(inst, 'errno') and inst.errno in errnos


@instance_checking_exception
def ProcessLookupError(inst):
    """Process not found."""
    return hasattr(inst, 'errno') and inst.errno == errno.ESRCH


@instance_checking_exception
def TimeoutError(inst):
    """Timeout expired."""
    return hasattr(inst, 'errno') and inst.errno == errno.ETIMEDOUT
