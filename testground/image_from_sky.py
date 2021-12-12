import setup_path
import airsim
import numpy as np
from threading import Thread
import time
from navigator import orbit
import cv2
import os
import tempfile
import sys

client = airsim.MultirotorClient()
camera_client = airsim.MultirotorClient()

filename = ""
record_data = False

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
        filename = "manuel_ucus_1_"
        count = 0
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
                
                airsim.write_file(os.path.normpath("./foto/"+filename+str(count)+ '.png'), airsim.string_to_uint8_array(rawImage))
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
            #sleep for .05 seconds
            #time.sleep(2)
    except KeyboardInterrupt:
        airsim.wait_key('Press any key to stop running this script')
        print("Done!\n")
    
    finally:
        return

if __name__ == "__main__":
    filename = "manuel_ucus_1_"

    lidarThread = Thread(target=camera_execute,daemon=True)
    
#    client.confirmConnection()
    camera_client.confirmConnection()
#        client.enableApiControl(False)
 #       client.enableApiControl(True)
  #      client.armDisarm(False)

    airsim.wait_key('Kalkis icin bir tusa basiniz')
#    client.armDisarm(True)
#   client.takeoffAsync().join()

    airsim.wait_key('Veri toplama ve ilerleme icin bir tusa basiniz')
    time.sleep(3)
#   client.moveToZAsync(client.getMultirotorState().kinematics_estimated.position.z_val + (-15), 5).join()
    record_data = True
    lidarThread.start()

    time.sleep(60)
#    x_pos =  client.getMultirotorState().kinematics_estimated.position.x_val
#    y_pos =  client.getMultirotorState().kinematics_estimated.position.y_val
#    z_pos = client.getMultirotorState().kinematics_estimated.position.z_val

#   client.moveToPositionAsync( x_pos , y_pos + 20, z_pos, 2).join()
    record_data = False
#   client.moveToPositionAsync( x_pos, y_pos, z_pos, 2).join()
#   client.hoverAsync().join()

    #airsim.wait_key("inis yapmak icin bir tusa basiniz")
#   client.moveToZAsync(-1, 5).join()
#   client.landAsync().join()
    #client.armDisarm(False)
    
    client.enableApiControl(False)

    pass