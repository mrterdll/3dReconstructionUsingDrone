from airsim.types import DrivetrainType
import setup_path
import airsim
import time
import cv2
import sys
import os
import tempfile
import numpy as np
from navigator import orbit
from threading import Thread

client = airsim.MultirotorClient()


if __name__ == "__main__":

    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    client.enableApiControl(False)

pass