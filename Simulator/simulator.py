import pika.exceptions
import requests
import time
from datetime import datetime, timedelta
import multiprocessing
import random
import pika
import json
import threading


# CENTRAL_API = "https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/"
CENTRAL_API = "http://localhost:8000/"
RABBIT_SERVER, RABBIT_PORT = "4.248.248.109", 5672
EXCHANGE_NAME = "res_exchange"



class Spot():
    def __init__(self, id: str, floor_level: int, spot_number: int, status: str = "vacant"):
        self.id = id
        self.floor_level = floor_level
        self.spot_number = spot_number
        self.status = status
        
        self.reservations: list[dict] = []
        
        self.queue_name = f"Reservation_{self.id}"
        self.routing_key = f"spot_{self.id}"
        
        consumer_thread = threading.Thread(target=self.subscribeToResQueue, daemon=True)
        consumer_thread.start()
        
    
    def subscribeToResQueue(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVER, RABBIT_PORT))
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=self.queue_name, routing_key=self.routing_key)
        
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.process_reservation, auto_ack=True)

        try:
            print("Ready to consume messages")
            channel.start_consuming()
            
        except pika.exceptions.StreamLostError as sle:
            print(f"StreamLostError encountered in consumer thread: {sle}")
        except Exception as e:
            print(f"Unexpected error in consumer thread: {e}")
        finally:
            print("Stopping consumption")
            if channel.is_open:
                try:
                    channel.stop_consuming()
                except Exception as stop_e:
                    print(f"Error stopping consumer: {stop_e}")
            if channel.is_open:
                channel.close()
            if connection.is_open:
                connection.close()
        
        
    def process_reservation(self, channel, method, properties, body: bytes):
        """Handle message from server that a reservation was created"""
        
        print(f"Sim {self.id}: Got message:")
        message = json.loads(body.decode())
        print(message)
        
        #1. update internal status
        reservation = {
            "start_time": datetime.fromisoformat(message["start_time"]),
            "end_time": datetime.fromisoformat(message["end_time"])    
        }
        # print(f"Inserting reservation: {reservation}")
        
        #2. insert reservation to self.reservations
        self.reservations.append(reservation)
        
        #3. sort the dict
        self.reservations.sort(key=lambda x: x["start_time"])
        
        if self.pause_simulation.is_set():
            print("pause got set after procesing res")
            
    
    def start(self, stop_event):
        
        self.pause_simulation = threading.Event()
        
        
        simulation_thread = threading.Thread(target=self.simulation_loop)
        simulation_thread.daemon = True
        simulation_thread.start()
        
        while not stop_event.is_set():
            
            # print(f"In main while, reservations: {self.reservations}")
            
            if len(self.reservations) > 0 and (datetime.now() + timedelta(seconds=50)) >= self.reservations[0]["start_time"]:
                if self.pause_simulation.is_set():
                    print("inside if 1, pause is set")
                else:
                    print("inside if 1, pause is unset")
                print(datetime.now())
                print(self.reservations[0]["start_time"])
                print(datetime.now() >= self.reservations[0]["start_time"])
                self.status = 'reserved'
                self.update_API_status("reserved")
                time.sleep(49)
                
                
            if len(self.reservations) > 0 and datetime.now() >= self.reservations[0]["start_time"]:
                self.pause_simulation.set()
                print("just set")
                self.update_API_status("occupied")
                # Wait until the current reservation ends
                current_res = self.reservations[0]
                # print(current_res)
                while datetime.now() < current_res["end_time"]:
                    time.sleep(1)
                # Once finished, remove the reservation and resume simulation
                self.status = 'vacant'
                self.update_API_status("vacant")
                self.reservations.pop(0)
                self.pause_simulation.clear()
                print("just unset")
            else:
                time.sleep(1)  # Check periodically

                
                
    def simulation_loop(self):
        """Continuously simulate parking if not paused."""
        while True:
            # Check if we should pause the simulation due to an active reservation
            if self.pause_simulation.is_set():
                time.sleep(1)  # Simply wait while paused
                continue

            # Run one cycle of the parking simulation
            self.simulate_parking()
        
        
        
    def simulate_parking(self):
        """Randomly make the spot available and occupied"""
        sleep_time = random.randint(10, 40)
        time.sleep(sleep_time)
        if self.status == 'vacant':
            self.status = "occupied"
            self.update_API_status("occupied")
        sleep_time = random.randint(5, 20)
        time.sleep(sleep_time)
        if self.status == 'occupied':
            self.status = "vacant"
            self.update_API_status("vacant")
        sleep_time = random.randint(5, 20)
        time.sleep(sleep_time)
        
        
    def update_API_status(self, status: str):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        spot_status_changed_response = requests.put(CENTRAL_API + f"spots/{self.id}", json={"status": status}, headers=headers)
        spot = spot_status_changed_response.json()
        print(spot)
        
        
    def check_reservations(self):
        """Checks self.reservations to see if a reservation is currently active"""


def run_spot(spot_data, stop_event):
    new_spot = Spot(
        id=spot_data["_id"],
        floor_level=spot_data["floor_level"],
        spot_number=spot_data["spot_number"],
        status=spot_data["status"]
    )
    new_spot.start(stop_event)

if __name__ == '__main__':
    spots_response = requests.get(CENTRAL_API + "spots?filter=spot_number%3Aeq%3A1&filter=floor_level%3Aeq%3A0")
    spots = spots_response.json()['records']
    stop_event = multiprocessing.Event()
    processes = []

    for spot in spots:
        p = multiprocessing.Process(target=run_spot, args=(spot, stop_event))
        p.start()
        processes.append(p)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        for p in processes:
            p.join()