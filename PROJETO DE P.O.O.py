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
    Retangulo = pygame.Rect(x, y, w, h)
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
        super().__init__(380, 510, 80, 70, cor, 10, "Sprite Nave Jogador Fase 01.png")
        
    def Movimentar(self):
        teclas = pygame.key.get_pressed()

        direita = int(teclas[pygame.K_RIGHT] or teclas[pygame.K_d])
        esquerda = int(teclas[pygame.K_LEFT] or teclas[pygame.K_a])
        baixo = int(teclas[pygame.K_DOWN] or teclas[pygame.K_s])
        cima = int(teclas[pygame.K_UP] or teclas[pygame.K_w])

        movimento_x = direita - esquerda
        movimento_y = baixo - cima

        self.rect.x += movimento_x * self.velocidade
        self.rect.y += movimento_y * self.velocidade

        self.rect.clamp_ip(DISPLAY.get_rect())

    def Atirar(self):
        tiro = pygame.Rect(
            self.rect.centerx - 5,
            self.rect.top - 20,
            10,
            20
    )
        tirosdoJogador.append(tiro)
        
class Inimigos(Personagem):
    def __init__(self, origem="normal"):
        self.entrandoPeloTopo = False
        if origem == "esquerda":
            x = 0
            y = random.randint(50, 400)
            self_direcao = 1

        elif origem == "direita":
            x = LARGURA - 100
            y = random.randint(50, 400)
            self_direcao = -1

        elif origem == "cima":
            x = random.randint(0, LARGURA - 100)
            y = -80
            self_direcao = random.choice([-1, 1])

            self.entrandoPeloTopo = True
            self.alvoY = random.randint(50, 400)

        else:
            x = random.randint(0, LARGURA - 100)
            y = random.randint(45, 260)
            self_direcao = random.choice([-1, 1])

        super().__init__(
            x, y, 100, 80, VERDE, 2,
            "Sprite inimigo fase 01.png"
        )
        self.direcao = self_direcao

    def Movimentar(self):
        if self.entrandoPeloTopo:
            self.rect.y += 2

            if self.rect.y >= self.alvoY:
                self.rect.y = self.alvoY
                self.entrandoPeloTopo = False
        else:
            self.rect.x += self.velocidade * self.direcao

            if self.rect.left <= 0:
                self.rect.left = 0
                self.direcao = 1

            elif self.rect.right >= LARGURA:
                self.rect.right = LARGURA
                self.direcao = -1
            
class Boss(Personagem):
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
inimigosPendentes = []
ultimoNascimento = 0
tirosdoJogador = []
tirosdosInimigos = []

ChefeDeFase = None
lasers = None

pontos = 0
hordas = 0
tempoInicial = 0
ultimoDisparo = 0
ultimoAtaque = 0
ultimoTiro = 0
ultimaHorda = 0

#FUNÇÕES DE FUNCIONALIDADES DA FASE (O QUE VAI FAZER A FASDE REALMENTE FUNCIONAR E EXIBIR NA TELA)
def CriacaodeHorda(quantidade, pelasBordas=False):
    if pelasBordas:
        novosInimigos = []
        novosInimigos.extend(Inimigos("esquerda") for i in range(5))
        novosInimigos.extend(Inimigos("direita") for i in range (5))
        novosInimigos.extend(Inimigos("cima") for i in range(quantidade - 10))
        random.shuffle(novosInimigos)
        inimigosPendentes.extend(novosInimigos)
    else:
        inimigos.extend(Inimigos() for i in range(quantidade))

    
def IniciandoAFase():
    global jogador, inimigos, tirosdoJogador, tirosdosInimigos
    global ChefeDeFase, lasers, pontos, hordas, tempoInicial
    global ultimoDisparo, ultimoAtaque, ultimoTiro, ultimaHorda
    global inimigosPendentes, ultimoNascimento
    
    jogador = Jogador(corDesejada)
    inimigos  = []
    tirosdoJogador = []
    tirosdosInimigos = []
    ChefeDeFase = None
    lasers = None
    
    pontos = 0
    hordas = 0
    tempoInicial = pygame.time.get_ticks()
    ultimoDisparo = tempoInicial
    ultimoAtaque = tempoInicial
    ultimoTiro = 0
    ultimaHorda = pygame.time.get_ticks()
    inimigosPendentes = []
    ultimoNascimento = pygame.time.get_ticks()
     
    CriacaodeHorda(20)
    
def AtaquesDoBoss(momento):
    global lasers
    larguraJogador = jogador.rect.centerx
    alturaJogador = jogador.rect.centery
    
    larguraInicio = ChefeDeFase.rect.centerx
    alturaInicio = ChefeDeFase.rect.bottom
    
    dx = larguraJogador - larguraInicio
    dy = alturaJogador - alturaInicio
    
    escala = max(LARGURA / abs(dx) if dx != 0 else 0, ALTURA / abs(dy) if dy != 0 else 0) * 2
    fimLargua = larguraInicio + dx * escala 
    fimAltura = alturaInicio + dy * escala
    
    linhas = [(larguraInicio, alturaInicio, fimLargua, fimAltura)]
    lasers = {"linhas": linhas, "inicio": momento, "aviso": 300, "duracao": 2000} 
              
