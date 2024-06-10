# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:55:42 2024

@author: ander
"""
import numpy as np
from calibration_functions.mean_bias_error import mean_bias_error
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import Union, List

def calculate_metrics(y_true: Union[np.ndarray, List[float]], 
                      y_pred: Union[np.ndarray, List[float]], 
                      label: str) -> None:
    """
    Calculates and displays evaluation metrics.

   This function calculates Root Mean Squared Error (RMSE), Mean Absolute Error (MAE),
   and Mean Bias Error (MBE) between observed and predicted values.
   The results are displayed with a given label.
   
    Args:
        y_true (Union[np.ndarray, List[float]]): observed values.
        y_pred (Union[np.ndarray, List[float]]): predicted values.
        label (str): The label to identify the displayed metrics.

    Returns:
        None: This function returns nothing.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mbe = mean_bias_error(y_true, y_pred)
    print(f"{label}:\nRMSE: {rmse:.2f}\nMAE: {mae:.2f}\nMBE: {mbe:.2f}\n")