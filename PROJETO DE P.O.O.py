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
        super().__init__(380, 510, 80, 70, cor, 6, "Sprite Nave Jogador Fase 01.png")
        
    def Movimentar(self):
        teclas = pygame.key.get_pressed()
        
        self.rect.x += self.velocidade * (
            teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        ) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
        
        self.rect.y += self.velocidade * (
            teclas[pygame.K_DOWN] or teclas[pygame.K_s]
        ) - (teclas[pygame.K_UP] or teclas[pygame.K_w])
        
        self.rect.clamp_ip(DISPLAY.get_rect())
        
    def Atirar(self):
        tiros_do_Jogador.append(pygame.Rect(self.rect.centerx - 3, self.rect.top - 10,6, 14))
        
class Inimigos(Personagem):
    def __init__(self):
        super().__init__(random.randit(0, LARGURA - 100),
        random.randint(45, 260), 100, 80, VERDE, 2, "Sprite inimigo fase 01.png"                 
        )
        self.direcao = random.choice([-1,1])
        
    def Movimentar(self):
        self.rect.x += self.velocidade * self.direcao
        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self.direcao *= -1
            
class ChefeDeFase(Personagem):
    def __init__(self):
        super().__init__(-50, -300, 900, 600, MARROM, 0, "nave boss teste.png")
        self.vida = 100
        self.vida_maxima = 100
        self.mask = pygame.mask.from_surface(self.image)
        
    def Desenhar(self):
        super().Desenhar() 
        x = (LARGURA - 300) // 2
        pygame.draw.rect(DISPLAY, VERMELHO, (x, 20, 300, 15))
        vida = int(300 * self.vida / self.vida_maxima)
        pygame.draw.rect(DISPLAY, VERDE, (x, 20, vida, 15))
        
# CRIANDO AS VARIÁVEIS DO CÓDIGO
# criamos as variáveis referentes ao ataques do jogador, dos inimigos, a quantidade de horas
# e até mesmo das telas e das cores (utilizando a lista)
telaAtual = 'inicio'
corDesejada = LISTA[0][1]

jogador = None
inimigos = []
tirosdoJogador = []
tirosdosInimigos = []

ChefeDeFase = None
lasers = None

pontos = 0
hordas = 0
tempoInicial = 0
ultimoTiro = 0
ultimoDisparo = 0
ultimoAtaque = 0

#FUNÇÕES DE FUNCIONALIDADES DA FASE (O QUE VAI FAZER A FASDE REALMENTE FUNCIONAR E EXIBIR NA TELA)
def CriacaodeHorda(quantidade):
    inimigos.extend(Inimigos() for i in range(quantidade))
    
def IniciandoAFase():
    global jogador, inimigos, tirosdoJogador, tirosdosInimigos
    global ChefeDeFase, lasers, pontos, hordas, tempoInicial
    global ultimoTiro, ultimoDisparo, ultimoAtaque
    
    jogador = Jogador(corDesejada)
    inimigos  = []
    tirosdoJogador = []
    tirosdosInimigos = []
    ChefeDeFase = None
    lasers = None
    
    pontos = 0
    hordas = 0
    tempoInicial = pygame.time.get_ticks()
    ultimoTiro = 0
    ultimoDisparo = tempoInicial
    ultimoAtaque = tempoInicial
    
    CriacaodeHorda(20)
    
def AtaquesDoBoss(momento):
    global lasers
    
    if random.choice([True, False]):
        y1 = ChefeDeFase.rect.y + 355
        y2 = ChefeDeFase.rect.y + 480
        linhas = [(0, y1, LARGURA, y1), (0, y2, LARGURA, y2)]
    else:
        linhas = [
            (ChefeDeFase.rect.left, ChefeDeFase.rect.bottom, 0, ALTURA),
            (ChefeDeFase.rect.right, ChefeDeFase.rect.bottom, LARGURA, ALTURA),
            (ChefeDeFase.rect.left, ChefeDeFase.rect.y, LARGURA, ALTURA),
            (ChefeDeFase.rect.right, ChefeDeFase.rect.y, 0, ALTURA)
        ]
        
    lasers = {"linhas": linhas, "inicio": momento, "aviso": 900, "duracao": 450 }
    
