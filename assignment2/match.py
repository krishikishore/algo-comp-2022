import numpy as np
from typing import List, Tuple
import random

# Define Person class to make structure simpler
class Person:
    def __init__(self, index, gender_id, gender_pref):
        self.index = index
        self.gender_id = gender_id
        self.gender_pref = gender_pref
    def __repr__(self): 
        return "Person index:% s gender_id:% s gender_pref:% s\n" % (self.index, self.gender_id, self.gender_pref)

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:

    # Initialize variables

    N = len(gender_id)
    proposers = []
    receivers = []
    matches = []
    
    # Create list of receivers

    for i in range(int(N/2)):
        person = Person(i, gender_id[i], gender_pref[i])
        receivers.append(person)
    
    # Create list of proposers

    for i in range(int(N/2), N):
        person = Person(i, gender_id[i], gender_pref[i])
        proposers.append(person)

    # Optimize values for gender identities and preferences

    for proposer in proposers:
        for receiver in receivers:
            if (proposer.gender_pref == "Men" and receiver.gender_id != "Male") or (receiver.gender_pref == "Men" and proposer.gender_id != "Male") or (proposer.gender_pref == "Women" and receiver.gender_id != "Female") or (receiver.gender_pref == "Women" and proposer.gender_id != "Female"): 
                scores[receiver.index][proposer.index] = 0
                scores[proposer.index][receiver.index] = 0                

    # Set up way to track proposers and receivers left to match and matches themselves

    proposerslefttomatch = []
    for proposer in proposers:
        proposerslefttomatch.append(proposer.index)
    
    receiverslefttomatch = []
    for receiver in receivers:
        receiverslefttomatch.append(receiver.index)

    matches = []

    # While there are still people left to propose

    while len(proposerslefttomatch) > 0:

        # Collect and sort preferences of first proposer on list of proposers

        preferences = []
        for receiver in receivers:
            preferences.append(scores[proposerslefttomatch[0]][receiver.index])
        
        indicesofsort = np.argsort(preferences)
        
        # Check if receiver is free

        for receiverindex in indicesofsort:
            if receiverindex in receiverslefttomatch:
                matches.append((receiverindex, proposerslefttomatch[0]))
                receiverslefttomatch.pop(receiverslefttomatch.index(receiverindex))
                break

            bestindex = -1

            # Update best index based on existing matches

            for k in range(len(matches)):
                if matches[k][0] == receiverindex:
                    bestindex = matches[k][1]
                    break
            
            # Use best index to find best score

            bestscore = scores[receiverindex][bestindex]

            # Checking preference over another

            if preferences[receiverindex] > bestscore:
                matches.append((receiverindex, proposerslefttomatch[0]))
                receiverslefttomatch.pop(receiverslefttomatch.index(receiverindex))
                matches.pop(matches.index(receiverindex, bestindex))
        
        # Done with the first proposer on list

        proposerslefttomatch.pop(0)
        print(matches)

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
