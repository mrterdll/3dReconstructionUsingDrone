import setup_path
import airsim
import numpy as np
from threading import Thread
import time
from navigator import orbit

client = airsim.MultirotorClient()
lidar_client = airsim.MultirotorClient()

filename = ""
record_data = False

def lidar_execute():
    print('Scanning Has Started\n')
    print('Use Keyboard Interrupt \'CTRL + C\' to Stop Scanning\n')
    existing_data_cleared = False   #change to true to superimpose new scans onto existing .asc files
    try:
        while record_data:
            
            file_name_with_ext = f"{filename}.asc"
            if not existing_data_cleared:
                f = open(file_name_with_ext,'w')
            else:
                f = open(file_name_with_ext,'a')
            lidar_data =lidar_client.getLidarData(vehicle_name='Drone1',lidar_name='LidarSensor1')
                    
            orientation = lidar_data.pose.orientation
            q0, q1, q2, q3 = orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val
            rotation_matrix = np.array(([1-2*(q2*q2+q3*q3),2*(q1*q2-q3*q0),2*(q1*q3+q2*q0)],
                                        [2*(q1*q2+q3*q0),1-2*(q1*q1+q3*q3),2*(q2*q3-q1*q0)],
                                        [2*(q1*q3-q2*q0),2*(q2*q3+q1*q0),1-2*(q1*q1+q2*q2)]))

            position = lidar_data.pose.position
            for i in range(0, len(lidar_data.point_cloud), 3):
                xyz = lidar_data.point_cloud[i:i+3]

                corrected_x, corrected_y, corrected_z = np.matmul(rotation_matrix, np.asarray(xyz))
                final_x = corrected_x + position.x_val
                final_y = corrected_y + position.y_val
                final_z = corrected_z + position.z_val

                f.write("%f %f %f\n" % (final_x,final_y,final_z))
            f.close()
            #time.sleep(0.2)
            existing_data_cleared = True
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
    nav = orbit.OrbitNavigator(radius=2,altitude=10, speed=3, iterations=3, center=[-1,0], snapshots=0)
    lidarThread = Thread(target=lidar_execute,daemon=True)
    
    client.confirmConnection()
    lidar_client.confirmConnection()
    client.enableApiControl(False)
    client.enableApiControl(True)
    client.armDisarm(False)
    
    airsim.wait_key('Kalkis icin bir tusa basiniz')
    client.armDisarm(True)
    client.takeoffAsync().join()


    airsim.wait_key('Yukselis icin bir tusa basiniz')
    
    client.moveToZAsync(-10, 1).join()
    client.hoverAsync().join()

    airsim.wait_key('Veri toplama ve yorunge icin bir tusa basiniz')
    record_data = True
    lidarThread.start()
    nav.start_orbit()

    airsim.wait_key("inis yapmak icin bir tusa basiniz")
    client.moveToZAsync(-1, 1).join()
    client.landAsync().join()
    client.armDisarm(False)
    record_data = False
    client.enableApiControl(False)

    pass