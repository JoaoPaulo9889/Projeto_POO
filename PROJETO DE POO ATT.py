
import pygame
import random
import sys
import os 

pygame.init()

# CONFIGURACOES
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CANGAÇO ESPACIAL")


# Carrega a imagem original da tela inicial
caminho_imagem_inicio = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Tela Inicial Cangaço Espacial.jpg"
)

imagem_original = pygame.image.load(
    caminho_imagem_inicio
).convert()

# Obtém as dimensões originais
largura_original = imagem_original.get_width()
altura_original = imagem_original.get_height()


# Calcula a escala para preencher toda a janela
escala = max(
    LARGURA / largura_original,
    ALTURA / altura_original
)

# Calcula as novas dimensões
largura_imagem = int(largura_original * escala)
altura_imagem = int(altura_original * escala)

# Redimensiona a imagem proporcionalmente
imagem_inicio = pygame.transform.smoothscale(
    imagem_original,
    (largura_imagem, altura_imagem)
)

# Calcula o corte central da imagem
corte_x = (largura_imagem - LARGURA) // 2
corte_y = (altura_imagem - ALTURA) // 2

# Recorta a imagem para preencher a janela
imagem_inicio = imagem_inicio.subsurface(
    (corte_x, corte_y, LARGURA, ALTURA)
)

# A imagem começa no canto superior esquerdo
posicao_imagem = (0, 0)

botao_de_play = pygame.Rect(325, 345, 155, 153)

# MENU DE CAMINHOS
menu_de_caminhos = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Tela de escolhas Cangaço Espacial.jpg"
)

imagem_do_menu = pygame.image.load(
    menu_de_caminhos
).convert()

tamanho_menu = max(
    LARGURA / imagem_do_menu.get_width(),
    ALTURA / imagem_do_menu.get_height()
)

largura_menu = int(
    imagem_do_menu.get_width() * tamanho_menu
)

altura_menu = int(
    imagem_do_menu.get_height() * tamanho_menu
)

imagem_menu = pygame.transform.scale(
    imagem_do_menu,
    
    
    (largura_menu, altura_menu)
)

corte_x = (largura_menu - LARGURA) // 2
corte_y = (altura_menu - ALTURA) // 2

imagem_menu = imagem_menu.subsurface(
    (corte_x, corte_y, LARGURA, ALTURA)
)

posicao_do_menu = (0, 0)

relogio = pygame.time.Clock()

PRETO = (10, 10, 25)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 100)
VERMELHO = (255, 60, 60)
AZUL = (0, 150, 255)
CINZA = (100, 100, 120)
AMARELO = (255, 230, 50)
LARANJA = (255, 160, 0)
MARROM = (139, 69, 19)

fonte = pygame.font.SysFont("arial", 38, bold=True)
fonte2 = pygame.font.SysFont("impact", 38, bold=True)
media = pygame.font.SysFont("arial", 27)
pequena = pygame.font.SysFont("arial", 20)

cores = [
    ("Amarelo", (255, 255, 0)),
    ("Azul", (0, 120, 255)),
    ("Verde", (0, 255, 100)),
    ("Vermelho", (255, 60, 60)),
    ("Roxo", (180, 70, 255)),
    ("Rosa", (255, 100, 190)),
    ("Ciano", (0, 255, 255)),
    ("Laranja", (255, 160, 0)),
    ("Marrom", (139, 69, 19)),
    
]

tela_atual = "inicio"
cor_escolhida = cores[0][1]

# VARIÁVEIS FASE 01
jogador = []
inimigos = []
tiros_jogador = []
tiros_inimigos = []

boss = None
lasers = []

pontos = 0
hordas_lancadas = 0
tempo_inicio = 0
ultimo_tiro = 0
ultimo_disparo_inimigo = 0
ultimo_ataque_boss = 0


# VARIÁVEIS FASE 02
usuario = None
inimigo_basico = []
tiros_usuario = []
tiros_inimigo = []

