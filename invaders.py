import pygame
from pygame.locals import *
import random

TAMANHO_TELA = 640, 480
TELA_JOGO = TAMANHO_TELA[0], TAMANHO_TELA[1] - 64
TAMANHO_NAVE = 64
TAMANHO_BOSS = 80


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        self.imagem = pygame.image.load("imagens/" + self.imagem)
        super(Nave, self). __init__()
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.cor = cor
        self.tx = tx; self.ty = ty
        self.velocidade = 10
        
class Inimigo(Nave):
    def __init__(self, x, y, imagem=None):
        cor = (255, 0,0)
        super(Inimigo, self).__init__(x, y, cor, TAMANHO, TAMANHO, imagem)
        self.velocidade = 5
        self.atirador = False

def atualiza(self):
        self.x += self.velocidade
        if self.x > TAMANHO_TELA[0]:
            self.x = 0
            self.y += TAMANHO + 10
            if self.y >= TAMANHO_TELA[1]:
                print("Voce morreu")
                raise Exception("Voce morreu")
        self.desenha()
        if self.atirador:
            random
            

MAX_TIROS = 10
MAX_INIMIGOS = 32
BOSS = 1
def principal():
    Vidas = 10
    inimigo = Inimigo(0, 0)
    x = TAMANHO_TELA[0] // 2
    y = TAMANHO_TELA[1] - TAMANHO
    nave = Nave(x, y, COR_NAVE, imagem = None)
    velocidade = 10
    tiros = pygame.sprite.Group()
    velocidade_inimigo = 5
    inimigos = pygame.sprite.Group()
    inimigos.add(inimigo)
    contador = 0 
    while True:
        if contador > 30 and len(inimigos) < MAX_INIMIGOS:
            inimigos.add(Inimigo(0, 0))
            contador = 0
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
                        (255, 255,255), 12, 23)
            tiros.add(tiro)

        nave.desenha()

        for inimigo in inimigos:
            inimigo.atualiza()

        for tiro in tiros:
            tiro.atualiza(inimigos)            
        
        pygame.display.flip()
        pygame.time.delay(30)
