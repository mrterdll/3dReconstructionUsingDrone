import cv2
from airsim import MultirotorClient as cameraClient
import airsim
import sys
import time
import os
from threading import Thread

class cameraRecorder:
    def __init__(self,camera_client:cameraClient,record_file_prefix:str,debug_mode:bool,image_display:bool,sleep_time:float):
        self.camera_client = camera_client
        self.record_file_prefix = record_file_prefix
        self.debug_mode = debug_mode
        self.record_mode = False
        self.image_display = image_display
        self.sleep_time = sleep_time


    def camera_execute_function(self):
        
        if(self.debug_mode):
            print('Scanning Has Started\n')
        try:
            if(self.image_display):
                fontFace = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.5
                thickness = 2
                textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
                if(self.debug_mode):
                    print(textSize)
                textOrg = (10, 10 + textSize[1])
                frameCount = 0
                startTime = time.time()
                fps = 0
            
            filename = "grid_1_"
            count = 0
            while self.record_data:
                # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
                rawImage = self.camera_client.simGetImage("high_res_bottom", airsim.ImageType.Scene)
                if (rawImage == None):
                    print("Camera is not returning image, please check airsim for error messages")
                    sys.exit(0)
                else:
                    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
                    if(self.image_display):
                        cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
                        cv2.imshow("scene", png)
                    
                    airsim.write_file(os.path.normpath("./foto/"+filename+str(count)+ '.png'), airsim.string_to_uint8_array(rawImage))
                    count+=1
                if(self.image_display):
                    frameCount = frameCount  + 1
                    endTime = time.time()
                    diff = endTime - startTime
                    if (diff > 1):
                        fps = frameCount
                        frameCount = 0
                        startTime = endTime
                time.sleep(self.sleep_time)
        except KeyboardInterrupt:
            print("\n\nProgram Ended")
        
        finally:
            return
    
    def start_recording(self):
        self.record_data = True
        self.camera_thread = Thread(target=self.camera_execute_function,daemon=True)
        self.camera_thread.start()
        return self.camera_thread
    
    def stop_recording(self):
        self.record_data = False
        self.camera_thread.join()