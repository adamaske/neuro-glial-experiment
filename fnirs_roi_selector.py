import numpy as np

def extract_fnirs_channels(data, channel_names):
    """
    Extracts fNIRS channels and organizes them by source-detector pair and wavelength.

    Args:
        data (numpy.ndarray): A (102 x N) numpy array representing the fNIRS data,
                              where N is the length of the time series.
        channel_names (list of str): A list of channel names like 
                                     ["S1-D1 760", "S2-D1 760", ..., "S1-D1 850", "S2-D1 850", ...].

    Returns:
        dict: A dictionary where keys are source-detector pairs (e.g., "S1-D1") and
              values are dictionaries containing "760" (deoxy) and "850" (oxy) time series.
    """

    if data.shape[0] != len(channel_names):
        raise ValueError(f"Number of channels in data and channel_names must match {data.shape[0]} vs {len(channel_names)}")

    num_channels = len(channel_names)
    half_channels = num_channels // 2

    channel_dict = {}

    for i, channel_name in enumerate(channel_names):
        parts = channel_name.split()
        source_detector = parts[0]
        wavelength = parts[1]

        if source_detector not in channel_dict:
            channel_dict[source_detector] = {"760": None, "850": None}

        if wavelength == "760":
            channel_dict[source_detector]["760"] = data[i, :]
        elif wavelength == "850":
            channel_dict[source_detector]["850"] = data[i, :]
        else:
            raise ValueError(f"Unexpected wavelength: {wavelength}")

    return channel_dict

# Example usage:
# Assuming you have your data and channel_names loaded:

# Generate some dummy data for demonstration
num_time_points = 100
num_channels = 102
data = np.random.rand(num_channels, num_time_points)

# Generate dummy channel names
channel_names = []
num_source_detectors = num_channels // 2 // 2 #divide by 2 for oxy and deoxy, divide by 2 again because we are generating them
for i in range(1, num_source_detectors + 1):
    channel_names.append(f"S{i}-D1 760")
for i in range(1, num_source_detectors + 2):
    channel_names.append(f"S{i}-D2 760")
for i in range(1, num_source_detectors + 1):
    channel_names.append(f"S{i}-D1 850")
for i in range(1, num_source_detectors + 2):
    channel_names.append(f"S{i}-D2 850")

channel_dict = extract_fnirs_channels(data, channel_names)

# Example: Accessing the time series for "S1-D1"
if "S1-D1" in channel_dict:
    deoxy_s1_d1 = channel_dict["S1-D1"]["760"]
    oxy_s1_d1 = channel_dict["S1-D1"]["850"]
    print("S1-D1 deoxy time series:", deoxy_s1_d1)
    print("S1-D1 oxy time series:", oxy_s1_d1)
else:
    print("S1-D1 not found.")

if "S2-D2" in channel_dict:
    deoxy_s2_d2 = channel_dict["S2-D2"]["760"]
    oxy_s2_d2 = channel_dict["S2-D2"]["850"]
    print("S2-D2 deoxy time series:", deoxy_s2_d2)
    print("S2-D2 oxy time series:", oxy_s2_d2)
else:
    print("S2-D2 not found.")