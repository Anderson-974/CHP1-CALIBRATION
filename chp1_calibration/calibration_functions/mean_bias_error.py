# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:52:22 2024

@author: ander
"""
import numpy as np
from typing import Union, List

def mean_bias_error(y_true: Union[np.ndarray, List[float]], y_pred: Union[np.ndarray, List[float]]) -> float:
    """
    Calculates the Mean Bias Error (MBE).

    This function takes two lists or numpy tables of observed (y_true),
    and predicted (y_pred) values as input, and returns the Mean Bias Error, 
    which is the average of the differences between predicted and observed values.

    Args:
        y_true (Union[np.ndarray, List[float]]): observed values.
        y_pred (Union[np.ndarray, List[float]]): predicted values.

    Returns:
        float: Mean Bias Error between predicted and observed values.
    """
    return np.mean(np.array(y_pred) - np.array(y_true))