pontos_usuario = 0
hordas_inimigos = 0
tempo_inicial = 0
ultimo_inimigo = 0


# FUNCOES DE INTERFACE

def texto(mensagem, fonte_usada, cor, x, y):
    imagem = fonte_usada.render(mensagem, True, cor)
    retangulo = imagem.get_rect(center=(x, y))
    tela.blit(imagem, retangulo)


def botao(mensagem, x, y, largura, altura, cor):
    retangulo = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, cor, retangulo, border_radius=10)
    pygame.draw.rect(tela, BRANCO, retangulo, 2, border_radius=10)
    texto(mensagem, media, PRETO,
          retangulo.centerx, retangulo.centery)
    return retangulo


# CLASSES

class Personagem():
        
    
    def __init__(self, x, y, largura, altura, cor, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
        self.velocidade = velocidade

    def desenhar(self):
        pygame.draw.rect(
            tela, self.cor, self.rect, border_radius=5
        )


class Jogador(Personagem):
    def __init__(self, cor):
        super().__init__(380, 510, 80, 70, cor, 6)

        caminho_sprite = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sprite teste.png"
        )

        imagem_original = pygame.image.load(
            caminho_sprite
        ).convert_alpha()

        self.image = pygame.transform.scale(
            imagem_original,
            (self.rect.width, self.rect.height)
        )

    def mover(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        self.rect.clamp_ip(tela.get_rect())

    def desenhar(self):
        tela.blit(self.image, self.rect)

    def atirar(self):
        tiro = pygame.Rect(
            self.rect.centerx - 3,
            self.rect.top - 10,
            6, 14
        )
        tiros_jogador.append(tiro)


class Inimigo(Personagem):
    def __init__(self):
        x = random.randint(0, LARGURA - 35)
        y = random.randint(45, 260)

        super().__init__(x, y, 100, 80, VERDE, 2)

        self.direcao = random.choice([-1, 1])
        
        sprite_inimigo = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "nave inimigo teste.png"
        )
        
        imagem_og = pygame.image.load(
                sprite_inimigo
        ).convert_alpha()
        
        self.image = pygame.transform.scale(
            imagem_og,
            (self.rect.width, self.rect.height)
        )

    def mover(self):
        self.rect.x += self.velocidade * self.direcao

        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self.direcao *= -1
            
    def desenhar(self):
        tela.blit(self.image, self.rect)

# CLASSE REFERENTE AO JOGADOR DA FASE 02
class Usuario(Personagem):
    def __init__(self, cor):
        super().__init__(380, 510, 80, 70, cor, 6)
        
        def teclas_mover(self):
            teclas = pygame.key.get_pressed()
            
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.rect.x -= self.velocidade
                
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.rect.x -= self.velocidade
                
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.rect.y -= self.velocidade

            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.rect.y += self.velocidade

            self.rect.clamp_ip(tela.get_rect())
            
        def desenhar(self):
            pygame.draw.rect(tela, AZUL, self.rect )

class Boss(Personagem):
    
    def __init__(self):
        # Define o tamanho e a posição do Boss
        super().__init__(
            -50, -300, 900, 600,
            (150, 40, 200), 0
        )

        # Vida do Boss
        self.vida = 30
        self.vida_maxima = 30

        # Localiza a imagem do Boss
        sprite_boss = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "nave boss teste.png"
        )

        # Carrega a imagem original
        imagem_original = pygame.image.load(
            sprite_boss
        ).convert_alpha()

        # Redimensiona a imagem para o tamanho do Boss
        self.image = pygame.transform.scale(
            imagem_original,
            (self.rect.width, self.rect.height)
        )

        # Cria a máscara para detectar colisões
        self.mask = pygame.mask.from_surface(self.image)

        

    def desenhar(self):
    # Desenha a imagem do Boss
        tela.blit(self.image, self.rect)

        # Barra de vida
        largura_barra = 300
        altura_barra = 15
        x_barra = (LARGURA - largura_barra) // 2
        y_barra = 20

        pygame.draw.rect(
            tela,
            VERMELHO,
            (x_barra, y_barra, largura_barra, altura_barra)
        )

        vida_atual = int(
            largura_barra * self.vida / self.vida_maxima
        )

        pygame.draw.rect(
            tela,
            VERDE,
            (x_barra, y_barra, vida_atual, altura_barra)
        )