def AtualizarLasers(momento):
    if not lasers:
        return False
    tempo = momento - lasers["inicio"]
    
    if not lasers["aviso"] <= tempo < lasers["aviso"] + lasers["duracao"]:
        return False
    
    for linha in lasers["linhas"]:
        pygame.draw.line(DISPLAY, VERMELHO, linha[:2], linha[2:], 8)
        
        if jogador.rect.clipline(linha):
            return True
        
    return False

#BOTÕES: criamos os botões que serão os botões clicáveis no jogo, para que o usuário se mova durante as telas
botaodePlay = pygame.Rect(325, 345, 155, 153)
botaodeCores = pygame.Rect(95, 325, 140, 130)
botaodeJogar = pygame.Rect(345, 325, 115, 125)
botaodeNaves = pygame.Rect(575, 325, 130, 130)
botaodeRetorno = pygame.Rect(40, 520, 150, 50)
botaodeContinuar = pygame.Rect(550, 520, 210, 50)

botoesdeCores = [
    pygame.Rect(180 + (i % 3) * 220,
                200 + (i // 3) * 85, 55, 45)
    for i in range(len(LISTA))
]
    
# LOOP PRINCIPAL DO JOGO: o loop principal (while) é uma, se não a parte mais importante do jogo, pois é aqui que sintetizaos
# todas as funções, botões, classe para que o jogo fique atualizando em tempo real e consiga funcionar corretamento
while True:
    momento = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse = evento.pos
             
            if telaAtual == "inicio":
                if botaodeJogar.collidepoint(mouse):
                    telaAtual = "menu"
            
            elif telaAtual == "menu":
                if botaodeCores.collidepoint(mouse):
                    telaAtual = "cores"
                    
                elif botaodeJogar.collidepoint(mouse):
                    telaAtual = "fases"
                    
                elif botaodeNaves.collidepoint(mouse):
                    telaAtual = "naves"
                    
            elif telaAtual == "naves":
                if botaodeRetorno.collidepoint(mouse):
                    telaAtual == "menu"
                    
            elif telaAtual == "cores":
                for i, r in enumerate(botoesdeCores):
                    if r.collidepoint(mouse):
                        corDesejada = LISTA[i][1]
                        
            if botaodeRetorno.collidepoint(mouse):
                telaAtual = "menu"
            elif botaodeContinuar.collidepoint(mouse):
                telaAtual = "fases"
                
            elif telaAtual == "fases":
                if pygame.Rect(150, 260, 220, 75).collidepoint(mouse):
                    IniciandoAFase()
                    telaAtual = "jogo"
                elif pygame.Rect(430, 260, 220, 75).collidepoint(mouse):
                    telaAtual == "fase2"
                elif botaodeRetorno.collidepoint(mouse):
                    telaAtual = "menu"
                    
            elif telaAtual in ("GameOver", "Vitória"):
                if pygame.Rect(220, 340, 360, 60).collidepoint(mouse):
                    IniciandoAFase()
                    telaAtual = "jogo"
                elif pygame.Rect(220, 420, 360, 60).collidepoint(mouse):
                    telaAtual = "fases"
                    
DISPLAY.fill(PRETO)

if telaAtual == "inicio":
    DISPLAY.blit(inicio, (0, 0))
    
elif telaAtual == "menu":
    DISPLAY.blit(menu, (0, 0))
    
elif telaAtual == "naves":
    CriarTexto("NÃO HÁ NENHUMA NAVE DESBLOQUEADA!", FONTEP, BRANCO, 400, 230)
    CriarBotao("VOLTAR", 40, 520, 150, 50, CINZA)
    
elif telaAtual == "cores":
    CriarTexto("ESCOLHA SUA NAVE", FONTEG, BRANCO, 400, 100)
    CriarTexto("Clique em uma cor para selecioná-la", FONTEP, BRANCO, 400, 165)
                
                     
        
            
    
        
        
        
