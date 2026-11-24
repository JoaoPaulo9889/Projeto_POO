# IMPORTAÇÕES: importamos o pygame para podermos dar início a programação do jogo, pois é a biblioteca responsável por isso. 
# Importamos a biblioteca Random pois ela nos permite gera números e escolhas aleatórias
# Importamos a biblioteca sys pois nos permite encerrar o programa e importamos a biblioteca OS para trabalharmos com os arquivos do computador.
import pygame
import random
import sys
import os 

# Iniciar a Biblioteca Pygame
pygame.init()

# CONFIGURAÇÕES DA TELA: damos valores para a altura e largura e usamos esses valores para criar a tela do jogo.
# Também colocamos o nome do jogo na guia e criamos o relógio para controlar o FPS do jogo
# também guardamos o endereço da pasta para facilitar de encontrar as imagens 
LARGURA, ALTURA = 800, 600
DISPLAY = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CANGAÇO ESPACIAL")
FPS = pygame.time.Clock()
PASTA = os.path.dirname(os.path.abspath(__file__))

# CORES: As cores são formadas de níveis de RGB (Red/Green/Blue), e dando valores para as três (sendo 0 = nada e 255 = tudo)
# nós conseguimos criar outras cores.
PRETO = (10, 10, 25)
LARANJA = (255, 160, 0)
VERDE = (0, 255, 100)
VERMELHO = (255, 60, 60)
AZUL = (0, 150, 255)
CINZA = (100, 100, 120)
AMARELO = (255, 230, 50)
MARROM = (139, 69, 19)
ROSA = (255, 100, 190)
BRANCO = (255, 255, 255)

# FONTES: Colocamos os atributos das cores, como: qual a fonte, seu tamanho, e se ela será em negrito ou não
# criamos 03 tipos de fontes, cada uma com tamanhos diferentes
FONTEG = pygame.font.SysFont("arial", 40)
FONTEM = pygame.font.SysFont("arial", 27)
FONTEP = pygame.font.SysFont("arial", 23)

# LISTA DE CORES (TUPLA): criamos uma tupla ( que não pode ser alterada diretamente ), criamos esta lista para que 
# o jogador possa fazer a escolha de cores da nave
LISTA = [
    ("AMARELO", (255, 230, 50)),
    ("AZUL", (0, 150, 255)),
    ("VERDE", (0, 255, 100)),
    ("VERMELHO", (255, 60, 60)),
    ("ROXO", (180, 70, 255)),
    ("ROSA", (255, 100, 190)),
    ("CINZA", (100, 100, 120)),
    ("LARANJA", (255, 160, 0)),
    ("MARROM",MARROM)
]

# FUNÇÕES (DEF) PARA IMPORTAR AS IMAGENS: Utilizamos a biblioteca os para acessaremos os arquivos do computador para importar as imagens
# a primeira funcção importa e redimensiona as imagens dos inimigos/oponetes e chefes e a segunda função chama a primeira ajusta as imagens de funso pára que fiquem em toda a tela
def importarImagem(nome, tamanho=None, fundo=False):
    imagem = pygame.image.load(
        os.path.join(PASTA, nome)
    ).convert() if fundo else pygame.image.load(
        os.path.join(PASTA, nome)
    ).convert_alpha()
    
    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)
        
    return imagem
        
def ImagemFundo(nome):
    imagem = importarImagem(nome, fundo=True)
    escala = max(LARGURA / imagem.get_width(),
                 ALTURA / imagem.get_height())
    
    tamanho = (
        int(imagem.get_width() * escala),
        int(imagem.get_height() * escala)
    )
    
    imagem = pygame.transform.smoothscale(imagem, tamanho)
    
    x = (imagem.get_width() - LARGURA) // 2
    y = (imagem.get_height() - ALTURA) // 2
    
    return imagem.subsurface((x, y, LARGURA, ALTURA))

tela_inicial = ImagemFundo("Tela Inicial Cangaço Espacial.jpg")
tela_menu = ImagemFundo("Tela de escolhas Cangaço Espacial.jpg")

# FUNÇÕES DE CRIAÇÕES NA TELA: criamos uma função que exibe mensagens de texto na tela do programa e uma função que cria botões na tela do programa
def CriarTexto(mensagem, fonte_utilizada, cor, x, y):
    imagem = fonte_utilizada.render(mensagem, True, cor)
    DISPLAY.blit(imagem, imagem.get_rect(center=(x, y)))
    
def CriarBotao(mensagem, x, y, w, h, cor):
    Retangulo = pygame.rect(x, y, w, h)
    pygame.draw.rect(DISPLAY, cor, Retangulo, border_radius=10)
    pygame.draw.rect(DISPLAY, BRANCO, Retangulo, 2, border_radius=10)
    CriarTexto(mensagem, FONTEM, PRETO, Retangulo.centerx, Retangulo.centery)
    return Retangulo

# CRIAÇÃO DE CLASSES: 
# CLASSE PERSONAGEM - 
class Personagem:
    def __init__(self, x, y, w, h, cor, velocidade, sprite=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.cor = cor
        self.velocidade = velocidade
        self.image = importarImagem(sprite, self.rect.size) if sprite else None
        
    def Desenhar(self):
        if self.image:
            DISPLAY.blit(self.image, self.rect)
        else:
            pygame.draw.rect(DISPLAY, self.cor, self.rect, border_radius=5)
            
class Jogador(Personagem):
    def __init__(self, cor):
        super().__init__(380, 510, 80, 70, cor, 6, "Sprite inimigo fase 01.png")
        
    def Movimentar(self):
        teclas = pygame.key.get_pressed()
        
        self.rect.x += self.velocidade * (
            teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        ) 