def AtualizarDirecaoLaser():
    if not lasers:
        return
    larguraInicio = ChefeDeFase.rect.centerx
    alturaInicio = ChefeDeFase.rect.bottom
    dx = jogador.rect.centerx - larguraInicio
    dy = jogador.rect.centery - alturaInicio
    
    escala = max(LARGURA / abs(dx) if dx else 0, ALTURA / abs(dy) if dy else 0) * 2
    fimLargura = int(larguraInicio + dx * escala)
    fimAltura = int(alturaInicio + dy * escala)
    
    lasers["linhas"] =  [(larguraInicio, alturaInicio, fimLargura, fimAltura)]
def AtualizarLasers(momento):
    if not lasers:
        return False
    tempo = momento - lasers["inicio"]
    
    if not lasers["aviso"] <= tempo < lasers["aviso"] + lasers["duracao"]:
        return False
    
    AtualizarDirecaoLaser()
    
    for linha in lasers["linhas"]:
        pygame.draw.line(DISPLAY, AMARELO, linha[:2], linha[2:], 25)
        
        if jogador.rect.clipline(linha):
            return True
        
    return False

#BOTÕES: criamos os botões que serão os botões clicáveis no jogo, para que o usuário se mova durante as telas
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
                    telaAtual = "menu"
                    
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
                    telaAtual = "fase2"
                elif botaodeRetorno.collidepoint(mouse):
                    telaAtual = "menu"
                    
            elif telaAtual in ("GameOver", "Vitória"):
                if pygame.Rect(220, 340, 360, 60).collidepoint(mouse):
                    IniciandoAFase()
                    telaAtual = "jogo"
                elif pygame.Rect(220, 420, 360, 60).collidepoint(mouse):
                    telaAtual = "fases"
