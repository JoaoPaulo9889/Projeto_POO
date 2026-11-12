# Imortamos as bibliotecas que serão utilizadas durante o programa, o pygame é importado 
# pois o objetivo do projeto é criar um jogo com uma interface gráfica, o random é importado
# para que pudessemos gerar valores aleatórios diferenciando os movimentos e tiros dos inimigos.
# O sys é importado para que disponibilize funcionalidades ligadas ao próprio python, como o encerramento do 
# programa.
# 
import pygame
import random 
import sys 
import os

# utilizamos pygame.init() para iniciar, "acordar" a biblioteca pygame para qualquer coisa que faremos a
# seguir (Mesmo que importemos a biblioteca, temos que inicia-la com o pygame.init())
pygame.init()

# Criamos a tela/guia onde será executado o jogo, setamos a largura e a altura e a utilizamos para 
# definir o tamanho da tela. Utilizamos também o set_caption para por o nome do jogo no topo da guia/tela.
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cangaço Espacial")

# criamos a variável fps para definir em quantos frames por segundo o nosso programa irá rodar,
# para evitar que trave ou as animações fiquem incorretas. Utilizaremos novamente mais para frente
fps = pygame.time.Clock()

# criamos as cores que serão utilizadas durante o jogo para diferenciar os inimigos do jogador, dar cor  
# aos tiros do jogador e, para que o usuário possa escolher qual a cor de sua nave ele irá querer usar.
# As cores funcionam com base em R(red) G(green) B(blue), sendo 0 a inexistência da cor e 255 a cor em sua
# maior potência, com isso pesquisamos os valores do RGB que formem as seguintes cores: 
    
CorPreta = (10, 10, 25)
CorBranca = (255, 255, 255)
CorVerde = (0, 255, 100)
CorVermelha = (255, 60, 60)
CorAzul = (0, 150, 255)
CorCinza = (100, 100, 120)
CorAmarela = (255, 230, 50)

# criamos as variáveis das fontes que desejamos utilizar na interface do código, utilizamos a fonte IMPACT
# com 3 tamanhos distintos e em negrito, utilizamos a função SysFont que busca uma fonte do S.O
fonte = pygame.font.SysFont('impact', 22, bold = True)
fonteMedia = pygame.font.SysFont('impact', 19)
fontePequena = pygame.font.SysFont('impact', 15)

lista_de_cores = []


