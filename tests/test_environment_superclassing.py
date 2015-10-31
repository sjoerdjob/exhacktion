import errno
import os
import unittest

from exhacktion.environmenterror import FileNotFoundError


class TestEnvironmentSuperClassing(unittest.TestCase):
    def test_catching_enoent_from_open(self):
        try:
            open("/I/sure/hope/this/does/not.exist")
        except FileNotFoundError:
            pass
        except Exception as e:
            raise AssertionError("Could not create proper exception:" + str(e))

    def test_catching_enoent_from_remove(self):
        try:
            os.remove("/I/sure/hope/this/does/not.exist")
        except FileNotFoundError:
            pass
        except Exception as e:
            raise AssertionError("Could not create proper exception:" + str(e))

    def test_catching_non_enoent(self):
        try:
            os.listdir(__file__)
        except FileNotFoundError:
            raise AssertionError(
                "Opening `/` raised FileNotFoundError, should be ENOTDIR"
            )
            pass
        except OSError as e:
            assert e.errno == errno.ENOTDIR
