#!usr/bin/env python3
import json
import sys
import os
import collections as c

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def response_grid(users):
    responses = []
    for user in users:
        responses.append(user.responses)
    return responses

def distribution_scores(qnum, answer, grid):
    qanswers = []
    for responses in grid:
        qanswers.append(responses[qnum])
    counts = c.Counter(qanswers)
    factor = 1 - (0.9 * (counts[answer] / len(grid)))
    return factor

def max_comp(users):
    maxcomp = 0
    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            if (compute_score(user1, user2, responsegrid) > maxcomp):
                maxcomp = compute_score(user1, user2, responsegrid) 
    return maxcomp

# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2, responsegrid):
    score = 0
    user1answers = user1.responses
    user2answers = user2.responses
    for i in range(0, len(user1answers)):
        if user1answers[i] == user2answers[i]:
            score += (1 * distribution_scores(i, user1answers[i], responsegrid))
    score /= len(user1answers)
    if (user1.gender in user2.preferences) and (user2.gender in user1.preferences):
        score *= 1
    else:
        score *= 0.1
    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    responsegrid = response_grid(users)
    highest_comp = max_comp(users)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, responsegrid)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score/highest_comp))
