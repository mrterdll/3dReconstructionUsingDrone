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
camera_client = airsim.MultirotorClient()

filename = ""
record_data = True

def camera_execute():
    print('Scanning Has Started\n')
    print('Use Keyboard Interrupt \'CTRL + C\' to Stop Scanning\n')
    existing_data_cleared = False   #change to true to superimpose new scans onto existing .asc files
    try:
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        thickness = 2
        textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
        print(textSize)
        textOrg = (10, 10 + textSize[1])
        frameCount = 0
        startTime = time.time()
        fps = 0
        filename = "grid_2_"
        count = 1000
        while record_data:

            # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
            rawImage = camera_client.simGetImage("high_res_bottom", airsim.ImageType.Scene)
            if (rawImage == None):
                print("Camera is not returning image, please check airsim for error messages")
                sys.exit(0)
            else:
                png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
                cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
                #cv2.imshow("Depth", png)
                #cv2.imshow("scene", png)
                
                with open (os.path.join("./testground/foto/",filename+str(count)+'.png'), "wb") as f:
                    f.write(bytes(airsim.string_to_uint8_array(rawImage)))
                
                #airsim.write_file(os.path.normpath("./foto/"+filename+str(count)+ '.png'), airsim.string_to_uint8_array(rawImage))
                count+=1
            frameCount = frameCount  + 1
            endTime = time.time()
            diff = endTime - startTime
            if (diff > 1):
                fps = frameCount
                frameCount = 0
                stardtTime = endTime

            key = cv2.waitKey(1) & 0xFF
            if (key == 27 or key == ord('q') or key == ord('x')):
                break
            #sleep for 8 seconds
            time.sleep(8)
    except KeyboardInterrupt:
        airsim.wait_key('Press any key to stop running this script')
        print("Done!\n")
    
    finally:
        return

def position():
    x_val = client.getMultirotorState().kinematics_estimated.position.x_val
    y_val = client.getMultirotorState().kinematics_estimated.position.y_val
    z_val = client.getMultirotorState().kinematics_estimated.position.z_val
    return x_val, y_val, z_val 

if __name__ == "__main__":
    filename = "grid_2_"

    cameraThread = Thread(target=camera_execute,daemon=True)
    client.confirmConnection()
    camera_client.confirmConnection()
    client.enableApiControl(False)
    client.enableApiControl(True)
    client.armDisarm(False)

    #airsim.wait_key('Kalkis icin bir tusa basiniz')
    client.armDisarm(True)
    client.takeoffAsync().join()
    client.moveToZAsync(client.getMultirotorState().kinematics_estimated.position.z_val + (-60), 5).join()
    time.sleep(3)

    #airsim.wait_key('Veri toplama ve ilerleme icin bir tusa basiniz')
    
    record_data = True
    cameraThread.start()
    
    xAxis = 80
    yAxis = 40
    numberOfLaps = 10
    speed = 2 
           
    x_pos, y_pos, z_pos =  position()

    x_start = x_pos
    y_start = y_pos

    printstr = f"starting point {x_start},{y_start}"
    print(printstr)

    for i in range(numberOfLaps):
        x_pos, y_pos, z_pos=  position()
        client.moveToPositionAsync(x_pos + xAxis, y_pos, z_pos, speed, drivetrain=DrivetrainType.MaxDegreeOfFreedom).join()
        x_pos, y_pos, z_pos =  position()
        client.moveToPositionAsync(x_pos, y_pos + yAxis, z_pos, speed, drivetrain=DrivetrainType.MaxDegreeOfFreedom).join()
        xAxis = -xAxis

    record_data = False

    client.moveToPositionAsync(x_start, y_start, z_pos ,2).join()    

    #airsim.wait_key("inis yapmak icin bir tusa basiniz")
    client.landAsync().join()
    client.enableApiControl(False)

    pass