import requests
import time
from datetime import datetime, timedelta
import multiprocessing

CENTRAL_API = "https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/"

def simulate_parking(spot, stop_event):       
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
    }
    while not stop_event.is_set():
        reservations_response = requests.get(CENTRAL_API + "reservations")
        reservations = reservations_response.json()['records']
        for reservation in reservations:
            if reservation['spot_id'] == spot['_id']:
                current_time = datetime.now()
                start_time = reservation['start_time']
                end_time = reservation['end_time']
                if str(current_time + timedelta(seconds=10)) >= start_time:
                    requests.put(CENTRAL_API + f"spots/{spot['_id']}", json={"status": "vacant"}, headers=headers)
                    time.sleep(1)
                while start_time <= str(datetime.now()) < end_time:
                    requests.put(CENTRAL_API + f"spots/{spot['_id']}", json={"status": "reserved"}, headers=headers)
                    time.sleep(30)

        if spot['status'] == 'vacant':
            status_changed_response = requests.put(CENTRAL_API + f"spots/{spot['_id']}", json={"status": "occupied"}, headers=headers)
            print(status_changed_response.json())
            time.sleep(30)
        if spot['status'] == 'occupied':
            status_changed_response = requests.put(CENTRAL_API + f"spots/{spot['_id']}", json={"status": "vacant"}, headers=headers)
            print(status_changed_response.json())
        time.sleep(30)


if __name__ == '__main__':
    spots_response = requests.get(CENTRAL_API + "spots")
    spots = spots_response.json()['records']
    stop_event = multiprocessing.Event()
    num_processes = len(spots)
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=simulate_parking, args=(spots[i], stop_event))
        p.start()
        processes.append(p)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        for p in processes:
            p.join()