# HORDAS E INICIO DA FASE

def criar_horda(quantidade):
    for i in range(quantidade):
        inimigos.append(Inimigo())


def iniciar_fase():
    global jogador, inimigos
    global tiros_jogador, tiros_inimigos
    global boss, lasers, pontos
    global hordas_lancadas, tempo_inicio
    global ultimo_tiro, ultimo_disparo_inimigo
    global ultimo_ataque_boss

    jogador = Jogador(cor_escolhida)

    inimigos = []
    tiros_jogador = []
    tiros_inimigos = []
    lasers = []

    boss = None
    pontos = 0
    hordas_lancadas = 0

    tempo_inicio = pygame.time.get_ticks()
    ultimo_tiro = 0
    ultimo_disparo_inimigo = tempo_inicio
    ultimo_ataque_boss = tempo_inicio

    # A primeira horda aparece imediatamente
    criar_horda(10)
    hordas_lancadas = 1
    
# INÍCIO DA FASE 02
# FUNÇÕES DA FASE 02

def gerar_inimigos(quantidade):
    for sim in range(quantidade):
        inimigo_basico.append(Inimigo(Personagem))


def iniciar_fase2():

    global usuario, inimigo_basico
    global tiros_usuario, tiros_inimigo
    global hordas_inimigos, tempo_inicial
    global ultimo_tiro, ultimo_inimigo
    global pontos_usuario

    usuario = Usuario(AZUL)

    inimigo_basico = []
    tiros_usuario = []
    tiros_inimigo = []

    pontos_usuario = 0
    hordas_inimigos = 0

    tempo_inicial = pygame.time.get_ticks()
    ultimo_tiro = 0
    ultimo_inimigo = 0

    gerar_inimigos(12)
    hordas_inimigos = 1


# ATAQUES DO BOSS

def criar_ataque_boss(agora):
    global lasers

    linhas = []

    # Ataques horizontais que saem dos lados do Boss
    if random.choice([True, False]):
        y1 = boss.rect.y + 355
        y2 = boss.rect.y + 480

        linhas.append((0, y1, LARGURA, y1))
        linhas.append((0, y2, LARGURA, y2))

    else:
        # Ataques diagonais que partem do Boss
        linhas.append((
            boss.rect.left, boss.rect.bottom,
            0, ALTURA
        ))

        linhas.append((
            boss.rect.right, boss.rect.bottom,
            LARGURA, ALTURA
        ))

        linhas.append((
            boss.rect.left, boss.rect.y,
            LARGURA, ALTURA
        ))

        linhas.append((
            boss.rect.right, boss.rect.y,
            0, ALTURA
        ))

    lasers = {
        "linhas": linhas,
        "inicio": agora,
        "aviso": 900,
        "duracao": 450
    }


def desenhar_lasers(agora):
    if not lasers:
        return

    tempo = agora - lasers["inicio"]

    # Azul = aviso para o jogador desviar
    # Vermelho = laser ativo e perigoso
    if tempo < lasers["aviso"]:
        cor = AZUL
        espessura = 4
    elif tempo < lasers["aviso"] + lasers["duracao"]:
        cor = VERMELHO
        espessura = 8
    else:
        return

    for linha in lasers["linhas"]:
        pygame.draw.line(
            tela, cor,
            (linha[0], linha[1]),
            (linha[2], linha[3]),
            espessura
        )

def jogador_atingido_pelo_laser(agora):
    if not lasers:
        return False

    tempo = agora - lasers["inicio"]

    # Durante o aviso azul, o laser ainda nao causa dano
    if tempo < lasers["aviso"]:
        return False

    if tempo >= lasers["aviso"] + lasers["duracao"]:
        return False

    for linha in lasers["linhas"]:
        if jogador.rect.clipline(linha):
            return True

    return False


