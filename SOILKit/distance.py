#! /usr/bin/env python3

def kl_divergence(dict1,dict2):
    #Ensure both dictionaries have same keys
    dict1,dict2 = _equate_distributions(dict1,dict2)
    return



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
