import pygame
import math
import random

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 950, 950
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

# Constantes
G = 6.67430  # Constante gravitacional
NUM_ESTRELAS = 1
NUM_PLANETAS = 20000
RAIO_PROPORCIONALIDADE = 1  # Constante de ajuste para o raio

# Espaço virtual
ESCALA = 1000  # Fator de escala: o mundo será 10x maior que a janela
ESPACO_VIRTUAL_LARGURA = LARGURA * ESCALA
ESPACO_VIRTUAL_ALTURA = ALTURA * ESCALA

# Funções auxiliares
def calcular_raio(massa):
    return (massa ** (1/3)) * RAIO_PROPORCIONALIDADE

def calcular_massa():
    return random.uniform(1000, 100000)

def gerar_posicao_aleatoria():
    x = random.uniform(100, ESPACO_VIRTUAL_LARGURA - 100)
    y = random.uniform(100, ESPACO_VIRTUAL_ALTURA - 100)
    return x, y

# Classes para Estrelas e Planetas
class CorpoCeleste:
    def __init__(self, x, y, vx, vy, massa, raio):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.raio = raio
        self.ativo = True

class Estrela(CorpoCeleste):
    def __init__(self, x, y, vx, vy, massa, raio):
        super().__init__(x, y, vx, vy, massa, raio)

class Planeta(CorpoCeleste):
    def __init__(self, x, y, vx, vy, massa, raio):
        super().__init__(x, y, vx, vy, massa, raio)

# Função para criar estrelas
def criar_estrelas(num_estrelas):
    estrelas = []
    for _ in range(num_estrelas):
        x, y = ESPACO_VIRTUAL_LARGURA/2, ESPACO_VIRTUAL_ALTURA/2
        massa = 100000000000
        raio = calcular_raio(massa)
        estrelas.append(Estrela(x, y, random.uniform(-10, 10), random.uniform(-10, 10), massa, raio))
    return estrelas

# Função para criar planetas
def criar_planetas(num_planetas):
    planetas = []
    for _ in range(num_planetas):
        x, y = gerar_posicao_aleatoria()
        planetas.append(Planeta(x, y, 500, 500, 10000, 1500))
    return planetas

# Criação das estrelas e planetas
estrelas = criar_estrelas(NUM_ESTRELAS)
planetas = criar_planetas(NUM_PLANETAS)

def verificar_colisoes():
    for i in range(NUM_ESTRELAS):
        if not estrelas[i].ativo:
            continue
        for j in range(i + 1, NUM_ESTRELAS):
            if not estrelas[j].ativo:
                continue

            dx = estrelas[j].x - estrelas[i].x
            dy = estrelas[j].y - estrelas[i].y
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia <= (estrelas[i].raio + estrelas[j].raio):
                # Colisão detectada - combinar estrelas
                if estrelas[i].massa >= estrelas[j].massa:
                    # Conservação do momento linear
                    massa_total = estrelas[i].massa + estrelas[j].massa
                    estrelas[i].vx = (estrelas[i].vx * estrelas[i].massa + estrelas[j].vx * estrelas[j].massa) / massa_total
                    estrelas[i].vy = (estrelas[i].vy * estrelas[i].massa + estrelas[j].vy * estrelas[j].massa) / massa_total
                    
                    # Aumentar a massa e "absorver" a outra estrela
                    estrelas[i].massa = massa_total
                    estrelas[i].raio = (estrelas[i].raio**3 + estrelas[j].raio**3)**(1/3)  # Ajuste do raio pelo volume
                    estrelas[j].ativo = False  # Desativar a estrela "absorvida"
                else:
                    # O mesmo processo, mas para o caso onde a estrela j absorve a estrela i
                    massa_total = estrelas[j].massa + estrelas[i].massa
                    estrelas[j].vx = (estrelas[j].vx * estrelas[j].massa + estrelas[i].vx * estrelas[i].massa) / massa_total
                    estrelas[j].vy = (estrelas[j].vy * estrelas[j].massa + estrelas[i].vy * estrelas[i].massa) / massa_total

                    estrelas[j].massa = massa_total
                    estrelas[j].raio = (estrelas[j].raio**3 + estrelas[i].raio**3)**(1/3)  # Ajuste do raio pelo volume
                    estrelas[i].ativo = False



# Função para calcular a gravidade entre duas estrelas
def calcular_gravidade_estrela(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    distancia = math.sqrt(dx * dx + dy * dy)

    if distancia > 0.01:  # Evitar divisão por zero
        # Força gravitacional
        forca = G * a.massa * b.massa / (distancia * distancia)

        # Aceleração no eixo X e Y para a (direção oposta à estrela b)
        ax_a = forca * dx / distancia / a.massa
        ay_a = forca * dy / distancia / a.massa

        # Aceleração no eixo X e Y para b (direção oposta à estrela a)
        ax_b = -forca * dx / distancia / b.massa
        ay_b = -forca * dy / distancia / b.massa

        # Atualizar as velocidades das estrelas
        a.vx += ax_a
        a.vy += ay_a

        b.vx += ax_b
        b.vy += ay_b
import random

# Função para gerar uma nova posição aleatória dentro dos limites da tela
def nova_posicao_aleatoria():
    x = random.uniform(0, LARGURA)
    y = random.uniform(0, ALTURA)
    return x, y

# Função para atualizar a posição das estrelas
def atualizar_estrelas():
    for i in range(NUM_ESTRELAS):
        if not estrelas[i].ativo:
            continue

        # Calcular a interação gravitacional com as outras estrelas
        for j in range(i + 1, NUM_ESTRELAS):
            if estrelas[j].ativo:
                calcular_gravidade_estrela(estrelas[i], estrelas[j])

        # Atualizar a posição das estrelas com base na velocidade
        estrelas[i].x += estrelas[i].vx
        estrelas[i].y += estrelas[i].vy

def atualizar_planetas():
    for i in range(NUM_PLANETAS):
        if planetas[i].ativo:
            for j in range(NUM_ESTRELAS):
                dx = estrelas[j].x - planetas[i].x
                dy = estrelas[j].y - planetas[i].y
                distancia = math.sqrt(dx**2 + dy**2)
                if distancia > 0:
                    F = G * estrelas[j].massa * planetas[i].massa / (distancia**2)
                    ax = F * dx / distancia / planetas[i].massa
                    ay = F * dy / distancia / planetas[i].massa
                    planetas[i].vx += ax
                    planetas[i].vy += ay
            planetas[i].x += planetas[i].vx
            planetas[i].y += planetas[i].vy

def desenhar_objeto(x_virtual, y_virtual, raio, cor):
    # Converte as coordenadas do espaço virtual para o espaço da tela (com escala)
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA

    # Desenha o círculo na tela
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))
    #pygame.draw.rect(tela, cor, pygame.Rect(int(x_tela), int(y_tela), int(raio_tela*2), int(raio_tela*2)))


def desenhar_estrelas():
    for estrela in estrelas:
        if estrela.ativo:
            desenhar_objeto(estrela.x, estrela.y, estrela.raio, (255, 255, 255))  # Amarelo

def desenhar_planetas():
    for planeta in planetas:
        if planeta.ativo:
            desenhar_objeto(planeta.x, planeta.y, planeta.raio, (170, 170, 170))  # Branco

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((0, 0, 0))  # Preencher a tela com preto
    verificar_colisoes()
    atualizar_estrelas()
    atualizar_planetas()
    desenhar_estrelas()
    desenhar_planetas()

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
