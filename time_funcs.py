import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def noise(s):
    rand = random.uniform(0.001,0.999)
    return s * math.log((1 - rand)/rand)

def time_to_pulses(time, t_0 = 0.011, a = 1.1, b = 0.015, add_noise = True):
    
    pulses = 0
    pulse_duration = t_0
    
    while time >= pulse_duration:
        time = time - pulse_duration
        pulses = pulses + 1
        pulse_duration = a * pulse_duration + add_noise * noise(b * a * pulse_duration)
        
    return pulses

def pulses_to_time(pulses, t_0 = 0.011, a = 1.1, b = 0.015, add_noise = True):
    
    time = 0
    pulse_duration = t_0
    
    while pulses > 0:
        time = time + pulse_duration
        pulses = pulses - 1
        pulse_duration = a * pulse_duration + add_noise * noise(b * a * pulse_duration)
    
    return time

def peak(t, reps = 10, n_training = 10, n_trials = 100):
    #n training: number of times you see the time simulation and “convert it to pulsess” (psychological time)
    # n_trail: number of times you try to recrate the simulation from “memory”
    results = pd.DataFrame(columns = ['rep', 'val'])
    for rep in range(reps):
        goal_pulses = 0
        for i in range(n_training):
            goal_pulses += time_to_pulses(t)
        goal_pulses = goal_pulses / n_training
        for i in range(n_trials):
            val = pulses_to_time(goal_pulses)
            results.loc[len(results)] = [rep, val]
    return results['val']

def bisection(values, reps = 100, n_training = 10, n_trials = 10):
    #n training: number of times you see the time simulation and “convert it to pulsess” (psychological time)
    # n_trail: number of times you try to recrate the simulation from “memory”

    training_short = min(values)
    training_long = max(values)
    
    results = pd.DataFrame(columns = ['rep', 'interval', 'prop_long'])
    
    for rep in range(reps):
        
        # training
        short = [time_to_pulses(training_short) for i in range(n_training)]
        short_pulses = sum(short) / len(short)
        long = [time_to_pulses(training_long) for i in range(n_training)]
        long_pulses = sum(long) / len(long)
        
        # testing
        for val in values:
            pulses = [time_to_pulses(val) for i in range(n_trials)]
            long_response = [p - short_pulses > long_pulses - p for p in pulses]
            prop_long = sum(long_response) / len(long_response)
            results.loc[len(results)] = [rep, val, prop_long]
    
    # plot mean proportion of long responses
    results = results.groupby(['interval'])['prop_long'].mean().reset_index()
    plt.plot(results['interval'], results['prop_long'], marker = "o")
    plt.xlabel("Time interval (s)")
    plt.ylabel("Proportion long")