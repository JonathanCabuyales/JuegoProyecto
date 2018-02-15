# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pygame, os, time
from random import *
from pygame.locals import *

desarrollador = False

# controles de a clase piso colisionan para que el personaje permanezca en el piso

class Piso(pygame.sprite.Sprite):
    def __init__(self,longitud,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((longitud,1))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top


class plataforma(pygame.sprite.Sprite):
    def __init__(self,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/plataforma.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.tech_sprite_lower = Piso(self.rect.width - 34,self.rect.left + 17,self.rect.top - 1)
        self.tech_sprite_upper = Piso(self.rect.width - 34,self.rect.left + 17,self.rect.top - 46)
        

#movimiento de plataforma elevadores
#la herencia no es aplicable debido al uso de sprites 
#movimiento a la derecha e izquierda
class Movimiento(pygame.sprite.Sprite):

	def __init__(self, top, left, right, velocidad):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('res/plataforma.png')
		self.rect = self.image.get_rect()
		self.rect.top = top
		self.rect.left = right
		self.limitleft = left
		self.limitright = right
		self.tech_sprite_lower = Piso(self.rect.width-44,self.rect.top + 65,self.rect.right - 66)
		self.tech_sprite_upper = Piso(self.rect.width-44,self.rect.top + 65,self.rect.right - 66)
		self.velocidad = velocidad
		self.up = True

	def update(self):
		if self.rect.left < self.limitleft:
			self.up = False
		if self.rect.left > self.limitright:
			self.up = True
		if self.up:
			self.rect.left -= self.velocidad
			self.tech_sprite_lower.rect.left -= self.velocidad
			self.tech_sprite_upper.rect.left -= self.velocidad
		else:
			self.rect.left += self.velocidad
			self.tech_sprite_lower.rect.left += self.velocidad
			self.tech_sprite_upper.rect.left += self.velocidad
		
		

#movimiento arriba - abajo

class Elevador(pygame.sprite.Sprite):
    def __init__(self, left, top, bottom, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/plataforma.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = bottom
        self.limittop = top
        self.limitbot = bottom
        self.tech_sprite_lower = Piso(self.rect.width-34,self.rect.left+17,self.rect.top-1)
        self.tech_sprite_upper = Piso(self.rect.width-34,self.rect.left+17,self.rect.top-46)
        self.velocidad = velocidad
        self.up = True
        #dimensiones del personaje y algo de espacio

    def update(self):
        if self.rect.top < self.limittop:
            self.up = False
        if self.rect.top > self.limitbot:
            self.up = True
        if self.up:
            self.rect.top -= self.velocidad
            self.tech_sprite_lower.rect.top -= self.velocidad
            self.tech_sprite_upper.rect.top -= self.velocidad
        else:
            self.rect.top += self.velocidad
            self.tech_sprite_lower.rect.top += self.velocidad
            self.tech_sprite_upper.rect.top += self.velocidad
        
        

class Moneda(pygame.sprite.Sprite):
    def __init__(self,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/moneda.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.wait = 0
        self.muerte = False

    def collect(self,sonido):
        self.image = pygame.transform.scale(self.image, (22, 22))
        if not self.muerte:
            sonido.play()
        self.muerte = True
        
    def update(self):
        
        if self.muerte:
            self.wait +=1
            self.rect.top -= 3
        if self.wait > 8:
            self.kill()
            Aladdin.monedas +=1
        if self.wait == 1:
            self.rect.left -= 3

class Rock (pygame.sprite.Sprite):

    def __init__ (self, left, anticipacion, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [pygame.image.load('res/rock1.png'),pygame.image.load('res/rock2.png')]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.init = left
        self.rect.top = -self.rect.height/2
        self.anticipacion = anticipacion
        self.anticipado = 0
        self.vy = 0
        self.velocidad = velocidad
        self.esperaragitar = 0
    
    def shake(self):
        k = randint(0,5)
        if self.esperaragitar == 1:
            self.rect.left += k
        elif self.esperaragitar == 3:
            self.rect.left -= k
        self.esperaragitar += 1
        self.esperaragitar %= 4


    def red(self):
        self.image = self.frames[1]
        
    def fall(self):
        self.rect.left = self.init
        self.image = self.frames[0]
        self.vy = self.velocidad
    

    def update (self):
        
        if self.anticipado in range (self.anticipacion/3, self.anticipacion):
            self.shake()
        if self.anticipado  in range (self.anticipacion * 2 /3, self.anticipacion):
            self.red ()
        elif self.anticipado > self.anticipacion:
            self.fall()
        else:
            self.vy = 0

        if self.rect.top > 300:
            self.kill()
            
        self.anticipado += 1
        self.rect.top += self.vy



class Aladdin (pygame.sprite.Sprite):
    
    monedas = 1
    
    def __init__ (self, juego, nivel, frecuencia_roca, anticipacion_roca):
        pygame.sprite.Sprite.__init__(self)
        self.stay = pygame.image.load('res/aladdin.png')
        self.frames = [pygame.image.load('res/aladdin.png'),pygame.image.load('res/aladdin1.png'),\
                       pygame.image.load('res/aladdin2.png'),pygame.image.load('res/aladdin3.png'),\
                       pygame.image.load('res/aladdin4.png'),]
        self.jump_img = pygame.image.load('res/jump.png')
        self.jump_f = pygame.image.load('res/jump_f.png')
        self.estructura = 0
        self.image = self.stay

        #settings for player's movements
        #opciones de movimiento para el jugadores
        self.velocidad = 8
        self.falspeed = 10
        self.velocidadsalto = -12
        self.duracionsalto = 4
        
        self.x = 0
        self.y = 210
        self.vx = 0
        self.vy = self.falspeed
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.tiemposalto = 0
        self.saltando = False
        self.jumpable = False
        self.start = time.time()
        self.paused = time.time() - time.time() 
        self.t= time.time()
        self.texto = pygame.font.Font('res/font/04B_03__.TTF', 14)
        self.text1 = pygame.font.Font('res/font/04B_03__.TTF', 10)
        self.text2 = pygame.font.Font('res/font/04B_03__.TTF', 96)
        self.advertencia = self.texto.render('', False, (255,0,0))
        self.mensaje = self.texto.render('', False, (255,255,255))
        self.mensaje3 = self.texto.render('', False, (255,255,255))
        self.nivel = nivel
        self.message2 = self.texto.render('nivel 0' + str(self.nivel), False, (255,255,255))
        self.message3 = self.text2.render('nivel 0' + str(self.nivel), False, (255,255,255))
        Aladdin.monedas = 0
        self.rocks = []
        self.globalrocks = juego.rocks
        self.rockfrequency = 1
        self.frecuencia_roca = frecuencia_roca
        self.anticipacion_roca = anticipacion_roca
        self.opacity = 255
        self.opacitywait = 0
        self.pausa = time.time()
        self.lag = 0

    def pause_t(self, bandera):
        if not bandera:
            self.pausa = time.time()
        else:
            self.pausa = time.time() - self.pausa
            self.paused += self.pausa
        
        

    def jump(self, sonido):
        if self.jumpable:
            sonido.play()
            self.tiemposalto = 0
            self.saltando = True
        
    def update(self):

        if self.opacitywait < 15:
            self.opacitywait += 1
        else:
            self.message3.set_alpha(self.opacity)
            self.opacity -= 9
    
        if self.saltando:
            if self.tiemposalto < self.duracionsalto:
                self.tiemposalto +=1
                self.vy = self.velocidadsalto
            else:
                self.tiemposalto = 0
                self.saltando = False

        
        self.advertencia = self.texto.render('', False, (255,0,0))
        if self.x + self.vx in range (0 - self.velocidad,533 - self.rect.width + self.velocidad):
            self.x += self.vx
        elif self.x + self.vx > 533 - self.rect.width + self.velocidad:
            # numero de monedas para pasar de nivel
            if Aladdin.monedas == 5:
                NuevoJuego(self.nivel+1)
            else:
                self.advertencia = self.texto.render('recoge las monedas primero', False, (255,0,0))

        self.lag += 1
        self.lag %= 2
        if self.vy != 0 and self.vx > 0:
            self.image = self.jump_img
        elif self.vy != 0 and self.vx < 0:
            self.image = self.jump_img
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.vy !=0 and self.vx == 0:
            self.image = self.jump_f
        elif self.vx == 0:
            self.image = self.stay
        elif self.vx > 0 and self.lag == 0:
            self.image = self.frames[self.estructura + 1]
            self.estructura += 1
            self.estructura %= len(self.frames) - 1
        elif self.vx < 0 and self.lag == 0:
            self.image = self.frames[self.estructura + 1]
            self.image = pygame.transform.flip(self.image, True, False)
            self.estructura += 1
            self.estructura %= len(self.frames) - 1
        
        self.y += self.vy
        self.rect.left = self.x
        self.rect.top = self.y
        self.mensaje = self.texto.render(str(Aladdin.monedas )+ '/5', False, (255,255,255))
        self.t= time.time() - self.start - self.paused
        self.rockfrequency += 1
        self.rockfrequency %= self.frecuencia_roca #Aumentar la frecuencia de la ricas 
        if self.rockfrequency == 0:
            self.rockrandom = randint (0, 500)  # colocar las rocas aleatorianmente  dentro del rango 0- 500 (pantalla)
            self.rocks.append(Rock(self.rockrandom, self.anticipacion_roca, 10))
            self.globalrocks.add(self.rocks.pop())

        self.mensaje3 = self.texto.render(str(round(self.t,1))+ ' ' + 's', False, (255,255,255))
        
        
class Juego():
    def __init__(self, nivel, plataforma, monedas, frecuencia_roca, anticipacion_roca):
        #instanciando las clases
        #[bottom floor, middle floor, top floor, first stopper, second stopper]
        self.floor = [Piso(194,0,275),Piso(147,207,248),Piso(190,355,224)]
        self.stops = [Piso(10,194,261),Piso(10,342,236)]
        self.monedas = monedas
        self.plataforma = plataforma
        self.sprites = pygame.sprite.Group(self.plataforma,self.monedas)
        self.rocks = pygame.sprite.Group()
        self.aladdin = Aladdin(self, nivel, frecuencia_roca, anticipacion_roca)
        self.character = pygame.sprite.Group(self.aladdin)
        
        #sprites para la  plataforma
        if desarrollador:
            for item in plataforma:
                self.sprites.add(item.tech_sprite_lower,item.tech_sprite_upper)
            
        
        self.spritespisos = pygame.sprite.Group(self.floor)
        self.spritesparadas = pygame.sprite.Group(self.stops)

def compare(x,y):
    if float(x[1]) > float (y[1]):
        return 1
    else:
        return -1

def build_highscores(names):
    names = sorted(names, cmp=compare)
    table = []

    for i in range(5):
        table.append ([texto.render(names[i][0], False, (255,255,255)),texto.render(names [i][1] + 's', False, (255,255,255))])
    return table
        
def NuevoJuego(nivel):
    global juego, tiempos, estructura
    if nivel == 1:
        pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load('res/game_bg.mp3')
        pygame.mixer.music.set_volume(volume / 5.0)
        pygame.mixer.music.play(-1, 0.0)
        juego = Juego (nivel, [Movimiento (100, 100, 120, 3), plataforma (40, 150), plataforma (120, 180), 
                        plataforma (200,200),plataforma (186, 120), plataforma (266, 90)],
                    [Moneda(116,45), Moneda(56,132), Moneda(282,72), Moneda (216,182), Moneda (385,55)],
                     40,50)
        
        #colocar las monedas en las plataformas: (x+16,y-18)  
        tiempos = []
        
    if nivel == 2:
        tiempos.append(round(juego.aladdin.t,1))
        juego = Juego (nivel, [plataforma (1, 138), plataforma (48, 180),plataforma (48, 99),
                             plataforma (115, 170), plataforma(160, 85),
                             plataforma (340, 118), plataforma (400, 90),
                             Elevador(460, 120, 210, 3), Elevador(265, 70, 230, 3)],
                     [Moneda(64,142), Moneda(131,116), Moneda(131,67), Moneda (310,50), Moneda (476,82)],
                     30, 40)

    if nivel == 3:
        tiempos.append(round(juego.aladdin.t,1))
        juego = Juego (nivel, [plataforma (0, 140), plataforma (55, 75), plataforma (120, 100),
                             plataforma (195, 75), plataforma (275, 95), plataforma (350, 75),
                             Elevador(450, 70, 200, 4)],
                     [Moneda(16,122), Moneda(136,82), Moneda(291,77), Moneda (475,35), Moneda (75,155)],
                     25, 35)
        
    if nivel == 4:
        tiempos.append(round(juego.aladdin.t,1))
        juego = Juego (nivel, [Elevador(220, 70, 220, 5)],
                     [Moneda(225,35), Moneda(115,25), Moneda(140,150), Moneda (330,20), Moneda (345,130)],
                     20,35)
        
    if nivel == 5:
        tiempos.append(round(juego.aladdin.t,1))
        juego = Juego (nivel, [plataforma (129, 208), plataforma (49, 186), plataforma (100, 134), 
                             plataforma (452, 91), plataforma (482, 135),plataforma (439, 180)],
                    [Moneda(17,152), Moneda(159,65), Moneda(311,76), Moneda (466,39), Moneda (450,157)],
                     15, 15)

    if nivel == 6:
        tiempos.append(round(juego.aladdin.t,1))
        estructura = 'win'
        #win sonido
        pygame.mixer.music.fadeout(50)
        win_s.play()



def main():
    global juego, tiempos, estructura, texto, volume, win_s
#inicializar los graficos
    
    pygame.init()  # incializar los modulos de 
    pygame.font.init()
    FPS = 30      # velocidad del juego.
    fpsClock = pygame.time.Clock()   #Crear objeto cloc usado para gestionar el  tiempo
    height = 300   #altura de la ventana 
    width = 533    # ancho de la ventana 

#posible escalado del juego
    scale = 2
   
    pantalla = pygame.display.set_mode((width, height))   # crear la ventana 
    pygame.display.set_caption("Aladdino")       #nombre de la ventana 
    imagenfondo = pygame.image.load('res/imagenfondo.png').convert() # metodo load de pygame para cargar imagenes
    bg1 = pygame.image.load('res/pausa.png').convert()  # cmabiar el formato de pixeles de la imagen 
    moneda = pygame.image.load('res/moneda.png')
    moneda = pygame.transform.scale(moneda,(14, 14))  # escala de la imagen de moneda
    timer = pygame.image.load('res/time.png')     
    
    win = [0,pygame.image.load('res/Ganador1.png'),pygame.image.load('res/Ganador2.png')]

#juego
    correr = True
    pausa = False

#almacenar el tiempo completo
    tiempos = []
    texto = pygame.font.Font('res/font/04B_03__.TTF', 20)   #formato de texto
    text_big = pygame.font.Font('res/font/04B_03__.TTF', 22)  #formato de texto
#nombre de los jugadores
    letters = []

#puntajesaltos
    puntajesaltos = open('res/puntajesaltos.txt', 'r')
    limit = text_big.render ('',False, (255,0,0))
    high = pygame.image.load('res/PUNTAJES.png')
    names = []

    menu = [0,pygame.image.load('res/Menu1.png'), pygame.image.load('res/Menu2.png'),\
            pygame.image.load('res/Menu3.png'),pygame.image.load('res/Menu4.png'),\
            pygame.image.load('res/Menu5.png')]
    over = [0,pygame.image.load('res/Fin1.png'),pygame.image.load('res/Fin2.png'),\
            pygame.image.load('res/Fin3.png')]
    estructura = 'menu'

#opciones
    opciones = [0,pygame.image.load('res/Opcion1.png'),pygame.image.load('res/Opcion2.png'),pygame.image.load('res/Opcion3.png'),
               pygame.image.load('res/Opcion4.png')]
    musicon = 1
    sfxon = 1
    onoffpick = [pygame.image.load('res/Apagado.png'),pygame.image.load('res/Encendido.png')]
    onoffunpick = [pygame.image.load('res/Apagado.png'),pygame.image.load('res/Encendido.png')]
    volume = 5
    volumepick = [0,pygame.image.load('res/Apagado.png'),pygame.image.load('res/volume_pick_20.png'),
                  pygame.image.load('res/volume_pick_40.png'),pygame.image.load('res/volume_pick_60.png'),
                  pygame.image.load('res/volume_pick_80.png'),pygame.image.load('res/volume_pick_100.png')]
    volumeunpick = [0,pygame.image.load('res/Apagado.png'),pygame.image.load('res/volume_unpick_20.png'),
                  pygame.image.load('res/volume_unpick_40.png'),pygame.image.load('res/volume_unpick_60.png'),
                  pygame.image.load('res/volume_unpick_80.png'),pygame.image.load('res/volume_unpick_100.png')]

#sobre
    historia = [1, pygame.image.load('res/HISTORIA2.png'),pygame.image.load('res/HISTORIA1.png')]
    reglas = [0,pygame.image.load('res/REGLA3.png'),pygame.image.load('res/REGLA2.png'),pygame.image.load('res/REGLA1.png')]
    sobre = [0, pygame.image.load('res/REGLA5.png'),pygame.image.load('res/REGLA4.png')]

#musica

    pygame.mixer.music.load('res/menu_bg.mp3')
    pygame.mixer.music.play(-1, 0.0)

#Sonidos secundarios
 #utilizar el metodo mixer para cargar la musica
    coin_s = pygame.mixer.Sound('res/moneda.wav')
    tick_s = pygame.mixer.Sound('res/tick.wav')
    jump_s = pygame.mixer.Sound('res/jump.wav')
    over_s = pygame.mixer.Sound('res/over.aiff')
    win_s = pygame.mixer.Sound('res/win.wav')
    rock_s = pygame.mixer.Sound('res/rock.wav')
    rock_s.set_volume(0.5)
    tick_s.set_volume(0.5) #ajustando el sonido alto
    
    
#main juego 
    while correr:

        if estructura == "juego":
            colision = pygame.sprite.spritecollide(juego.aladdin, juego.rocks, False)
            if colision:
                if colision[0].vy == 0:
                    colision[0].kill()
                    rock_s.play()
                else:
                    pygame.mixer.music.fadeout(200)
                    over_s.play()
                    estructura = "over"

            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)
            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        juego.aladdin.jump(jump_s)
                    if event.key == pygame.K_p:
                        juego.aladdin.pause_t(pausa)
                        if not pausa:
                            volume /= 2
                            juego.aladdin.message3 = juego.aladdin.text2.render('', False, (255,255,255))
                        else:
                            if juego.aladdin.opacity > 0:
                                juego.aladdin.message3 = juego.aladdin.text2.render('nivel 0' + str(juego.aladdin.nivel), False, (255,255,255))
                            volume *= 2
                        pausa = not pausa
                    if event.key == pygame.K_ESCAPE:
                        estructura = "menu"
                        pygame.mixer.music.load('res/menu_bg.mp3')
                        pygame.mixer.music.set_volume(volume / 5.0)
                        pygame.mixer.music.play(-1, 0.0)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        juego.aladdin.vx = 0


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                juego.aladdin.vx = juego.aladdin.velocidad
            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                juego.aladdin.vx = -juego.aladdin.velocidad


            colision = pygame.sprite.spritecollide(juego.aladdin, juego.spritespisos, False)
            if colision:
                juego.aladdin.vy = 0
                juego.aladdin.y = colision[0].rect.top - juego.aladdin.rect.height + 1
                juego.aladdin.jumpable = True            
            else:
                juego.aladdin.jumpable = False
                if not juego.aladdin.saltando:
                    juego.aladdin.vy = juego.aladdin.falspeed
                    
            
                    
            colision = pygame.sprite.spritecollide(juego.aladdin, juego.spritesparadas, False)
            if colision:
                juego.aladdin.x = colision[0].rect.left -  juego.aladdin.rect.width

            for item in juego.plataforma:
                if pygame.sprite.collide_rect(juego.aladdin,item.tech_sprite_lower) and pygame.sprite.collide_rect(juego.aladdin,item.tech_sprite_upper):
                    juego.aladdin.vy = 0
                    juego.aladdin.y = item.tech_sprite_lower.rect.top - juego.aladdin.rect.height + 1
                    juego.aladdin.jumpable = True

                    if item.__class__.__name__ == 'Elevador':
                        juego.aladdin.vy = 0
                        juego.aladdin.jumpable = True
                        if item.up:
                            juego.aladdin.y = item.tech_sprite_lower.rect.top - juego.aladdin.rect.height + 1 - item.velocidad
                        else:
                            juego.aladdin.y = item.tech_sprite_lower.rect.top - juego.aladdin.rect.height + 1 + item.velocidad
                            
                        
                    

            for item in juego.monedas:
                if pygame.sprite.collide_rect(juego.aladdin,item):
                    item.collect(coin_s)
                    
        


                
            #grupo de caracteres esta hecho para que se coloquen antes del personaje

                pantalla.blit(imagenfondo, (0,0))   #mostar imagen de fondo en la posición 0,0
                juego.sprites.clear(pantalla,imagenfondo)
                juego.character.clear(pantalla,imagenfondo)
                juego.rocks.clear(pantalla,imagenfondo)
                juego.sprites.draw(pantalla)
                juego.character.draw(pantalla)
                juego.rocks.draw(pantalla)
                
                pantalla.blit(juego.aladdin.message3, (85,75))
                pantalla.blit(juego.aladdin.mensaje,(483,257))
                pantalla.blit(juego.aladdin.mensaje3,(483,275))
                pantalla.blit(juego.aladdin.message2,(460,242))
                pantalla.blit(juego.aladdin.advertencia, (300, 150))
                pantalla.blit(moneda, (463,256))
                pantalla.blit(timer, (463,273))

            #Si el juego esta en pausa no antualiza la pantalla
            if not pausa:
                juego.sprites.update()
                juego.character.update()
                juego.rocks.update()
            else:
                pantalla.blit(bg1,(200,100))

            #dibujar sprites para depuracion
            if desarrollador:
                juego.spritespisos.draw(pantalla)
                juego.spritesparadas.draw(pantalla)
            #estrucutra de juego dependiendo de la imagen y deteccion de presion de botones

        if estructura == "menu":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        correr = False
                        pygame.mixer.music.stop()
                        pygame.font.quit()
                        puntajesaltos.close()
                        pygame.quit()
                        os._exit(1)
                        
                    if event.key == pygame.K_DOWN:
                        tick_s.play()
                        menu[0] += 1
                        menu[0] %= 5
                    if event.key == pygame.K_UP:
                        tick_s.play()
                        menu[0] -= 1
                        menu[0] %= 5
                    if event.key == pygame.K_RETURN:
                        if menu[0] == 0:
                            NuevoJuego(1)
                            estructura = "juego"
                        if menu[0] == 1:
                            estructura = "historia"
                        if menu[0] == 2:
                            #el archivo de puntajes es solo de lectura
                            puntajesaltos.close()
                            puntajesaltos = open('res/puntajesaltos.txt', 'r')
                            names = build_highscores([x.split(':') for x in puntajesaltos.read().rstrip('\n').split('\n')])
                            estructura = "high"
                            menu[0] == 0
                        if menu[0] == 3:
                            opciones[0] = 0
                            estructura = "opciones"
                        if menu[0] == 4:
                            correr = False
                            pygame.mixer.music.stop()
                            puntajesaltos.close()
                            pygame.font.quit()
                            pygame.quit()
                            os._exit(1)
                            
            
            pantalla.blit(menu[menu[0]+1], (0,0))

            """* estructuras para identificar en que boton se encuentra *"""

        if estructura == "over":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    puntajesaltos.close()
                    pygame.font.quit()
                    pygame.quit()
                    os._exit(1)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        over[0] += 1
                        over[0] %= 3
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        over[0] -= 1
                        over[0] %= 3
                    if event.key == pygame.K_ESCAPE:
                        estructura = "menu"
                        over_s.fadeout(50)
                        pygame.mixer.music.load('res/menu_bg.mp3')
                        pygame.mixer.music.set_volume(volume / 5.0)
                        pygame.mixer.music.play(-1, 0.0)
                    if event.key == pygame.K_RETURN:
                        if over[0] == 0:
                            NuevoJuego(1)
                            over_s.fadeout(50)
                            estructura = "juego"
                        if over[0] == 1:
                            over_s.fadeout(50)
                            pygame.mixer.music.load('res/menu_bg.mp3')
                            pygame.mixer.music.set_volume(volume / 5.0)
                            pygame.mixer.music.play(-1, 0.0)
                            estructura = "menu"
                            over[0] = 0
                        if over[0] == 2:
                            correr = False
                            pygame.mixer.music.stop()
                            pygame.font.quit()
                            puntajesaltos.close()
                            pygame.quit()
                            os._exit(1)

            pantalla.blit(over[over[0]+1], (0,0))
            #estructura de ganar y detectar que botones son presionados

        if estructura == "win":
            for event in pygame.event.get():
                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)

                elif event.type == pygame.KEYDOWN:
                    if len(pygame.key.name(event.key)) == 1 and len(letters) < 8:
                        letters.append(pygame.key.name(event.key).upper())
                    if event.key == pygame.K_BACKSPACE and len(letters)>0:
                        letters.pop()
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        win[0] += 1
                        win[0] %= 2
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        win[0] -= 1
                        win[0] %= 2
                    if event.key == pygame.K_ESCAPE:
                        win[0] = 0
                        estructura = "menu"
                        win_s.fadeout(50)
                        pygame.mixer.music.load('res/menu_bg.mp3')
                        pygame.mixer.music.set_volume(volume / 5.0)
                        pygame.mixer.music.play(-1, 0.0)

                    if event.key == pygame.K_RETURN:
                        if win[0] == 0:
                            if len(letters) > 3:
                                estructura = "high"
                                puntajesaltos.close()
                                puntajesaltos = open('res/puntajesaltos.txt', 'a')#almacena el nombre del juegador y tiempo
                                puntajesaltos.write(''.join(letters) + ':' + str(sum(tiempos))+'\n')
                                puntajesaltos.close()
                                puntajesaltos = open('res/puntajesaltos.txt', 'r')
                                names = build_highscores([x.split(':') for x in puntajesaltos.read().rstrip('\n').split('\n')])
                                limit = text_big.render ('',False, (255,0,0))
                                win_s.fadeout(50)
                                pygame.mixer.music.load('res/menu_bg.mp3')
                                pygame.mixer.music.set_volume(volume / 5.0)
                                pygame.mixer.music.play(-1, 0.0)
                            else:
                                limit = text_big.render ('___',False, (255,0,0))
                        if win[0] == 1:
                            win[0] = 0
                            estructura = "menu"
                            win_s.fadeout(50)
                            pygame.mixer.music.load('res/menu_bg.mp3')
                            pygame.mixer.music.set_volume(volume / 5.0)
                            pygame.mixer.music.play(-1, 0.0)

                                 
                    
                    

            score = texto.render(str(sum(tiempos)) + 's', False, (255,255,255))
            name = text_big.render (' '.join(letters),False, (255,255,255))

            pantalla.blit(win[win[0]+1], (0,0))
            pantalla.blit(limit, (322,157))
            pantalla.blit(name, (174,182)) 
            pantalla.blit(score,(302,102))

        if estructura == "high":
            
            for event in pygame.event.get():
                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        estructura = "menu"

                    

                
            pantalla.blit(high, (0,0))
            pantalla.blit(names[0][0],(160,130))
            pantalla.blit(names[0][1],(300,130))
            pantalla.blit(names[1][0],(160,150))
            pantalla.blit(names[1][1],(300,150))
            pantalla.blit(names[2][0],(160,170))
            pantalla.blit(names[2][1],(300,170))
            pantalla.blit(names[3][0],(160,190))
            pantalla.blit(names[3][1],(300,190))
            pantalla.blit(names[4][0],(160,210))
            pantalla.blit(names[4][1],(300,210))

        if estructura == "opciones":
            
           for event in pygame.event.get():
            if event.type == QUIT: 
                correr = False
                pygame.mixer.music.stop()
                pygame.font.quit()
                puntajesaltos.close()
                pygame.quit()
                os._exit(1)
            #evento al presionar un  botón
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estructura = "menu"
                if event.key == pygame.K_DOWN:
                    tick_s.play()
                    opciones[0] += 1
                    opciones[0] %= 4
                if event.key == pygame.K_UP:
                    tick_s.play()
                    opciones[0] -= 1
                    opciones[0] %= 4
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if opciones[0] == 0: #posicion de la imagen off en 0
                        tick_s.play()         # reporduciti sonido
                        musicon += 1     
                        musicon %= 2
                    if opciones[0] == 1:
                        print("entra" )
                        tick_s.play()
                        sfxon += 1
                        sfxon %= 2
                if opciones[0] == 2:
                    if event.key == pygame.K_LEFT and volume > 0:
                        tick_s.play()
                        volume -= 1
                    if event.key == pygame.K_RIGHT and volume < 5:
                        tick_s.play()
                        volume += 1
                
                if event.key == pygame.K_RETURN:
                    if opciones[0] == 3:
                        estructura = "menu"

            #moiifcar posicion de imagenes de opciones 
            pantalla.blit(opciones[opciones[0]+1], (0,0))

            if opciones[0] == 0:
                pantalla.blit(onoffpick[musicon],(274,100))
            else:
                pantalla.blit(onoffunpick[musicon],(274,100))
                
            if opciones[0] == 1:
                pantalla.blit(onoffpick[sfxon],(274,126))
            else:
                pantalla.blit(onoffunpick[sfxon],(274,126))

            if opciones[0] == 2:
                pantalla.blit(volumepick[volume+1],(274,154))
            else:
                pantalla.blit(volumeunpick[volume+1],(274,154))
                
#todo el volumen de botones
            if sfxon == 0:
                coin_s.set_volume(0.0)
                tick_s.set_volume(0.0)
                jump_s.set_volume(0.0)
                over_s.set_volume(0.0)
                win_s.set_volume(0.0)
                rock_s.set_volume(0.0)
            else:
                coin_s.set_volume(volume/5.0)
                tick_s.set_volume(volume/10.0)
                jump_s.set_volume(volume/5.0)
                over_s.set_volume(volume/5.0)
                win_s.set_volume(volume/5.0)
                rock_s.set_volume(volume/10.0)

        if musicon == 0:
            pygame.mixer.music.set_volume(0.0)
        else:
            pygame.mixer.music.set_volume(volume/5.0)

                
        if estructura == "historia":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estructura = "menu"
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        tick_s.play()
                        historia[0] += 1
                        historia[0] %= 2
                    if event.key == pygame.K_RETURN:
                        if historia[0] == 0:
                            estructura = "menu"
                        if historia[0] == 1:
                            tick_s.play()
                            estructura = "reglas"
                            reglas[0] = 2

        
            pantalla.blit(historia[historia[0]+1], (0,0))
            
        if estructura == "sobre":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estructura = "menu"
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        tick_s.play()
                        sobre[0] += 1
                        sobre[0] %= 2
                    if event.key == pygame.K_RETURN:
                        if sobre[0] == 0:
                            estructura = "menu"
                        if sobre[0] == 1:
                            tick_s.play()
                            estructura = "reglas"
                            reglas[0] = 1

        
            pantalla.blit(sobre[sobre[0]+1], (0,0))


        if estructura == "reglas":

            for event in pygame.event.get():

                if event.type == QUIT: 
                    correr = False
                    pygame.mixer.music.stop()
                    pygame.font.quit()
                    puntajesaltos.close()
                    pygame.quit()
                    os._exit(1)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estructura = "menu"
                    if event.key == pygame.K_RIGHT:
                        tick_s.play()
                        reglas[0] += 1
                        reglas[0] %= 3
                    if event.key == pygame.K_LEFT:
                        tick_s.play()
                        reglas[0] -= 1
                        reglas[0] %= 3                        
                    if event.key == pygame.K_RETURN:
                        if reglas[0] == 0:
                            estructura = "menu"
                        if reglas[0] == 1:
                            tick_s.play()
                            estructura = "historia"
                            historia[0] = 1
                        if reglas[0] == 2:
                            tick_s.play()
                            estructura = "sobre"
                            sobre[0] = 1

        
            pantalla.blit(reglas[reglas[0]+1], (0,0))
            
                        
        pygame.display.update()
        fpsClock.tick(FPS)  # tiempo transcurrido y velocidad del juego

main()
