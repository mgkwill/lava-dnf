# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import unittest

from lava.lib.dnf.operations.enums import ReduceMethod


class TestReduceMethod(unittest.TestCase):
    def test_validate_sum(self):
        """Tests whether SUM is a valid type of the ReduceMethod enum."""
        ReduceMethod.validate(ReduceMethod.SUM)

    def test_validate_mean(self):
        """Tests whether MEAN is a valid type of the ReduceMethod enum."""
        ReduceMethod.validate(ReduceMethod.MEAN)

    def test_invalid_type_raises_type_error(self):
        """Tests whether int is an invalid type of the ReduceMethod enum."""
        with self.assertRaises(TypeError):
            ReduceMethod.validate(int)

    def test_invalid_value_raises_value_error(self):
        """Tests whether FOO is an invalid value of the ReduceMethod enum."""
        with self.assertRaises(AttributeError):
            _ = ReduceMethod.FOO
