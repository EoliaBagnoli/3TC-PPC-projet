#******************************* La fonction external crée un des évenements proposés aléatoirement à des intevalles de temps aléatoires. 

import time
import signal
import os
import random

def external(pid_market) : 
    print("here is external")
    while True :
        print("What is happening to the Market ?")
        evenement = random.randint(1, 4)
        if evenement == 1 :
            print("HURRICANE")
            os.kill(pid_market, signal.SIGCHLD)
        elif evenement == 2 : 
            print("PUTIN MAKES A WAR")
            os.kill(pid_market, signal.SIGUSR1)
        elif evenement == 3 : 
            print("FUEL SHORTAGE")
            os.kill(pid_market, signal.SIGUSR2)
        elif evenement == 4 : 
            print("BUTTERFLY EFFECT")
            #os.kill(pid_market, signal.SIGINT)
        else : 
            print("L'evenement que vous avez demandé n'existe pas")
        time.sleep(random.randint(10,100))