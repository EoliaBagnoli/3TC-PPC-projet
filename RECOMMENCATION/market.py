import multiprocessing
import threading
from external import *
import signal
import socket
import struct
from string import printable

global energy_price
global NUM_HOUSES
global full_sim
global internal_event
global external_event 
lock = threading.Lock()

def newPrice(current_temp, everybody_connected) :

    while everybody_connected.value != True : 
        time.sleep(0.1)

    atenuation_coeff = 0.99
    modulating_coeff_int = 0.001
    modulating_coeff_ext = 0.01
    modulating_coeff_buy = 0.2
    modulating_coeff_sell = 0.1

    global energy_price
    energy_price = 10
    global internal_event
    internal_event = False
    global external_event
    external_event = False

    while current_temp.value != 10000 :
        if (external_event) :
            if internal_event :
                energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp.value + modulating_coeff_ext + modulating_coeff_buy
            else :
                energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp.value + modulating_coeff_ext - modulating_coeff_sell
        else :
            if internal_event :
                energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp.value + modulating_coeff_buy
            else : 
                energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp.value - modulating_coeff_sell
        energy_price = 0.1 if energy_price < 0.1 else energy_price
        print(f"The price of the energy is : <{round(energy_price, 4)} €> right now")
        time.sleep(1)

def handler (sig, frame) : 

    global socket_pid
    global external_pid
    global external_event

    if sig == signal.SIGCHLD : 
        print(" ")
        print("HURRICANE HAPPENING")
        print(" ")
        external_event = True
    elif sig == signal.SIGUSR1 : 
        print(" ")
        print("PUTIN INVADES UKRAINE (again)")
        print(" ")
        external_event = True
    elif sig == signal.SIGUSR2 : 
        print(" ")
        print("FUEL SHORTAGE HAPPENING")
        print(" ")
        external_event = True

    # here : to make sure that every process is killed 
    elif sig == signal.SIGINT : 
        print(" ")
        print(" ")
        print("KILLING ALL THE PROCESSES :")
        print(" ")
        print(" ")
        active = multiprocessing.active_children()
        for child in active:
            print(f"killing : {child}")
            child.kill()
        os.kill(multiprocessing.parent_process().pid, signal.SIGINT)
        os.kill(multiprocessing.current_process().pid, signal.SIGKILL)

def socket_creation(current_temp, everybody_connected) : 

    #print(f"Socket PID : {multiprocessing.current_process().pid}")

    #print("Creating the socket")
    HOST = "localhost"
    PORT = 1313

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        number_of_connections = 0
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

        sockets = [threading.Thread for i in range(NUM_HOUSES)]

        while number_of_connections < NUM_HOUSES :
            #print("waiting for a connection")
            client_socket, address = server_socket.accept()
            client_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            sockets[number_of_connections] = threading.Thread(target = home_interaction, args =(client_socket, address, current_temp,))
            sockets[number_of_connections].start()
            number_of_connections +=1
        
        everybody_connected.value = True

        for h in sockets :
            h.join()

def home_interaction(client_socket, address, current_temp) :
    #with client_socket: 
    global internal_event

    trade_policy = client_socket.recv(1024)
    client_policy = int.from_bytes(trade_policy, "big")
    print(f"*************** Connected to client : {address}. Client's policy is number : {client_policy} **********************")

    while current_temp.value != 10000 :
        data = client_socket.recv(1024)
        client_request = data.decode()
        client_request = str(client_request)
        # on enlève les espaces indésirables
        client_request = client_request.strip()
        # on enlève les char spéciaux
        client_request = ''.join(char for char in client_request if char in printable)
        
        if client_request == "BUY" : 
            #if full_sim == True : 
            print("FROM MARKET : someone just bought me energy")
            with lock : 
                internal_event = True
        elif client_request == "SELL" : 
            #if full_sim == True : 
            print("FROM MARKET : someone just sold me energy")
            with lock :
                internal_event = False
    print("Disconnecting from client: ", address) 
    client_socket.close()

def market(current_temp, number_of_houses, everybody_connected, full_simulation) :

    global NUM_HOUSES
    global full_sim
    NUM_HOUSES = number_of_houses
    full_sim = full_simulation

    #print("Market function")
    #print(f"Market PID : {multiprocessing.current_process().pid}")
    signal.signal(signal.SIGCHLD, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)

    pid = multiprocessing.current_process().pid

    ext = multiprocessing.Process(target=(external), args=(pid, current_temp, everybody_connected,))
    ext.start()

    tcp_socket = threading.Thread(target=(socket_creation), args=(current_temp, everybody_connected,))
    tcp_socket.start()

    newPrice(current_temp, everybody_connected)

    ext.join()
    tcp_socket.join()