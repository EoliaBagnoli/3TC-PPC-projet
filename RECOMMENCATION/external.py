#******************************* La fonction external crée un des évenements proposés aléatoirement à des intevalles de temps aléatoires. 

import time
import signal
import os
import random


def external(pid_market, current_temp, everybody_connected) : 

    #waits for everything to get in place before starting
    while everybody_connected.value != True : 
        time.sleep(0.1)

    while current_temp.value != 10000 :

        time.sleep(random.randint(2, 15))
        evenement = random.randint(1, 61)
        if (evenement >= 1) and (evenement <= 20) :
            # correspond to HURRICANE
            os.kill(pid_market, signal.SIGCHLD)
        elif (evenement >= 21) and (evenement <= 40) : 
            # correspond to PUTIN MAKES A WAR
            os.kill(pid_market, signal.SIGUSR1)
        elif (evenement >= 41) and (evenement <= 60) : 
            ## correspond to FUEL SHORTAGE
            os.kill(pid_market, signal.SIGUSR2)
        elif evenement == 61 : 
            print(" ")
            print(" ")
            print("**************************** APOCALYPSE. EVERYBODY IS DEAD. *****************************")
            os.kill(pid_market, signal.SIGINT)
        else : 
            print("L'evenement que vous avez demandé n'existe pas")