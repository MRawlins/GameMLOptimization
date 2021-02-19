import random
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import GameDetails as game

#This function is defined so that the return variable is what we're seeking to minimize. Analogue to playing multiple rounds?
def f(X):
    return np.sum(X)

varbound = np.array([[0,10]]*3)

#function to minimize, three input variables
#This algorithm is designed to minimize its input. So, to maximize, we'd toss in a negative sign to the above return value.
model = ga(function=f, dimension=3, variable_type='int', variable_boundaries=varbound)

model.run()

convergence = model.report
solution = model.output_dict

#main
deck = game.Deck()
players = []
for x in range(4):
    players.append(game.Player())
gameState = game.GameState(players)
game.playRound(gameState, deck)