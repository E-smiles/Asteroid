
from email.mime import image
from tkinter import Scale
from if3_game.engine import Sprite, Game, Layer, Text
from pyglet import window, font
from math import cos, sin, radians
from random import randint, choice

RESOLUTION = (800, 600) #Constante(qui ne changera pas d'ou les majuscules) qui contient un tupple de la taille de la fênetre.
LIFE_MAX = 5


class AsteroidGame(Game):
    def __init__(self):
        super().__init__()


        font.add_file("fonts/bubble2.ttf")

# Création des layer

        self.background_layer = Layer()
        self.add(self.background_layer) # Je l'ajoute à moi même, je le crée et l'ajoute

        self.game_layer = Layer()
        self.add(self.game_layer)

        self.ui_layer = UILayer()
        self.add(self.ui_layer) #user interface

# Créer les éléments de jeux

        position = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        self.spaceship = Spaceship(position)
        
        self.game_layer.add(self.spaceship)
        self.ui_layer.spaceship = self.spaceship

        for n in range(3): # Je vais le faire 3 fois (astéroides)
            x = randint(0, RESOLUTION[0])
            while x >= 200 and x <= RESOLUTION[0] -200:
                x = randint(0, RESOLUTION[0])
            
            y = randint(0, RESOLUTION[1])
            while y >= 200 and y <= RESOLUTION[1]:
                y = randint(0, RESOLUTION[1])
        
            
            position = (x, y)

            sx = randint(-200, 200)#speed x
            sy = randint(-200, 200)#speed y
            speed = (sx, sy)

            asteroid = Asteroid((position), (speed)) #x - y c'est la position
            self.game_layer.add(asteroid)
            self.ui_layer.asteroids.append(asteroid)

        #Créer les élément background

        bg = Sprite("images/bag.png", (0,0)) #0,0 c'est l'ancrage en bas a gauche
        self.background_layer.add(bg)

        #Power-up temporaire
        power_up = OneUp((200, 200))
        self.game_layer.add(power_up)
        
class UILayer(Layer):

    def __init__(self):
        super().__init__() 

        #text = Text("Ceci sont des astéroides.", (400, 560), 36, anchor="center", font_name="Bubble")
        #self.add(text) Si je veux mettre un message au demarage

        self.spaceship = None

        self.asteroids = []

        self.lifes = []

        for n in range(LIFE_MAX):
            pos_x = 750 - n * 35 #Position horizontal
            pos_y = 550

            image = "images/life2.gif"
            position = (pos_x, pos_y)
            anchor = (8, 8)
            s = Sprite(image, position, scale= 0.2, anchor = anchor)
            self.add(s)

            self.lifes.append(s)

            self.game_over_message = text = Text("", (400, 300), 100, anchor="center", font_name="bubble mim")
            self.add(self.game_over_message)

            self.you_win_message = text = Text("", (400, 300), 100, anchor="center", font_name="bubble mim")
            self.add(self.you_win_message)


    def update(self, dt):
        super().update(dt)

        #afficher de la vie du vaisseau

        for index in range(len(self.lifes)):
            if index < self.spaceship.life:
                self.lifes[index].opacity = 255
            else :
                self.lifes[index].opacity = 0
                
        if self.spaceship.life <= 0:
            self.game_over_message.text = "Game Over"          
        else:
            self.game_over_message.text = ""

        player_won = True

        for asteroid in self.asteroids:
            if asteroid.is_destroyed == False:
                player_won = False
                break
        if player_won:
            self.you_win_message.text = "You Win !"


class SpaceItem(Sprite):
    def __init__(self, image, position, anchor, speed = (0, 0), rotation_speed = 0): #Constructeur 
        super().__init__(image, position, anchor = anchor, collision_shape = "circle")# Si je veux que se soit un rectangle je change avec le mot rectangle - Chemin vers l'image et anchor au centre de mon image
        self.speed = speed #Je lui donne une vitesse de 0 pour commencer
        self.rotation_speed = rotation_speed #Prendra la valeur par defaut 0

    def update(self, dt): #différence de temps deltatime (La différence, l'écart de temps) Fonction update : Call back appeler a chaque frame
        super().update(dt) #Le dt : le temps durant la derniere update
        pos_x = self.position[0] #Position horizontal
        pos_y = self.position[1] #Position vertical

#calcule du déplacement

        move = (self.speed[0] * dt, self.speed[1] * dt)#e= Vitesse * le temps mouvement rectiline uniforme

# Application du déplacement

        pos_x += move[0]
        pos_y += move[1]

#Correction de la position si on sort de l'écran

        if pos_x > RESOLUTION[0] + 32:
            pos_x = -32

        elif pos_x < -32:
            pos_x = RESOLUTION[0] + 32

        if pos_y > RESOLUTION[1] + 32:
            pos_y = -32
        elif pos_y < -32:
            pos_y = RESOLUTION[1] + 32
        
        
#On bouge effectivement l'objet

        self.position = (pos_x , pos_y) #Tupple qu'on peut remplacer

# On applique la rotation ici
        self.rotation += self.rotation_speed * dt


#un nombre de degre par seconde multiplier par le temps (dt - temps entre deux frames)
#Rotation sef.rotation => rotation actuel
#Self.rotation_speed qui est la vitesse de rotation ajouter a ta rotation la vitesse de rotation * par le temps

