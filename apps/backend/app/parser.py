from unittest import result

from pymavlink import mavutil

def parse_log(filepath):
    # Create a connection to the log file
    mav = mavutil.mavlink_connection(filepath)

    result = {}

    # Read messages from the log file
    while True:
        msg = mav.recv_match()
        if msg is None:
            break  # End of file
        # Process the message (for example, store it in a dictionary)

        msg_type = msg.get_type()

        result.setdefault(msg_type, []).append(msg.to_dict())

    return result

if __name__ == "__main__":  
    result = parse_log("../../logs/test.bin")  
    print(result.keys(  ))  # Print the types of messages found in the log file