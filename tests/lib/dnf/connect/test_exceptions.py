# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import unittest

from lib.dnf.connect.exceptions import MissingOpError, DuplicateOpError


class TestMissingOpError(unittest.TestCase):
    def test_raising_missing_op_error(self):
        """Tests whether the MissingOpError can be raised and its attribute
        is set correctly."""
        missing_op = "test"
        # check whether the exception is raised
        with self.assertRaises(MissingOpError) as context:
            raise MissingOpError(missing_op)

        # check whether the missing_op attribute is set
        self.assertEqual(context.exception.missing_op, missing_op)

        # check whether the default message is set
        self.assertTrue(context.exception.args[0] is not None)


class TestDuplicateOpError(unittest.TestCase):
    def test_raising_duplicate_op_error(self):
        """Tests whether the DuplicateOpError can be raised and its attribute
        is set correctly."""
        duplicate_op = "test"
        # check whether the exception is raised
        with self.assertRaises(DuplicateOpError) as context:
            raise DuplicateOpError(duplicate_op)

        # check whether the duplicate_op attribute is set
        self.assertEqual(context.exception.duplicate_op, duplicate_op)

        # check whether the default message is set
        self.assertTrue(context.exception.args[0] is not None)


if __name__ == '__main__':
    unittest.main()