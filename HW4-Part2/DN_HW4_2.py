# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 18:20:24 2021

@author: M Sabbagh
"""

import numpy as np
import matplotlib.pyplot as plt

def LB(arrival_times, service_time):
    """
    
    Parameters
    ----------
    arrival_times : 
        A vector containing all the packet arrival times in miliseconds
    service_time :
        Time of service in miliseconds
        
    Returns
    -------
    departure_times :
        A vector containing the times that these packets exit the system

    """
    L = len(arrival_times)
    departure_times = [0] * L
    departure_times[0] = arrival_times[0]
    
    for i in range(L - 1):
        if arrival_times[i + 1] >= departure_times[i] + service_time:
            departure_times[i + 1] = arrival_times[i + 1]
        else:
            departure_times[i + 1] = departure_times[i] + service_time

    return departure_times

#arrival_times = [6, 16, 17, 18, 20, 40]
#print(LB(arrival_times, service_time = 5))

def TB(arrival_times, service_time):
    
    L = len(arrival_times)
    departure_times = [0] * L
    
    for i in range(L):
        if arrival_times[i] // service_time >= i + 1:
            departure_times[i] = arrival_times[i]
        else:
            departure_times[i] = (i + 1) * service_time
    
    return departure_times

#arrival_times = [6, 16, 17, 18, 20, 40]
#print(TB(arrival_times, service_time = 5))


def deterministic(start, T, L):
    """

    Parameters
    ----------
    start : 
        Arrival time of first packet
    T : 
        Inter-arrival time in milisecons
    L : 
        Number of packets

    Returns
    -------
    AP1 : Arrival times vector
        

    """
    
    AP1 = [0] * L       # Arrival times vector
    AP1[0] = start
    for i in range (L - 1):
        AP1[i + 1] = AP1[i] + T
        
    return AP1
        
def deterministic_batch(start, T, L):
    """

    Parameters
    ----------
    start : 
        Arrival time of first packet
    T : 
        1/4 of inter-arrival time in milisecons
    L : 
        Number of packets (L must be a multiple of 4)

    Returns
    -------
    AP2 : Arrival times vector
        

    """
    
    if L % 4 == 0:
        
        AP2 = [0] * L
        
        for i in range (L // 4):
            
            if i == 0:
                
                for j in range(4):
                    AP2[j] = start
            
            if i > 0:
                
                for j in range (4):
                    AP2[4 * i + j] = AP2[4 * (i - 1) + j] + 4 * T
        return AP2
    else:
        return("Error: Number of packets must be a multiple of 4")


def poisson(start, T, L):
    """
    
    Parameters
    ----------
    start : 
        Arrival time of first packet
    T : 
        The inter-arrival time is given by an exponential distribution with mean T
    L : 
        Number of packets

    Returns
    -------
    AP3 : 
        Arrival times vector

    """
    AP3 = [0] * L
    AP3[0] = start
    for i in range (L - 1):
        AP3[i + 1] = AP3[i] + np.random.exponential(scale = T)
    return AP3

def poisson_batch(start, T, L):
    """

    Parameters
    ----------
    start : 
        Arrival time of first packet
    T : 
        The inter-arrival time is given by an exponential distribution with mean 4T
    L : 
        Number of packets (L must be a multiple of 4)

    Returns
    -------
    AP4 : 
        Arrival times vector

    """
    
    if L % 4 == 0:
        
        AP4 = [0] * L
        
        for i in range (L // 4):
            
            if i == 0:
                
                for j in range(4):
                    AP4[j] = start
            
            if i > 0:
                x = np.random.exponential(scale = 4 * T)
                for j in range (4):
                    AP4[4 * i + j] = AP4[4 * (i - 1) + j] + x
        return AP4
    else:
        return("Error: Number of packets must be a multiple of 4")
 
           
def Ave_Delay(arrival_times, departure_times):
    
    if len(arrival_times) == len(departure_times):
        
        L = len(departure_times)
        Delay = 0
        
        for i in range (L):
            Delay = Delay + departure_times[i] - arrival_times[i]
            
        Ave_Delay = Delay / L    
        return Ave_Delay
    else:
        return("Error: Two input arrays must be the same length")
    

# Question 2_ Leaky Bucket

service_time = 5        # Time of service = 5 msec
start = 0               # Arrival time of first packet
L = 10000               # Number of packets
ADLB = np.zeros([4, 18])
throughput_LB = np.zeros([4, 18]) 
utilization = [0] * 18
packet_size = 1000      # Packet size = 1 Kb

for i in range(18):
    T = 20 - i
    utilization[i] = (service_time / T) * 100
    
    AT1 = deterministic(start, T, L)
    DT1 = LB(AT1, service_time)
    ADLB[0, i] = Ave_Delay(AT1, DT1)
    throughput_LB[0, i] = L * packet_size / (DT1[L - 1])
    
    AT2 = deterministic_batch(start, T, L)
    DT2 = LB(AT2, service_time)
    ADLB[1, i] = Ave_Delay(AT2, DT2)
    throughput_LB[1, i] = L * packet_size / (DT2[L - 1])
    
    AT3 = poisson(start, T, L)
    DT3 = LB(AT3, service_time)
    ADLB[2, i] = Ave_Delay(AT3, DT3)
    throughput_LB[2, i] = L * packet_size / (DT3[L - 1])
    
    AT4 = poisson_batch(start, T, L)
    DT4 = LB(AT4, service_time)
    ADLB[3, i] = Ave_Delay(AT4, DT4)
    throughput_LB[3, i] = L * packet_size / (DT4[L - 1])

  
#print(ADLB)
plt.figure()
plt.plot(utilization, ADLB[0, :], label = "Deterministic")
plt.plot(utilization, ADLB[1, :], label = "Deterministic with Batch Arrival")
plt.plot(utilization, ADLB[2, :], label = "Poisson Process")
plt.plot(utilization, ADLB[3, :], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.title("Average Delay of Leaky Bucket")
plt.legend()
plt.show()

#########################################
# Utilization < 100 %
plt.figure()
plt.plot(utilization[0:16], ADLB[0, 0:16], label = "Deterministic")
plt.plot(utilization[0:16], ADLB[1, 0:16], label = "Deterministic with Batch Arrival")
plt.plot(utilization[0:16], ADLB[2, 0:16], label = "Poisson Process")
plt.plot(utilization[0:16], ADLB[3, 0:16], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.title("Average Delay of Leaky Bucket")
plt.legend()
plt.show()
#########################################
   
plt.figure()
plt.plot(utilization, throughput_LB[0, :], label = "Deterministic")
plt.plot(utilization, throughput_LB[1, :], label = "Deterministic with Batch Arrival")
plt.plot(utilization, throughput_LB[2, :], label = "Poisson Process")
plt.plot(utilization, throughput_LB[3, :], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.title("Throughput of Leaky Bucket")
plt.legend()
plt.show()

############################################
# Utilization < 100 % 
plt.figure()
plt.plot(utilization[0:16], throughput_LB[0, 0:16], label = "Deterministic")
plt.plot(utilization[0:16], throughput_LB[1, 0:16], label = "Deterministic with Batch Arrival")
plt.plot(utilization[0:16], throughput_LB[2, 0:16], label = "Poisson Process")
plt.plot(utilization[0:16], throughput_LB[3, 0:16], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.title("Throughput of Leaky Bucket")
plt.legend()
plt.show()
############################################
    


# Question 2_ Token Bucket

service_time = 5        # Time of service = 5 msec
start = 0               # Arrival time of first packet
L = 10000               # Number of packets
ADTB = np.zeros([4, 18])
throughput_TB = np.zeros([4, 18]) 
utilization = [0] * 18
packet_size = 1000      # Packet size = 1 Kb

for i in range(18):
    T = 20 - i
    utilization[i] = (service_time / T) * 100
    
    AT1 = deterministic(start, T, L)
    DT1 = TB(AT1, service_time)
    ADTB[0, i] = Ave_Delay(AT1, DT1)
    throughput_TB[0, i] = L * packet_size / (DT1[L - 1])
    
    AT2 = deterministic_batch(start, T, L)
    DT2 = TB(AT2, service_time)
    ADTB[1, i] = Ave_Delay(AT2, DT2)
    throughput_TB[1, i] = L * packet_size / (DT2[L - 1])
    
    AT3 = poisson(start, T, L)
    DT3 = TB(AT3, service_time)
    ADTB[2, i] = Ave_Delay(AT3, DT3)
    throughput_TB[2, i] = L * packet_size / (DT3[L - 1])
    
    AT4 = poisson_batch(start, T, L)
    DT4 = LB(AT4, service_time)
    ADTB[3, i] = Ave_Delay(AT4, DT4)
    throughput_TB[3, i] = L * packet_size / (DT4[L - 1])
    
    
#print(ADTB)
plt.figure()
plt.plot(utilization, ADTB[0, :], label = "Deterministic")
plt.plot(utilization, ADTB[1, :], label = "Deterministic with Batch Arrival")
plt.plot(utilization, ADTB[2, :], label = "Poisson Process")
plt.plot(utilization, ADTB[3, :], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.title("Average Delay of Token Bucket")
plt.legend()
plt.show()

################################################
# Utilization < 100 % 
plt.figure()
plt.plot(utilization[0:16], ADTB[0, 0:16], label = "Deterministic")
plt.plot(utilization[0:16], ADTB[1, 0:16], label = "Deterministic with Batch Arrival")
plt.plot(utilization[0:16], ADTB[2, 0:16], label = "Poisson Process")
plt.plot(utilization[0:16], ADTB[3, 0:16], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.title("Average Delay of Token Bucket")
plt.legend()
plt.show()
################################################
    
plt.figure()
plt.plot(utilization, throughput_TB[0, :], label = "Deterministic")
plt.plot(utilization, throughput_TB[1, :], label = "Deterministic with Batch Arrival")
plt.plot(utilization, throughput_TB[2, :], label = "Poisson Process")
plt.plot(utilization, throughput_TB[3, :], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.title("Throughput of Token Bucket")
plt.legend()
plt.show()

###############################################
# Utilization < 100 % 
plt.figure()
plt.plot(utilization[0:16], throughput_TB[0, 0:16], label = "Deterministic")
plt.plot(utilization[0:16], throughput_TB[1, 0:16], label = "Deterministic with Batch Arrival")
plt.plot(utilization[0:16], throughput_TB[2, 0:16], label = "Poisson Process")
plt.plot(utilization[0:16], throughput_TB[3, 0:16], label = "Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.title("Throughput of Token Bucket")
plt.legend()
plt.show()
###############################################
   

plt.figure()
plt.plot(utilization, ADLB[0, :], label = "Leaky Bucket" )
plt.plot(utilization, ADTB[0, :], label = "Token Bucket")
plt.title("Deterministic")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, ADLB[1, :], label = "Leaky Bucket" )
plt.plot(utilization, ADTB[1, :], label = "Token Bucket")
plt.title("Deterministic with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, ADLB[2, :], label = "Leaky Bucket" )
plt.plot(utilization, ADTB[2, :], label = "Token Bucket")
plt.title("Poisson Process")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, ADLB[3, :], label = "Leaky Bucket" )
plt.plot(utilization, ADTB[3, :], label = "Token Bucket")
plt.title("Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Average Delay (msec)")
plt.legend()
plt.show()



plt.figure()
plt.plot(utilization, throughput_LB[0, :], label = "Leaky Bucket")
plt.plot(utilization, throughput_TB[0, :], label = "Token Bucket")
plt.title("Deterministic")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, throughput_LB[1, :], label = "Leaky Bucket")
plt.plot(utilization, throughput_TB[1, :], label = "Token Bucket")
plt.title("Deterministic with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, throughput_LB[2, :], label = "Leaky Bucket")
plt.plot(utilization, throughput_TB[2, :], label = "Token Bucket")
plt.title("Poisson Process")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.legend()
plt.show()

plt.figure()
plt.plot(utilization, throughput_LB[3, :], label = "Leaky Bucket")
plt.plot(utilization, throughput_TB[3, :], label = "Token Bucket")
plt.title("Poisson Process with Batch Arrival")
plt.xlabel("Utilization (%)")
plt.ylabel("Throughput (Kbps)")
plt.legend()
plt.show()