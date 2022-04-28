# Image-Rotation-Angle-Detection-with-Python
This code can be used for finding the angle that the image has been rotated by. Especially is tested on satellite data where geo-referencing rotates the image.

`angle, rotated_list = getAngleofRotation(path, return_images=True, img_list=['<path>/img1.tif','<path>/img2.tif','<path>/img3.tif'])` can be used to find the angle and rotate the image back to the straights.

If only angle is what one needs to find and save processing time and memory space:
`angle = getAngleofRotation(path, return_images=False)` will only compute the angle and return the float value
