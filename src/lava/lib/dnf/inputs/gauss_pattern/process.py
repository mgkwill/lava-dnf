# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import numpy as np
import typing as ty

from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.process.ports.ports import OutPort


class GaussPattern(AbstractProcess):
    """
    Gauss pattern generator Process.

    This process generates Gauss patterns and send them through
    the OutPort a_out.
    It recomputes new patterns and sends them asynchronously only when one of
    the parameters amplitude, mean or stddev changes.

    Parameters:
    -----------
    shape: tuple(int)
        number of neurons per dimension, e.g. shape=(30, 40)
    amplitude: float
        amplitude of the Gauss pattern
    mean: list(float) or float
        mean of the Gauss pattern
    stddev: list(float) or float
        standard deviation of the Gauss pattern
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        shape = kwargs.pop("shape")
        amplitude = kwargs.pop("amplitude")
        mean = self._validate_param(np.array(shape),
                                    "mean",
                                    kwargs.pop("mean"))
        stddev = self._validate_param(np.array(shape),
                                      "stddev",
                                      kwargs.pop("stddev"))

        self._shape = Var(shape=(len(shape),), init=np.array(shape))

        self._amplitude = Var(shape=(1,), init=np.array([amplitude]))
        self._mean = Var(shape=(len(shape),), init=mean)
        self._stddev = Var(shape=(len(shape),), init=stddev)

        self.pattern = Var(shape=shape, init=np.zeros(shape))

        self.changed = Var(shape=(1,), init=np.array([True]))

        self.a_out = OutPort(shape=shape)

    def _validate_param(self,
                        shape: np.ndarray,
                        param_name: str,
                        param: ty.Union[float, ty.List[float]]):
        """Validates that parameter param with name param_name is either
        a float value or a list of floats of the same length as the
        dimensionality of the given shape.

        Returns param as ndarray.

        Parameters
        ----------
        shape : numpy.ndarray
            shape of the pattern
        param_name : str
            name of the parameter (either mean or stddev)
        param : list(float) or float
            parameter of the pattern

        Returns
        -------
        param : numpy.ndarray

        """
        # If param is a float (or int)
        if isinstance(param, float) or isinstance(param, int):
            # Cast param to float
            param = float(param)
            # Create a list with single element
            param = [param]

        # If param is of length 1, no validation against shape
        if len(param) == 1:
            param_val = param[0]
            # Broadcast param value to a list of length equal to shape
            # dimensionality
            param = [param_val for _ in range(shape.shape[0])]
        # Else, if param is of length > 1
        elif len(param) > 1:
            # Validate that the length is equal to shape dimensionality
            if len(param) != shape.shape[0]:
                raise ValueError(
                    f"<{param_name}> parameter has length different "
                    "from shape dimensionality")
        else:
            raise ValueError(f"<{param_name}> parameter cannot be empty")

        return np.array(param)

    def _update(self):
        """Set the value of the changed flag Var to True"""
        self.changed.set(np.array([True]))

    @property
    def shape(self) -> np.ndarray:
        """Get value of the shape Var

        Returns
        -------
        shape : numpy.ndarray
        """
        try:
            return self._shape.get()
        except AttributeError:
            return None

    @property
    def amplitude(self) -> np.ndarray:
        """Get value of the amplitude Var

        Returns
        -------
        amplitude : numpy.ndarray
        """
        try:
            return self._amplitude.get()
        except AttributeError:
            return None

    @amplitude.setter
    def amplitude(self, amplitude: float):
        """Set the value of the amplitude Var and updates the changed flag"""
        self._amplitude.set(np.array([amplitude]))
        self._update()

    @property
    def mean(self) -> np.ndarray:
        """Get value of the mean Var

        Returns
        -------
        mean : numpy.ndarray
        """
        try:
            return self._mean.get()
        except AttributeError:
            return None

    @mean.setter
    def mean(self, mean: ty.Union[float, ty.List[float]]):
        """Set the value of the mean Var and updates the changed flag"""
        mean = self._validate_param(self.shape, "mean", mean)
        self._mean.set(mean)
        self._update()

    @property
    def stddev(self) -> np.ndarray:
        """Get value of the stddev Var

        Returns
        -------
        stddev : numpy.ndarray
        """
        try:
            return self._stddev.get()
        except AttributeError:
            return None

    @stddev.setter
    def stddev(self, stddev: ty.Union[float, ty.List[float]]):
        """Set the value of the stddev Var and updates the changed flag"""
        stddev = self._validate_param(self.shape, "stddev", stddev)
        self._stddev.set(stddev)
        self._update()
