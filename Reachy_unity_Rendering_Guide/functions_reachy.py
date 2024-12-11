
REACHY_JOI = {
    "r_shoulder_pitch": {"range": [-2.618, 1.57]},
    "r_shoulder_roll":  {"range": [-3.14, 0.174]},
    "r_arm_yaw":        {"range": [-1.57, 1.57]},
    "r_elbow_pitch":    {"range": [-2.182, 0]},
    "r_forearm_yaw":    {"range": [-1.745, 1.745]},
    "r_wrist_pitch":    {"range": [-0.785, 0.785]},
    "r_wrist_roll":     {"range": [-0.785, 0.785]},
    "l_shoulder_pitch": {"range": [-2.618, 1.57]},
    "l_shoulder_roll":  {"range": [-0.174, 3.14]},
    "l_arm_yaw":        {"range": [-1.57, 1.57]},
    "l_elbow_pitch":    {"range": [-2.182, 0]},
    "l_forearm_yaw":    {"range": [-1.745, 1.745]},
    "l_wrist_pitch":    {"range": [-0.785, 0.785]},
    "l_wrist_roll":     {"range": [-0.785, 0.785]},
    "neck_roll":        {"range": [-0.4, 0.4]},
    "neck_pitch":       {"range": [-0.4, 0.55]},
    "neck_yaw":         {"range": [-1.4, 1.4]},
}


def reset_reachy_to_mid_points():

    my_dict = REACHY_JOI
    keys = list(my_dict.keys())
    ranges = [my_dict[key]["range"] for key in keys]
    mid_values = [(mn + mx) / 2 for mn, mx in ranges]
    new_dict = {keys[j]: mid_values[j] for j in range(len(keys))}

    return new_dict


def reset_reachy_to_I_pose():
    my_dict = REACHY_JOI
    keys = list(my_dict.keys())
    new_dict = {keys[j]: 0 for j in range(len(keys))}

    return new_dict


def take_the_action(current_pose, joints_of_interest=None, decrease=False):
    my_dict = REACHY_JOI
    keys = list(my_dict.keys())
    ranges = [my_dict[key]["range"] for key in keys]
    increments = [(mx - mn) * 0.01 for mn, mx in ranges] # 0.05
    max_val = [mx for _, mx in ranges]
    min_val = [mn for mn, _ in ranges]

    # Default to all joints if none specified
    if joints_of_interest is None:
        joints_of_interest = keys

    if decrease == False:
        new_dict = {
            keys[j]: (
                min(current_pose[keys[j]] + increments[j], max_val[j])
                if keys[j] in joints_of_interest
                else current_pose[keys[j]]
            )
            for j in range(len(keys))
        }
    else:
        new_dict = {
            keys[j]: (
                max(current_pose[keys[j]] - increments[j], min_val[j])
                if keys[j] in joints_of_interest
                else current_pose[keys[j]]
            )
            for j in range(len(keys))
        }

    return new_dict

