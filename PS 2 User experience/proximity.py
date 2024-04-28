from geopy.distance import geodesic
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import bluetooth
from wifi import Cell, Scheme

cred = credentials.Certificate("path_to_your_firebase_credentials.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'your_firebase_database_url'  
})

def get_gps_coordinates():
    latitude = 0.0
    longitude = 0.0
    return latitude, longitude

def get_bluetooth_devices():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    return nearby_devices

def get_wifi_devices():
    wifi_networks = Cell.all('wlan0')
    return wifi_networks

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters 

def main():
    counter = 0
    start_time = None
    total_proximity_duration = 0

    while True:
        device1_coords = get_gps_coordinates()
        device2_coords = get_gps_coordinates()

        bluetooth_devices = get_bluetooth_devices()
        bluetooth_proximity = False
        for addr, name in bluetooth_devices:
            if addr == 'bluetooth_mac_address_of_device_2':
                bluetooth_proximity = True
                break

        wifi_devices = get_wifi_devices()
        wifi_proximity = False
        for wifi_network in wifi_devices:
            if wifi_network.ssid == 'wifi_network_name_of_device_2':
                wifi_proximity = True
                break

        distance = calculate_distance(device1_coords, device2_coords)

        proximity_threshold = 1.0 
        if distance < proximity_threshold or bluetooth_proximity or wifi_proximity:
            if start_time is None:
                start_time = time.time()
                counter += 1
        else:
            if start_time is not None:
                end_time = time.time()
                duration = end_time - start_time
                total_proximity_duration += duration
                print(f"Devices were in proximity for {duration} seconds.")
                start_time = None

                update_database(duration)

        time.sleep(1)

def update_database(duration):
    ref = db.reference('/proximity_duration')
    ref.push(duration)

if __name__ == "__main__":
    main()