# FIM DO LOOP PRINCIPAL 
# CONTINUAÇÃO DO LOOP PRINCIPAL, responsável por decidir o que deve acontecer e aparecer na tela em cada mommento do jogo               
    DISPLAY.fill(PRETO)
    if telaAtual == "inicio":
        DISPLAY.blit(tela_inicial, (0, 0))
    
    elif telaAtual == "menu":
        DISPLAY.blit(tela_menu, (0, 0))
    
    elif telaAtual == "naves":
        CriarTexto("NÃO HÁ NENHUMA NAVE DESBLOQUEADA!", FONTEP, BRANCO, 400, 230)
        CriarBotao("VOLTAR", 40, 520, 150, 50, CINZA)
    
    elif telaAtual == "cores":
        CriarTexto("ESCOLHA SUA NAVE", FONTEG, BRANCO, 400, 100)
        CriarTexto("Clique em uma cor para selecioná-la", FONTEP, BRANCO, 400, 165)
        
        for i, (nome, cor) in enumerate(LISTA):
            r = botoesdeCores[i]
            pygame.draw.rect(DISPLAY, cor, r, border_radius=5)
            borda = BRANCO if cor == corDesejada else CINZA
            pygame.draw.rect(DISPLAY, borda, r, 4, border_radius=5)
            CriarTexto(nome, FONTEP, BRANCO, r.centerx, r.bottom + 18)
            
        pygame.draw.rect(DISPLAY, corDesejada, (380, 455, 40, 30))
        CriarTexto("Sua nave", FONTEP, BRANCO, 400, 495)
        CriarBotao("VOLTAR", 40, 520, 150, 50, CINZA)
        CriarBotao("CONTINUAR", 550, 520, 210, 50, VERDE)
        
    elif telaAtual == "fases":
        CriarTexto("ESCOLHA UMA FASE", FONTEG, BRANCO, 400, 130)
        CriarBotao("Fase 01", 150, 260, 220, 75, MARROM)
        CriarBotao("Fase 02", 430, 260, 220, 75, AMARELO)
        CriarBotao("VOLTAR", 40, 520, 150, 50, CINZA)
        
    elif telaAtual == "jogo":
        jogador.Movimentar()
        teclas = pygame.key.get_pressed()
        
        if inimigosPendentes and momento - ultimoNascimento >= 35:
            inimigos.append(inimigosPendentes.pop(0))
            ultimoNascimento = momento
        if teclas[pygame.K_SPACE]:
            if momento - ultimoTiro >= 200:
                jogador.Atirar()
                ultimoTiro = momento

            
        tempodeFase = momento - tempoInicial
        if hordas < 1 and momento - ultimaHorda >= 5000:
            CriacaodeHorda(15 if hordas == 1 else 20, pelasBordas=True)
            hordas += 1
            ultimaHorda = momento
            
        if inimigos and momento - ultimoDisparo >= 800:
            inimigo = random.choice(inimigos)
            
            tirosdosInimigos.append(
                pygame.Rect(
                    inimigo.rect.centerx - 4,
                    inimigo.rect.bottom,
                    8, 12
                )
            )
            ultimoDisparo = momento
            
        for inimigo in inimigos:
            inimigo.Movimentar()
            
        for lista, velocidade in [
            (tirosdoJogador, -9),
            (tirosdosInimigos, 5)
        ]:
            for tiro in lista[:]:
                tiro.y += velocidade

                if tiro.bottom < 0 or tiro.top > ALTURA:
                    lista.remove(tiro)
        for tiro in tirosdoJogador[:]:
            for inimigo in inimigos[:]:
                if tiro.colliderect(inimigo.rect):
                    tirosdoJogador.remove(tiro)
                    inimigos.remove(inimigo)
                    pontos += 100
                    break

                
        if any(t.colliderect(jogador.rect) for t in tirosdosInimigos):
            telaAtual = "GameOver"
            
        if any(i.rect.colliderect(jogador.rect) for i in inimigos):
            telaAtual = "GameOver"
            
        if hordas == 1 and not inimigos and not inimigosPendentes and ChefeDeFase is None:
            ChefeDeFase = Boss()
            ultimoAtaque = momento
            
        if ChefeDeFase and telaAtual == "jogo":
            if not lasers or momento >= lasers["inicio"] + lasers["aviso"] + lasers["duracao"]:
                AtaquesDoBoss(momento)
                
            if AtualizarLasers(momento):
                telaAtual = "GameOver"
                
            for tiro in tirosdoJogador[:]:
                mascara = pygame.mask.Mask(tiro.size, fill=True)
                deslocamento = (
                    tiro.left - ChefeDeFase.rect.left,
                    tiro.top - ChefeDeFase.rect.top
                )
                if ChefeDeFase.mask.overlap(mascara, deslocamento):
                    tirosdoJogador.remove(tiro)
                    ChefeDeFase.vida -= 1
                    
                    if ChefeDeFase.vida <= 0:
                        ChefeDeFase = None
                        lasers = None
                        telaAtual = "Vitoria"
                        break
            
        jogador.Desenhar()
            
        for inimigo in inimigos:
            inimigo.Desenhar()
                
        for tiro in tirosdoJogador:
            for tiro in tirosdoJogador:
                pygame.draw.rect(DISPLAY, (0, 255, 0), tiro)
            
        for tiro in tirosdosInimigos:
            pygame.draw.rect(DISPLAY, VERMELHO, tiro)
                
        if ChefeDeFase:
            ChefeDeFase.Desenhar()
                
        if lasers and ChefeDeFase:
            tempo = momento - lasers["inicio"]
            if tempo < lasers["aviso"]:
                AtualizarDirecaoLaser()
                for linha in lasers["linhas"]:
                    pygame.draw.line(
                            DISPLAY, AZUL, linha[:2], linha[2:], 25
                        )
            
        CriarTexto("Pontos: " + str(pontos), FONTEP, BRANCO, 75, 25)
        CriarTexto("Fase 01", FONTEP, BRANCO, 710, 25)
            
        if ChefeDeFase is None and hordas < 10:
            CriarTexto("Hordas: " + str(hordas) + "/10", FONTEP, BRANCO, 400, 25)
                
        elif ChefeDeFase:
            CriarTexto("BOSS", FONTEP, BRANCO, 400, 250)
                
    elif telaAtual == "fase2":
        CriarTexto("FASE 02 ESTÁ EM DESENVOLVIMENTO", FONTEG, BRANCO, 400, 250)
        CriarBotao("VOLTAR", 40, 520, 150, 50, CINZA)
        
    elif telaAtual == "GameOver":
        CriarTexto("GAME OVER", FONTEG, VERMELHO, 400, 180)
        CriarTexto("PONTUAÇÃO: " + str(pontos), FONTEM, BRANCO, 400, 260)
        CriarBotao("Tentar de Novo", 220, 340, 360, 60, VERDE)
        CriarBotao("Sair da Fase", 220, 420, 360, 60, (220, 100, 80))
        
    elif telaAtual == "Vitoria":
        CriarTexto("VOCÊ VENCEU!!", FONTEG, VERDE, 400, 180)
        CriarTexto("Voce Derrotou o Boss!!", FONTEM, BRANCO, 400, 250)
        CriarTexto("Sua Pontuação:" + str(pontos), FONTEP, BRANCO, 400, 290)
        CriarBotao("Jogar Novamente", 220, 340, 360, 60, VERDE)
        CriarBotao("Voltar às Fases", 220, 420, 360, 60, (80, 150, 220))
        
    pygame.display.flip()
    FPS.tick(60)
            
            
    
    
    
                
                     
        
            
    
        
        
        
