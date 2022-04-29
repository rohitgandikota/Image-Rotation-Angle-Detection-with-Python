# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 15:32:37 2022

@author: Rohit Gandikota
"""

import numpy as np
import cv2
import math
from scipy import ndimage
import gdal
import glob
import os


def getAngleofRotation(path, return_images=False, img_list=[], debug=False):
    '''
    Returns the angle the georeferenced image is rotated by
    
        Parameters:
            path (str): Path where the image is present
            return_images (bool) [Optional]: The flag to return the rotated image back
            img_list (List) [Optional]: Images list of which the rotation has to be performed on. (Should be absolute path only. Full path)
            debug (bool) [Optional]: Will return the lines drawn on the image if true
            
        Returns:
            median_angle (float): Float value of the angle by which the image is rotated by
            out_list (List) [Conditional]: List of all rotated images as per input `img_list`. Conditional of `return_images`.
            debug_img (ndarray) [Conditional]: Image with lines drawn on the jpg. Conditional on `debug` flag.
            
    '''
    # Finding image
    img_path = glob.glob(os.path.join(path,'*.jpg'))[0]
    if not os.path.exists(img_path):
        return 0
    
    # Reading image and converting to gray scale
    img_before = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    img_gray[img_gray>0] = 255
    # Using edge filtering to bring out sharp features and lines in the image
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    # Detecting lined using Hough Transform
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=20, maxLineGap=5)
    
    # Finding angles using slope formula tan(θ) = (y2-y1)/(x2-x1)
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    
    # The algorithm will detect multiple lines and edges. We take the median of all angles
    median_angle = np.median(angles)+90
    
    if debug:
        return angle, img_before
    # If return_images is True, rotate the images and return the list
    out_list = []
    if return_images:
        for img in img_list:
            try:
                # Read the image
                try:
                    # If tif file
                    tif = gdal.Open(img).ReadAsArray()
                except Exception:
                    # If PNG or jpg
                    tif = cv2.imread(img_path)
                # Rotating the image
                tif_rotated = ndimage.rotate(tif, median_angle)
                out_list.append(tif_rotated)           
            except Exception as e:
                print(f'Error in rotating images! : {e}')
                
        return median_angle, out_list
    
    return median_angle

if __name__=='__main__':
    import matplotlib.pyplot as plt
    path = 'D:\\Projects\\PQC\\RadQA\\213627031'
    path = 'D:\\Projects\\DLIP\\RadQA\\data\\211361111'
    tif_files = glob.glob(os.path.join(path,'*.tif'))
    angle, outlist = getAngleofRotation(path, return_images=True, img_list=[tif_files[0]])
    print(f"Angle is {angle:.04f}")
    
