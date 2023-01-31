import random
import time
import socket

initial_energy = 15
global production_rate 
global consumption_rate 
global trade_policy 
MIN_TO_SELL = 10
MIN_TO_BUY = 5

# selling queue fonctionnelle mais problèmes ds le côté économique 

def home(id, selling_queue, current_temp, everybody_connected, full_simulation) :

    global trade_policy
    global production_rate
    global consumption_rate

    #print(f"Home PID : {multiprocessing.current_process().pid}")
    trade_policy = random.randint(1,3)
    production_rate = random.randint(1,5)
    consumption_rate = random.randint(1,5)

    HOST = "localhost"
    PORT = 1313
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        trade_policy_bytes = trade_policy.to_bytes(2, 'big')
        #print(f"My policy is number {trade_policy_bytes}")
        server_socket.sendall(trade_policy_bytes)

        # on s'assure que le serveur a bien reçu l'info avant d'envoyer la suite*
        while everybody_connected.value != True : 
            time.sleep(0.1)
        time.sleep(1)
        energy_gestion(id, server_socket, selling_queue, current_temp, full_simulation)



def energy_gestion(id, server_socket, selling_queue, current_temp, full_simulation) :

    global initial_energy 

    while current_temp.value != 10000 : 

        initial_energy = initial_energy - consumption_rate + production_rate

        # si on veut vendre
        if initial_energy >= MIN_TO_SELL : 
            if trade_policy == 1 :
                if full_simulation == True : 
                    print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : put {initial_energy-MIN_TO_BUY} energy in the queue")
                selling_queue.put([id, initial_energy-MIN_TO_BUY])
            elif trade_policy == 2 : 
                if full_simulation == True : 
                    print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : sold {initial_energy-MIN_TO_BUY} energy on the market") 
                server_socket.sendall("SELL".encode())
                server_socket.sendall((initial_energy-MIN_TO_BUY).to_bytes(2, 'big'))
            elif trade_policy == 3 :
                if full_simulation == True : 
                    print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : put {initial_energy-MIN_TO_BUY} energy in the queue")
                selling_queue.put([id, initial_energy-MIN_TO_BUY])
                time.sleep(2)
                if selling_queue.get()[0] == id : 
                    initial_energy = initial_energy + selling_queue.get()[1]
                    server_socket.sendall("SELL".encode())
                    server_socket.sendall((initial_energy-MIN_TO_BUY).to_bytes(2, 'big'))
                    if full_simulation == True : 
                        print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : got my energy back from the queue and sold it on the market")

            initial_energy = MIN_TO_BUY

        # si on est en rade d'énergie 
        if (initial_energy < MIN_TO_BUY) : 
            if selling_queue.empty() == False : 
                message = selling_queue.get()[1]
                if full_simulation == True : 
                    print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : got {message} energy from the queue")
                initial_energy = initial_energy + message
            else :      
                if full_simulation == True : 
                    print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : bought {MIN_TO_BUY} energy from the market") 
                initial_energy = initial_energy + MIN_TO_BUY
                server_socket.sendall("BUY".encode())
                server_socket.sendall(MIN_TO_BUY.to_bytes(2, 'big'))
        
        time.sleep(1)