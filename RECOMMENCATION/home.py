import random
import time
import socket

initial_energy = 15
production_rate = 2
consumption_rate = 3
trade_policy = 0
MIN_TO_SELL = 10
MIN_TO_BUY = 5
trade_policy = random.randint(1, 2)

# selling queue fonctionnelle mais problèmes ds le côté économique 

def home(id, selling_queue) :

    HOST = "localhost"
    PORT = 1313
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        trade_policy_bytes = trade_policy.to_bytes(2, 'big')
        server_socket.sendall(trade_policy_bytes)
        while(True) : 
            energy_gestion(id, server_socket, selling_queue)



def energy_gestion(id, server_socket, selling_queue) :
    global initial_energy 

    while True :

        initial_energy = initial_energy - consumption_rate + production_rate

        # si on veut vendre
        if initial_energy >= MIN_TO_SELL : 
            if trade_policy == 1 :
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : put {initial_energy-MIN_TO_BUY} enery in the queue")
                selling_queue.put(initial_energy-MIN_TO_BUY)
            elif trade_policy == 2 : 
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : sold {initial_energy-MIN_TO_BUY} energy on the market") 
                server_socket.sendall("SELL".encode())
                server_socket.sendall((initial_energy-MIN_TO_BUY).to_bytes(2, 'big'))
            initial_energy = MIN_TO_BUY

        # si on est en rade d'énergie 
        if (initial_energy < MIN_TO_BUY) : 
            if selling_queue.empty() == False : 
                message = selling_queue.get()
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : got {message} energy from the queue")
                initial_energy = initial_energy + message
            else :      
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : bought {MIN_TO_BUY} energy from the market") 
                initial_energy = initial_energy + MIN_TO_BUY
                server_socket.sendall("BUY".encode())
                server_socket.sendall(MIN_TO_BUY.to_bytes(2, 'big'))
        
        time.sleep(3)