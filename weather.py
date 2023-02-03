#**************** La fonction weather fait croitre ou décroitre la température aléatoirement de 1 toutes les secondes

import random
import time
import multiprocessing

MONTH_DURATION = 15

def weather(current_temp, temps_max, everybody_connected) :
    while everybody_connected.value != True : 
        time.sleep(0.1)
    start = time.time()
    execution = 0
    month = 0
    print (" ")
    print (" ")
    print(f"MONTH NUMBER {month+1}")
    print (" ")
    print (" ")

    while execution < temps_max : 
        aleatoire = random.choice([True, False])
        if aleatoire == True : 
            current_temp.value = current_temp.value + 1
        else : 
            current_temp.value = current_temp.value - 1
        time.sleep(1)
        end = time.time()
        execution = end - start

        # one month = 15 seconds
        if execution >= (month * MONTH_DURATION + MONTH_DURATION) :
            month +=1 
            print (" ")
            print (" ")
            print(f"MONTH NUMBER {month+1}")
            print (" ")
            print (" ")

    current_temp.value = 10000
    print(" ")
    print(" ")
    print("TIME REACHED END OF SIMULATION")
    print(" ")
    print(" ")
