import numpy as np
import os, sys 
import re

# functions to get relative calibration factors
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_channel_order(text):
    channel_order_pattern = re.compile(r'P[ABCDEF][S][12]')
    match = channel_order_pattern.findall(text)
    if match:
        return match
    return []

def extract_calibration_data(text, channel_order):
    pattern = re.compile(r'PARAMETER_DOUBLE\s+P_RELATIVE_CALIBRATION\s+DETECTOR\s+(\d+)\s+=\s+([\d\s.]+)')
    matches = pattern.findall(text)
    
    calibration_data = {}
    
    for match in matches:
        detector_number = int(match[0])
        values = list(map(float, match[1].split()))
        calibration_data[detector_number] = dict(zip(channel_order, values))
    
    return calibration_data

def get_rel_calib(file_path): 
    """
    Finds relative calibration factors in a cdmsbats configuration file
    Parameters: 
        file_path: str, file path to config file.
    Returns: 
        dictionary of relative calibration factors for each detector. 
        Can access using get_rel_calib(file_path)[int(det_number)][str(channel)]
    """
    text = read_file(file_path)
    channel_order = extract_channel_order(text)
    if not channel_order:
        print("Channel order not found...")
        return
    
    calibration_data = extract_calibration_data(text, channel_order)
    return calibration_data