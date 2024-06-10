# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:50:38 2024

@author: ander
"""
import os
from typing import Optional

def create_output_dir(output_dir: str) -> Optional[None]:
    """
    Checks and creates the output folder if it does not exist.

    This function takes a folder path as a string. 
    If the folder does not exist, it is created.

    Args:
        output_dir (str): The path of the folder to be checked and created if necessary.

    Returns:
        Optional[None]: This function returns nothing.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)