class Spaceship(SpaceItem):
    def __init__(self, position):
        image = "images/whale3.png"
        anchor = (68, 32)
        super().__init__(image, position, anchor)
        self.velocity = 0 #velocity sera l'hypoténus

        self.invulnerability = False
        self.chrono = 0
        self.life = 3
        self.is_overpowered = False

    def update(self, dt):        

        if self.invulnerability == True:
            self.opacity = 125
            self.chrono += dt # Je garde en mémoire le temps de vie quelle a depuis la création de mon objet
            if self.chrono >= 3:
                self.invulnerability = False
                self.chrono = 0
        
        else:
            self.opacity = 255

        if self.is_overpowered == True:
            self.power_chrono += dt
            if self.power_chrono >= 10:
                self.is_overpowered = False
                self.change_image("images/spaceship.png")
                self.power_chrono = 0


        
        dsx = cos(radians(self.rotation)) * self.velocity #d pour delta
        dsy = sin(radians(self.rotation)) * self.velocity * -1 #inverser la velocité avec le negatif
        
        sx = self.speed[0] + dsx
        sy = self.speed[1] + dsy
        self.speed =(sx, sy)

        super().update(dt)
        
    def over_power_on(self):
        self.change_image("images/spaceship.png")
        self.is_overpowered = True
        self.power_chrono = 0 

    def on_key_press(self, key, modifiers): #Quand on appuie sur la touche ctl shift clé presser ensemble = modifiers
        if key == window.key.LEFT:
            self.rotation_speed -= 50
        elif key == window.key.RIGHT:
            self.rotation_speed = 50
        elif key == window.key.UP:
            self.velocity = 5
        elif key == window.key.SPACE:
            self.spawn_bullet()
            
    
    def on_key_release(self, key, modifiers):
        if key == window.key.LEFT and self.rotation_speed < 0:
            self.rotation_speed = 0
        elif key == window.key.RIGHT and self.rotation_speed > 0:
            self.rotation_speed = 0
        elif key == window.key.UP:
            self.velocity = 0
    
    def spawn_bullet(self):

        bullet_velocity = 100
        sx = cos(radians(self.rotation)) * bullet_velocity
        sy = sin(radians(self.rotation)) * bullet_velocity * -1
    
        bullet_speed = (self.speed[0] + sx, self.speed[1] + sy)

        x = cos(radians(self.rotation)) * 70 #Pour que la bullet sort du vaisseau sans toucher le vaisseau - Si mon vaisseau fait 150 je / par 2 plus 4 pour que ça sorte de mon vaiseau
        y = sin(radians(self.rotation)) * 70 * -1

        bullet_position = (self.position[0] + x, self.position[1] + y) #[0] axe des x

        bullet = Bullet(bullet_position, bullet_speed)
        self.layer.add(bullet) #
    
    def on_collision(self, other):
            if isinstance(other, Asteroid): #Is instance = Verifier que l'objet appartient a la classe et ses enfants -Si l'autre objet est un spaceship alors je le détruit
                if self.is_overpowered:
                    other.destroy()
                else:
                    self.destroy()

    def destroy(self):
        
        if self.invulnerability == False:
            self.invulnerability = True
            self.life -= 1
            print(self.life)
            if self.life <= 0:
                super().destroy() #éviter la récursivité 

class Asteroid(SpaceItem):
    def __init__(self, position, speed, level =3):

        self.level = level
        if level == 3:
            image = "images/asteroid128.png"
            anchor = (64, 64)
        elif level == 2:
            image = "images/asteroid64.png"
            anchor = (32, 32)
        else:
            image = "images/asteroid32.png"
            anchor = (16, 16)

        rotation_speed = 50 #Pour changer la vitesse de rotation des asteroides
        super().__init__(image, position, anchor, speed, rotation_speed)
    
    def destroy(self):
        if self.level > 1:
            for n in range(2):
                sx = randint(-300, 300)
                sy = randint(-300, 300)
                speed = (sx, sy)

                level = self.level -1
                asteroid = Asteroid(self.position, speed, level = level)

                self.layer.add(asteroid)
                self.layer.game.ui_layer.asteroids.append(asteroid) #Le caractère de traversé

        if randint(1, 5) == 1:
            possibilities =[
                OneUp(self.position), 
                Overpower(self.position)]
            power_up = choice(possibilities)
            self.layer.add(power_up)

        super().destroy()

    

class Bullet(SpaceItem):
    def __init__(self, position, speed):
        image = "images/bubble.png"
        anchor = (8,8)
        rotation_speed = 5
        super().__init__(image,position, anchor, speed, rotation_speed)

        self.life_time = 0


    def update(self, dt):
        super().update(dt) # Comportement de l'ancètre

        self.life_time += dt # Je garde en mémoire le temps de vie quelle a depuis la création de mon objet

        if self.life_time >= 3:
            self.destroy()

    def on_collision(self, other):
        if isinstance(other, Asteroid):
           self.destroy()
           other.destroy()


class PowerUp(SpaceItem):

    def __init__(self, image, position, anchor, life_time):
        super().__init__(image, position, anchor)
        self.life_time = life_time
    
    def update(self, dt):
        super().update(dt)

        self.life_time -= dt
        if self.life_time <= 0:
            self.destroy()

    def on_collision(self, other):
        if isinstance(other, Spaceship):
           self.apply_effect(other)
           self.destroy()

    def apply_effect(self, spaceship):
        pass

class OneUp(PowerUp):

    def __init__(self,position):
        
        image = "images/get_a_life.png"
        anchor = (16, 16)
        life_time = 10
        
        super().__init__(image, position, anchor, life_time)

    def apply_effect(self, spaceship):
        if spaceship.life < LIFE_MAX:
            spaceship.life += 1

class Overpower(PowerUp):

    def __init__(self,position):
        
        image = "images/powerup.png"
        anchor = (16, 16)
        life_time = 10
        super().__init__(image, position, anchor, life_time)

    def apply_effect(self, spaceship):
        spaceship.over_power_on()


