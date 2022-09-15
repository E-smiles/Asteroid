from if3_game.engine import init, Layer, Sprite
from asteroid import RESOLUTION, AsteroidGame, Spaceship, Asteroid, Bullet
from random import randint


init(RESOLUTION,(" " * 100) +  "Asteroid") #Fonction init : on lui donne la résolution et une chaine de caractere, qui va initier le titre de la fentre.

game = AsteroidGame()
game.run() #Elle lance le jeu, on utilise la methode run.

