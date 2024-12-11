import pickle
from tqdm import tqdm
from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time
import socket
from scipy.signal import savgol_filter
from functions_reachy import reset_reachy_to_I_pose


### Window path

## Drinking soda motion
#file_path = r"C:\Users\user\Desktop\Reachy_unity_Rendering_Guide\predicted_motions\pred_REACHY_ex_13_08.pkl" 

## Drinking soda key poses (old/longer version)
file_path = r"C:\Users\user\Desktop\Reachy_unity_Rendering_Guide\predicted_motions\one_stage_predicted_soda_key_poses_old_version.pkl" 





def send_message_to_unity(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8052))
    client_socket.sendall(message.encode())
    client_socket.close()



with open(file_path, 'rb') as file:
    motion_data = pickle.load(file)
    

print("Number of poses: ", len(motion_data))
print("Number of joints: ", len(motion_data[0]))
print("Name of joints: ", list(motion_data[0].keys()))

# Function to convert pose radians to degrees, including wrists and neck
def convert_pose_to_degrees(pose):
    return {
        'r_shoulder_pitch': float(np.degrees(pose['r_shoulder_pitch'])),
        'r_shoulder_roll': float(np.degrees(pose['r_shoulder_roll'])),
        'r_arm_yaw': float(np.degrees(pose['r_arm_yaw'])),
        'r_elbow_pitch': float(np.degrees(pose['r_elbow_pitch'])),
        'r_forearm_yaw': float(np.degrees(pose['r_forearm_yaw'])),
        'r_wrist_pitch': float(np.degrees(pose['r_wrist_pitch'])),
        'r_wrist_roll': float(np.degrees(pose['r_wrist_roll'])),
        
        'l_shoulder_pitch': float(np.degrees(pose['l_shoulder_pitch'])),
        'l_shoulder_roll': float(np.degrees(pose['l_shoulder_roll'])),
        'l_arm_yaw': float(np.degrees(pose['l_arm_yaw'])),
        'l_elbow_pitch': float(np.degrees(pose['l_elbow_pitch'])),
        'l_forearm_yaw': float(np.degrees(pose['l_forearm_yaw'])),
        'l_wrist_pitch': float(np.degrees(pose['l_wrist_pitch'])),
        'l_wrist_roll': float(np.degrees(pose['l_wrist_roll'])),
        
        'neck_roll': float(np.degrees(pose['neck_roll'])),
        'neck_pitch': float(np.degrees(pose['neck_pitch'])),
        'neck_yaw': float(np.degrees(pose['neck_yaw'])),
    }

# Convert all poses in motion_data from radians to degrees
motion_data_degrees = [convert_pose_to_degrees(pose) for pose in tqdm(motion_data, desc="Converting Poses to Degrees")]


joint_keys = motion_data[0].keys()

### Apply smoothing filtering (Comment when unnecessary)

print("median filtering....")
for ki, k in enumerate(joint_keys):
    values = np.array([th[k] for th in motion_data_degrees])
    #print(values.shape)
    values = savgol_filter(values, 25, 2)
    # print(values.shape)
    for thi, th in enumerate(motion_data_degrees):
        th[k] = values[thi]
        # angles[thi] = th
print("filtering done")


# Now use the converted data in your loop to set goal positions
def get_pose(pose, reachy):
    try:
        current_pose = {
            reachy.r_arm.r_shoulder_pitch: pose['r_shoulder_pitch'],
            reachy.r_arm.r_shoulder_roll: pose['r_shoulder_roll'],
            reachy.r_arm.r_arm_yaw: pose['r_arm_yaw'],
            reachy.r_arm.r_elbow_pitch: pose['r_elbow_pitch'],
            reachy.r_arm.r_forearm_yaw: pose['r_forearm_yaw'],
            reachy.r_arm.r_wrist_pitch: pose['r_wrist_pitch'],
            reachy.r_arm.r_wrist_roll: pose['r_wrist_roll'],

            
            reachy.l_arm.l_shoulder_pitch: pose['l_shoulder_pitch'],
            reachy.l_arm.l_shoulder_roll: pose['l_shoulder_roll'],
            reachy.l_arm.l_arm_yaw: pose['l_arm_yaw'],
            reachy.l_arm.l_elbow_pitch: pose['l_elbow_pitch'],
            reachy.l_arm.l_forearm_yaw: pose['l_forearm_yaw'],
            reachy.l_arm.l_wrist_pitch: pose['l_wrist_pitch'],
            reachy.l_arm.l_wrist_roll: pose['l_wrist_roll'],


            reachy.head.neck_roll: pose['neck_roll'],
            reachy.head.neck_pitch:  pose['neck_pitch'],
            reachy.head.neck_yaw: pose['neck_yaw'],
        }
        return current_pose
    except AttributeError:
        pass


reachy = ReachySDK(host='localhost')

start_time = time.time()

index_for_image = 0

for pose in tqdm(motion_data_degrees, desc="Processing Poses"):
    
    ## Uncomment below only for non consecutive poses (needed for calibration)

    # reset_pose_degrees = convert_pose_to_degrees(reset_reachy_to_I_pose())
    # #print(reset_pose_degrees)
    # reset_position = get_pose(reset_pose_degrees,reachy)
    # goto(
    # goal_positions = reset_position,
    # duration = 0.1)
    # time.sleep(0.5) 

    current_pose = get_pose(pose, reachy)
    goto(
    goal_positions = current_pose,
    duration = 0.1)
    time.sleep(1)

    current_pose = get_pose(pose, reachy)
    goto(
    goal_positions = current_pose,
    duration = 0.1)

    time.sleep(0.5)   

    capture_message = f"capture_one_{index_for_image:03d}"
    send_message_to_unity(capture_message)

    time.sleep(0.5)   
    index_for_image+=1
    
end_time = time.time()
elapse_time = (end_time - start_time)//60 
print("\n")
print(f"Time take: {int(elapse_time)} min")



