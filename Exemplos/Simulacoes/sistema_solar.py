import pygame
import math

pygame.init()

LARGURA_SIMULACAO, ALTURA_SIMULACAO = 1600, 1000
tela_simulacao = pygame.display.set_mode((LARGURA_SIMULACAO, ALTURA_SIMULACAO))
clock = pygame.time.Clock()

ESCALA_DISTANCIA = 1.5e9 
G = 6.67430e-11 * 1e8  

# Deixa a simulação mais rápida (cuidado com valores muito grandes)
FATOR_TEMPO = 1

# Alterei a velocidade porque estava muito lenta
VELOCIDADE_FAKE_TERRA = 29783 * 15000


# Crio a classe corpo celeste, que será usada apra instanciar os planetas
class CorpoCeleste:
    def __init__(self, nome, x, y, vx, vy, massa, raio, cor):
        self.nome = nome
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.raio = raio
        self.cor = cor

    def atualizar_posicao(self):
        self.x += self.vx * FATOR_TEMPO
        self.y += self.vy * FATOR_TEMPO

    def desenhar(self):
        x_tela = LARGURA_SIMULACAO // 2 + int(self.x / ESCALA_DISTANCIA)
        y_tela = ALTURA_SIMULACAO // 2 + int(self.y / ESCALA_DISTANCIA)
        pygame.draw.circle(tela_simulacao, self.cor, (x_tela, y_tela), self.raio)


# O Sol foi adicionado no meio da tela. Seu tamanho é o único que não está em proporção, pois é muito grande
sol = CorpoCeleste("Sol", 0, 0, 0, 0, 1.989e30, 20, (255, 204, 0))
mercurio = CorpoCeleste("Mercurio", 0.580e11, 0, 0, VELOCIDADE_FAKE_TERRA / 0.65, 3.301e24, 3, (143, 145, 146))
venus = CorpoCeleste("Venus", 1.082e11, 0, 0, VELOCIDADE_FAKE_TERRA / 0.9, 4.868e24, 7.9, (158, 84, 21))
terra = CorpoCeleste("Terra", 1.496e11, 0, 0, VELOCIDADE_FAKE_TERRA, 5.972e24, 8, (100, 100, 255))
marte = CorpoCeleste("Marte", 2.279e11, 0, 0, VELOCIDADE_FAKE_TERRA / 1.21, 6.417e24, 8.1, (230, 121, 62))
jupiter = CorpoCeleste("Jupiter", 7.785e11, 0, 0, VELOCIDADE_FAKE_TERRA / 2.5, 1.898e27, 80, (196, 108, 53))

# Saturno saiu da tela, mas pode ser visto em alguns momentos
saturno = CorpoCeleste("Saturno", 14.294e11, 0, 0, VELOCIDADE_FAKE_TERRA / 3.5, 5.684e27, 160, (203, 195, 146))

# Array com todos os planetas criados
corpos = [sol, mercurio, venus, terra, marte, jupiter, saturno]

# Função auxiliar para calcular a gravidade
def calcular_gravidade(corpo_a, corpo_b):
    dx = corpo_b.x - corpo_a.x
    dy = corpo_b.y - corpo_a.y

    # Calcula-se a distância entre dois corpos
    distancia = math.sqrt(dx ** 2 + dy ** 2)

    # Evita divisão por 0
    if distancia > 0.1:

        # Fg = M*m*G/d²
        forca = G * corpo_a.massa * corpo_b.massa / (distancia ** 2)

        ax = forca * dx / distancia / corpo_a.massa * FATOR_TEMPO
        ay = forca * dy / distancia / corpo_a.massa * FATOR_TEMPO
        corpo_a.vx += ax
        corpo_a.vy += ay

        bx = -forca * dx / distancia / corpo_b.massa * FATOR_TEMPO
        by = -forca * dy / distancia / corpo_b.massa * FATOR_TEMPO
        corpo_b.vx += bx
        corpo_b.vy += by

rodando = True
while rodando:
    tela_simulacao.fill((0, 0, 0))
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for i, corpo_a in enumerate(corpos):
        for j, corpo_b in enumerate(corpos):
            if i != j:
                calcular_gravidade(corpo_a, corpo_b)
        corpo_a.atualizar_posicao()
        corpo_a.desenhar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