# BOTOES DAS TELAS

botoes_cores = []
botao_cores_menu = pygame.Rect(95, 325, 140, 130)
botao_jogar_menu = pygame.Rect(345, 325, 115, 125)
botao_naves_menu = pygame.Rect(575, 325, 130, 130)
botao_retorno_naves = pygame.Rect(40, 520, 150, 50)

botoes_cores = []

for i in range(len(cores)):
    x = 180 + (i % 3) * 220
    y = 200 + (i // 3) * 85

    botoes_cores.append(
        pygame.Rect(x, y, 55, 45)
    )

botao_voltar_cores = pygame.Rect(40, 520, 150, 50)
botao_continuar = pygame.Rect(550, 520, 210, 50)

botao_fase = pygame.Rect(150, 260, 250, 75)
botao_fase2 = pygame.Rect(430, 260, 220, 75)
botao_voltar_fases = pygame.Rect(40, 520, 150, 50)

botao_tentar = pygame.Rect(220, 340, 360, 60)
botao_sair_fase = pygame.Rect(220, 420, 360, 60)


# LOOP PRINCIPAL

while True:
    agora = pygame.time.get_ticks()
    
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                mouse = evento.pos

                # TELA INICIAL
                if tela_atual == "inicio":
                    if botao_de_play.collidepoint(mouse):
                        tela_atual = "menu"

                # MENU DE CAMINHOS
                elif tela_atual == "menu":

                    if botao_cores_menu.collidepoint(mouse):
                        tela_atual = "cores"

                    elif botao_jogar_menu.collidepoint(mouse):
                        tela_atual = "fases"

                    elif botao_naves_menu.collidepoint(mouse):
                        tela_atual = "naves"

                # TELA DE NAVES
                elif tela_atual == "naves":
                    if botao_retorno_naves.collidepoint(mouse):
                        tela_atual = "menu"

                # TELA DE CORES
                elif tela_atual == "cores":
                    for i, retangulo in enumerate(botoes_cores):
                        if retangulo.collidepoint(mouse):
                            cor_escolhida = cores[i][1]

                    if botao_voltar_cores.collidepoint(mouse):
                        tela_atual = "menu"

                    elif botao_continuar.collidepoint(mouse):
                        tela_atual = "fases"

                # TELA DE FASES
                elif tela_atual == "fases":
                    if botao_fase.collidepoint(mouse):
                        iniciar_fase()
                        tela_atual = "jogo"
                        
                    elif botao_fase2.collidepoint(mouse):
                        iniciar_fase()
                        tela_atual = "fase2"
                    

                    elif botao_voltar_fases.collidepoint(mouse):
                        tela_atual = "menu"
                # FASE 02
                    elif tela_atual == "fase2":

                        imediato = pygame.time.get_ticks()

                        tela.fill(PRETO)

                            # MOVIMENTAÇÃO DO JOGADOR
                        usuario.teclas_mover()

                            # MOVIMENTAÇÃO DOS INIMIGOS
                        for inimigo in inimigo_basico:
                                inimigo.mover()

                            # DESENHO DO JOGADOR
                            
                            # DESENHO DOS INIMIGOS
                        for inimigo in inimigo_basico:
                                inimigo.desenho()

                            # PONTUAÇÃO
                        texto(
                                "Pontos: " + str(pontos_usuario),
                                pequena,
                                BRANCO,
                                75,
                                25
                            )

                        texto(
                                "Fase 02",
                                pequena,
                                BRANCO,
                                710,
                                25
                            )

                # GAME OVER
                elif tela_atual == "gameover":
                    if botao_tentar.collidepoint(mouse):
                        iniciar_fase()
                        tela_atual = "jogo"

                    elif botao_sair_fase.collidepoint(mouse):
                        tela_atual = "fases"

                # VITORIA
                elif tela_atual == "vitoria":
                    if botao_tentar.collidepoint(mouse):
                        iniciar_fase()
                        tela_atual = "jogo"

                    elif botao_sair_fase.collidepoint(mouse):
                        tela_atual = "fases"


    tela.fill(PRETO)

    # TELA INICIAL
    # TELA INICIAL
    if tela_atual == "inicio":
        tela.blit(imagem_inicio, posicao_imagem)
        
    elif tela_atual == "menu":
        tela.fill((72, 53, 30))
        tela.blit(imagem_menu, posicao_do_menu)
        
    # TELA DAS NAVES BLOQUEADAS
    elif tela_atual == "naves":
        texto(
            "NÃO HÀ NENHUMA NAVE DESBLOQUEADA AINDA",
            fonte,
            BRANCO,
            300,
            230
        )

        botao(
            "VOLTAR",
            40, 520, 150, 50,
            CINZA
        )
        
    # TELA DE ESCOLHA DE CORES
    elif tela_atual == "cores":
        texto("ESCOLHA SUA NAVE", fonte, BRANCO, 400, 100)
        texto(
            "Clique em uma cor para seleciona-la",
            pequena, BRANCO, 400, 165
        )

        for i, (nome, cor) in enumerate(cores):
            r = botoes_cores[i]

            pygame.draw.rect(tela, cor, r, border_radius=5)

            borda = BRANCO if cor == cor_escolhida else CINZA

            pygame.draw.rect(
                tela, borda, r, 4, border_radius=5
            )

            texto(nome, pequena, BRANCO, r.centerx, r.bottom + 18)

        pygame.draw.rect(
            tela, cor_escolhida,
            (380, 455, 40, 30), border_radius=5
        )

        texto("Sua nave", pequena, BRANCO, 400, 495)

        botao("VOLTAR", 40, 520, 150, 50, CINZA)
        botao(
            "CONTINUAR", 550, 520, 210, 50, VERDE
        )

    # TELA DE ESCOLHA DE FASES
    elif tela_atual == "fases":
        texto("ESCOLHA UMA FASE", fonte, BRANCO, 400, 130)

        botao("Fase 01", 150, 260, 220, 75, MARROM)
        botao("Fase 02", 430, 260, 220, 75, AMARELO)
        botao("VOLTAR", 40, 520, 150, 50, CINZA)

    # FASE 01
    elif tela_atual == "jogo":
        jogador.mover()

        teclas = pygame.key.get_pressed()

        # Tiro continuo do jogador
        if teclas[pygame.K_SPACE] and agora - ultimo_tiro >= 250:
            jogador.atirar()
            ultimo_tiro = agora

        # SURGIMENTO DAS HORDAS
        tempo_fase = agora - tempo_inicio

        if hordas_lancadas < 3:
            proximo_tempo = hordas_lancadas * 30000

            if tempo_fase >= proximo_tempo:
                if hordas_lancadas == 1:
                    criar_horda(15)

                elif hordas_lancadas == 2:
                    criar_horda(20)

                hordas_lancadas += 1

        # TIROS DOS INIMIGOS
        if inimigos and agora - ultimo_disparo_inimigo >= 800:
            inimigo = random.choice(inimigos)

            tiro = pygame.Rect(
                inimigo.rect.centerx - 4,
                inimigo.rect.bottom,
                8, 12
            )

            tiros_inimigos.append(tiro)
            ultimo_disparo_inimigo = agora

        # MOVIMENTACAO DOS INIMIGOS
        for inimigo in inimigos:
            inimigo.mover()

        # MOVIMENTACAO DOS TIROS DO JOGADOR
        for tiro in tiros_jogador[:]:
            tiro.y -= 9

            if tiro.bottom < 0:
                tiros_jogador.remove(tiro)

        # MOVIMENTACAO DOS TIROS DOS INIMIGOS
        for tiro in tiros_inimigos[:]:
            tiro.y += 5

            if tiro.top > ALTURA:
                tiros_inimigos.remove(tiro)

        # COLISAO ENTRE TIROS DO JOGADOR E INIMIGOS
        for tiro in tiros_jogador[:]:
            for inimigo in inimigos[:]:
                if tiro.colliderect(inimigo.rect):
                    tiros_jogador.remove(tiro)
                    inimigos.remove(inimigo)
                    pontos += 1
                    break

        # COLISAO ENTRE TIROS INIMIGOS E JOGADOR
        for tiro in tiros_inimigos[:]:
            if tiro.colliderect(jogador.rect):
                tela_atual = "gameover"
                break

        # COLISAO ENTRE JOGADOR E INIMIGOS
        for inimigo in inimigos:
            if jogador.rect.colliderect(inimigo.rect):
                tela_atual = "gameover"
                break

        # O BOSS APARECE DEPOIS DAS TRES HORDAS
        # E SOMENTE QUANDO TODOS OS INIMIGOS MORREREM
        if (
            hordas_lancadas == 3
            and len(inimigos) == 0
            and boss is None
        ):
            boss = Boss()
            ultimo_ataque_boss = agora

        # COMBATE CONTRA O BOSS
        if boss is not None and tela_atual == "jogo":

            # Criacao dos ataques com intervalo
            if agora - ultimo_ataque_boss >= 2500:
                criar_ataque_boss(agora)
                ultimo_ataque_boss = agora

            # Verifica se algum laser atingiu o jogador
            if jogador_atingido_pelo_laser(agora):
                tela_atual = "gameover"

            # Os tiros do jogador causam dano ao Boss
            for tiro in tiros_jogador[:]:
                mascara_tiro = pygame.mask.Mask(
                    (tiro.width, tiro.height),
                    fill = True
                )
                
                deslocamento = (
                    tiro.left - boss.rect.left,
                    tiro.top - boss.rect.top
                )
                
                colisao = boss.mask.overlap(
                    mascara_tiro,
                    deslocamento
                )
                
                if colisao is not None:
                    tiros_jogador.remove(tiro)
                    boss.vida -= 1
                    
                    if boss.vida <= 0:
                        boss = None
                        lasers = []
                        tela_atual = "vitoria"
                        break

                
        # DESENHO DOS PERSONAGENS E PROJETEIS
        jogador.desenhar()

        for inimigo in inimigos:
            inimigo.desenhar()

        for tiro in tiros_jogador:
            pygame.draw.rect(tela, AMARELO, tiro)

        for tiro in tiros_inimigos:
            pygame.draw.rect(tela, VERMELHO, tiro)

        if boss is not None:
            boss.desenhar()
            desenhar_lasers(agora)

        texto(
            "Pontos: " + str(pontos),
            pequena, BRANCO, 75, 25
        )

        texto("Fase 01", pequena, BRANCO, 710, 25)

        if boss is None and hordas_lancadas < 3:
            texto(
                "Horda: " + str(hordas_lancadas) + "/3",
                pequena, BRANCO, 400, 25
            )

        elif boss is not None:
            texto("BOSS", pequena, BRANCO, 400, 250)

    # TELA GAME OVER
    elif tela_atual == "gameover":
        texto("GAME OVER", fonte, VERMELHO, 400, 180)
        texto(
            "Pontuacao: " + str(pontos),
            media, BRANCO, 400, 260
        )

        botao(
            "Tentar denovo", 220, 340, 360, 60, VERDE
        )

        botao(
            "Sair da Fase", 220, 420, 360, 60,
            (220, 100, 80)
        )

    # TELA DE VITORIA
    elif tela_atual == "vitoria":
        texto("VOCE VENCEU!", fonte, VERDE, 400, 180)

        texto(
            "Voce derrotou o Boss!",
            media, BRANCO, 400, 250
        )

        texto(
            "Pontuacao: " + str(pontos),
            pequena, BRANCO, 400, 290
        )

        botao(
            "Jogar novamente", 220, 340, 360, 60, VERDE
        )

        botao(
            "Voltar as Fases", 220, 420, 360, 60,
            (80, 150, 220)
        )

    pygame.display.flip()
    relogio.tick(60)