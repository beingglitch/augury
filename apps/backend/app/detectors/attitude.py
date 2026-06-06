def detect_attitude_changes(log_data):
    attitude_changes = []
    
    # Check if ATTITUDE messages are present in the log data
    if 'ATT' not in log_data:
        return attitude_changes  # No attitude data to analyze
        
    for msg in log_data['ATT']:

        if msg is not None:
            # Calculate the difference in attitude
            roll_diff = abs(msg["DesRoll"] - msg["Roll"])
            pitch_diff = abs(msg["DesPitch"] - msg["Pitch"])
            yaw_diff = abs(msg["DesYaw"] - msg["Yaw"])
            
            if yaw_diff > 180:
                yaw_diff = 360 - yaw_diff

            # Define a threshold for significant attitude change (example: 10 degrees)
            threshold = 5
            
            if roll_diff > threshold or pitch_diff > threshold or yaw_diff > threshold:
                attitude_changes.append({
                    'time': msg['TimeUS'],
                    'roll_diff': roll_diff,
                    'pitch_diff': pitch_diff,
                    'yaw_diff': yaw_diff
                })
            
            if len(attitude_changes) != 0:
                return { "detection": True, "description": { "max_roll": max(diff["roll_diff"] for diff in attitude_changes), "max_pitch": max(diff["pitch_diff"] for diff in attitude_changes), "max_yaw": max(diff["yaw_diff"] for diff in attitude_changes) } }

            return { "detection": False, "description": "No significant attitude changes detected." }
