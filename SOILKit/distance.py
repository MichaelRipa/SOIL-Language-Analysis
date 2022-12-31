#! /usr/bin/env python3

from scipy.stats import entropy

def symmetrical_kl_divergence(dict1,dict2,smoothing_factor=0.5):

    #Ensure both dictionaries have same keys
    dict1,dict2 = _equate_distributions(dict1,dict2)
    #Place distributions in format compatible with scipy
    vec1 = []
    vec2 = []
    for key in dict1.keys():
        vec1.append(dict1[key])
        vec2.append(dict2[key])

    #Convert to probability distribution & apply smoothing
    smoothed_vec1 = _convert_to_distribution(vec1,smoothing_factor)
    smoothed_vec2 = _convert_to_distribution(vec2,smoothing_factor)

    #Compute symmetrical KL divergence
    return (entropy(vec1,vec2) + entropy(vec2,vec1))/2

def _equate_distributions(dict1,dict2):
    '''Ensures two distributions have the same sample space. Any "event" present in `dict1` but missing from `dict2` gets inserted into `dict2` with zero probability (and vice versa)'''
    
    events_dict1 = list(dict1.keys())
    events_dict2 = list(dict2.keys())
    #Iterate through keys of both dictionaries
    for event in (events_dict1 + events_dict2):
        #Ensure both dictionaries contain event
        if event not in dict1.keys():
            dict1[event] = 0
        if event not in dict2.keys():
            dict2[event] = 0

    return dict1, dict2

def _convert_to_distribution(frequencies,smoothing_factor=0.5):
    '''Converts an array `frequencies` (raw counts) to a probability distribution. Applies smoothing to events with no counts (value of 0) with respect to `smoothing_factor`'''
    total_frequency = 0
    total_smoothed = 0
    # Iterate over each frequency, apply smoothing if null
    for i,freq in enumerate(frequencies):
        total_frequency += freq 
        if freq == 0:
            frequencies[i] += smoothing_factor
            total_smoothed += smoothing_factor
    
    total = total_frequency + total_smoothed
    for i in range(len(frequencies)):
        frequencies[i] /= total

    return frequencies

