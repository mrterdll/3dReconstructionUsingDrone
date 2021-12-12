from airsim.types import YawMode
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
import math

# ip = "192.168.0.11"
# client = airsim.MultirotorClient(ip=ip)
# lidar_client = airsim.MultirotorClient(ip=ip)

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
        filename = "orbit_"
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
                cv2.imshow("scene", png)
                
                airsim.write_file(os.path.normpath("./foto/"+filename+str(count)+ '.png'), airsim.string_to_uint8_array(rawImage))
                count+=1
            frameCount = frameCount  + 1
            endTime = time.time()
            diff = endTime - startTime
            if (diff > 1):
                fps = frameCount
                frameCount = 0
                startTime = endTime

            key = cv2.waitKey(1) & 0xFF
            if (key == 27 or key == ord('q') or key == ord('x')):
                break
    except KeyboardInterrupt:
        airsim.wait_key('Press any key to stop running this script')
        print("Done!\n")
    
    finally:
        return

if __name__ == "__main__":
    filename = "orbit_test_1"
    #TODO: dronu yukseltecek kod yazilacak
    #TODO: dron donerken veri toplanip gorsellestirilecek
    #TODO: lidar veri miktari azaltilacak ve deneme yapilacak

    cameraThread = Thread(target=camera_execute,daemon=True)
    
    client.confirmConnection()
    camera_client.confirmConnection()
    client.enableApiControl(False)
    client.enableApiControl(True)
    client.armDisarm(False)
    
    airsim.wait_key('Kalkis icin bir tusa basiniz')
    client.armDisarm(True)
    client.takeoffAsync().join()


    airsim.wait_key('Yukselis icin bir tusa basiniz')
    
    client.moveToZAsync(-5, 1).join()
    client.hoverAsync().join()

    airsim.wait_key('Veri toplama ve yorunge icin bir tusa basiniz')
    record_data = True

    
    drone_posistion = client.getMultirotorState().kinematics_estimated.position
    current_altitude = drone_posistion.z_val
    

    w_val = client.getMultirotorState('Drone1').kinematics_estimated.orientation.w_val
    heading_degree = np.arccos(w_val) * 180 / 3.14159265359
    print(heading_degree)
        
    orbit_radius = 15
    center_point_x =  (np.cos(heading_degree) * orbit_radius) 
    center_point_y =  (np.sin(heading_degree) * orbit_radius)

    print(center_point_x )
    print(center_point_y )

    center_vector = [center_point_x,center_point_y]    
    
    #center_vector_y = client.getMultirotorState('Drone1').kinematics_estimated.orientation

    #nav = orbit.OrbitNavigator(client =client,radius=15,altitude=current_altitude, speed=3, iterations=1, center=[0,-1], snapshots=0)
    #print(current_altitude)

    #print(center_vector_y)
    

    nav = orbit.OrbitNavigator(client =client,radius=orbit_radius,altitude=current_altitude, speed=2, iterations=1, center = center_vector, snapshots=0)
    #Thread.start()
    nav.start_orbit()

    airsim.wait_key("inis yapmak icin bir tusa basiniz")
    record_data = False
    client.moveToZAsync(-1, 5).join()
    
    client.landAsync().join()
    #client.armDisarm(False)
    
    client.enableApiControl(False)

    pass