from matplotlib import pyplot as plt
import numpy as np
import pathlib

def get_phish_data():
    files = [f for f in pathlib.Path().glob("parse/*")]
    total_time = np.array([])
    total_traffic = np.array([])
    for filename in files:
        time_duration, traffic_length = np.loadtxt(str(filename), delimiter=',', skiprows=1, unpack=True)
        total_time = np.concatenate((total_time, time_duration), axis=0)
        total_traffic = np.concatenate((total_traffic, traffic_length), axis=0)
    
    return total_time, total_traffic
            
          
def get_benign_data():
    idx = 0
    files = [f for f in pathlib.Path().glob("benign/parse/*")]
    total_time = np.array([])
    total_traffic = np.array([])
    for filename in files:
        time_duration, traffic_length = np.loadtxt(str(filename), delimiter=',', skiprows=1, unpack=True)
        for i in range(len(time_duration) - 1):
            if time_duration[i+1] - time_duration[i] > 1:
                total_time = np.concatenate((total_time, time_duration[:i+1]), axis=0)
                total_traffic = np.concatenate((total_traffic, traffic_length[:i+1]), axis=0)
                break
        idx = idx + 1
        if idx == 500:
            break
    return total_time, total_traffic

if __name__ == '__main__':
    phishing_x, phishing_y = get_phish_data()
    benign_x, benign_y = get_benign_data()
    plt.scatter(phishing_x, phishing_y, s=2, color='r')
    #plt.scatter(benign_x, benign_y, s=2, color='b')
    plt.xlabel('Time')
    plt.ylabel('Packet Size')
    plt.legend()
    plt.show()

#

