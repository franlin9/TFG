#!/usr/bin/env python3
import time
import math
import sys

import torch
import torchvision
import traitlets
import numpy as np
import ipywidgets.widgets as widgets
from jetracer.nvidia_racecar import NvidiaRacecar
from torch2trt import TRTModule
from torch2trt import torch2trt
from jetcam.csi_camera import CSICamera
from utils import preprocess

car = NvidiaRacecar()

print("[SYSTEM] System starts up .... Please wait")

# use the TensorRT to faster inference
CATEGORIES = ['apex']

### When you got the TensorRT version weight, change to following code
model_trt = TRTModule()
model_trt.load_state_dict(torch.load('road_following_model_trt.pth'))

print("[OK] Finish to faster inference with TensorRT")

camera = CSICamera(width=224, height=224, capture_fps=65)

# front wheel setting
# car.steering_gain means the maximum rotation of front wheel
# car.steering_offset means the init shifting of front wheel

# back wheel setting
# car.throttle means the maximum speed of back wheel
# car.throttle_gain means the maximum limitation speed of back wheel

# Car parameter
car.throttle = 0.32
car.steering = 0
car.steering_offset = 0

# PID parameter
STEERING_GAIN = 1.7
STEERING_BIAS = 0.45

print ("Successful to load parameter")

#If the car wobbles left and right, lower the steering gain
#If the car misses turns, raise the steering gain
#If the car tends right, make the steering bias more negative (in small increments like -0.05)
#If the car tends left, make the steering bias more postive (in small increments +0.05)

while True:
    try:
        image = camera.read() #capture the images of the camera
        image = preprocess(image).half() #process the image
        output = model_trt(image).detach().cpu().numpy().flatten() #execute the image through of optimez model tensoRT, move the tensor to CPU in a numpy
        x = float(output[0]) # Extracts and converts the model output to a float number.
        pid_steering = x * STEERING_GAIN + STEERING_BIAS #Calculate the direction value using the proportional controller.
        print("[OUTPUT] AI-Output:{} PID-Steering:{}".format(x, pid_steering))
        car.steering = pid_steering
    except Exception as e:
        print("Error: ", e)
        car.throttle = 0  # Stop the car in case of error
