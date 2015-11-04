import pygame
from pygame.locals import *
import random

TAMANHO_TELA = 640, 480
TAMANHO = 64
COR_NAVE = (0, 128, 255)
VELOCIDADE = 5
MAX_TIROS = 5
WEAPON = 500000


boosts = pygame.sprite.Group()

def init():
    global TELA, FONTE
    pygame.init()
    FONTE = pygame.font.Font("sans.ttf", 48)
    FONTE.set_bold(True)
    TELA = pygame.display.set_mode(TAMANHO_TELA)
    
def atualiza_pontos():
    pontos = nave.pontos
    texto = "{:05d}".format(pontos)
    img = FONTE.render(texto, True, (255,255,255))
    TELA.blit(img, (0, TAMANHO_TELA[1] - img.get_height()))

class Nave(pygame.sprite.Sprite):
    
    def __init__(self, x, y, cor, tx=TAMANHO, ty=TAMANHO, imagem=None):
        super(Nave, self).__init__()
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.cor = cor
        self.tx = tx; self.ty = ty
        self.velocidade = 10
            
        self.carregar(imagem)
        self.pontos = 0
     
    def carregar(self, imagem):
        if not imagem:
            self.imagem = None
            return
           
        self.imagem = pygame.image.load("imagens/" + imagem)
     
    def apaga(self):
    	return 
        pygame.draw.rect(TELA, (0,0,0), (self.ox, self.oy, self.tx, self.ty) )
        
    def kill(self):
        self.apaga()
        super(Nave, self).kill()
        
    def desenha(self):
        self.rect = pygame.Rect ( (self.x, self.y, self.tx,self.ty) )
        self.apaga()
        if not self.imagem:
            pygame.draw.rect(TELA, self.cor, self.rect)
        else:
            TELA.blit(self.imagem, self.rect)
        self.ox = self.x
        self.oy = self.y
        if self.__class__ is Nave:
            atualiza_pontos()
        
            
class Boost(Nave):
    
    def __init__(self, x, y, imagem="bonusarma.png"):
        cor = (200, 0, 200)
        super(Boost, self).__init__(x, y, cor, TAMANHO, TAMANHO, imagem)
        self.velocidade = VELOCIDADE
        
    def atualiza(self, nave):
        global WEAPON
        self.y += self.velocidade
        self.desenha()
        
        if self.rect.colliderect(nave.rect):
            self.kill()
            WEAPON += 5
            
        
class Tiro(Nave):   
    def atualiza(self, inimigos):
        self.y -= self.velocidade
        self.desenha()
        if self.y < 0:
            self.kill()
        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect):
                self.kill()
                inimigo.health -= WEAPON
                if inimigo.health < 1:
                    inimigo.kill()
                    nave.pontos += inimigo.valor
                    if inimigo.boss:
                        boost = Boost(inimigo.x, inimigo.y)
                        boosts.add(boost)
                                       
               
imagem_fundo = pygame.image.load ("imagens/fundo.png")                
def fundo (tela):
   tela.blit(imagem_fundo, (0,0))


class Inimigo(Nave):
    health = 30
    boss = False
    valor = 1
    
    def __init__(self, x, y, imagem="spaceinvaders4.png"):
        cor = (200, 0,200)
        super(Inimigo, self).__init__(x, y, cor, TAMANHO, TAMANHO, imagem)
        self.velocidade = VELOCIDADE

        
    def atualiza(self):
        self.x += self.velocidade
        if self.x > TAMANHO_TELA[0]:
            self.x = 0
            self.y += TAMANHO + 10
            if self.y >= TAMANHO_TELA[1]:
                print("Voce morreu")
                raise Exception("Voce morreu")
        self.desenha()


class Boss(Inimigo):
    health = 140
    boss = True
    valor = 10
    def __init__(self, x, y):
        cor = (200, 0, 200)
        super(Boss, self).__init__(x, y, "boss_0_0.png")

    
def principal():
    global nave
    x = TAMANHO_TELA[0] // 2
    y = TAMANHO_TELA[1] - TAMANHO
    nave = Nave(x, y, COR_NAVE, imagem="nave.png")
    velocidade = 10
    tiros = pygame.sprite.Group()
    velocidade_inimigo = 5
    inimigos = pygame.sprite.Group()
    contador = 31
    onda = 0
     
    criar_inimigos = {"base": 2, "criados": 0, "forca": 30}
    criando_inimigos = True

    while True:
        if contador > 30 and criando_inimigos:
   
            inimigo = Inimigo(0,0)
            inimigo.health = criar_inimigos["forca"]
            inimigos.add(inimigo)
            criar_inimigos["criados"] += 1
            if criar_inimigos["criados"] >= criar_inimigos["base"]:
                criando_inimigos = False
            contador = 0
            
        if not inimigos:
            onda += 1
            contador = 31
            if onda % 2:
            
                inimigos.add(Boss(0, 0))
            else:
                criar_inimigos["base"] += 5
                criar_inimigos["forca"] += 10
                criar_inimigos["criados"] = 0
                criando_inimigos = True
            
        contador += 1
        pygame.event.pump()
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            nave.x -= velocidade
        elif teclas[K_RIGHT]:
            nave.x += velocidade
        if teclas[K_ESCAPE]:
            break
        if teclas[K_SPACE] and len(tiros) <= MAX_TIROS:
            tiro = Tiro(nave.x + TAMANHO//2, TAMANHO_TELA[1] - TAMANHO,
                        (255, 255,255), 4, 4)
            tiros.add(tiro)
            
        fundo(TELA)

        nave.desenha()
        
        for b in boosts:
            b.atualiza(nave)
        
        for inimigo in inimigos:
            inimigo.atualiza()

        for tiro in tiros:
            tiro.atualiza(inimigos)
        
        pygame.display.flip()
        pygame.time.delay(30)

try:
    init()
    principal()
finally:
    pygame.quit()
