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
NUM_ESTRELAS = 2
RAIO_PROPORCIONALIDADE = 2  # Constante de ajuste para o raio
ESCALA = 200  # Fator de escala
COLISAO = 1   #1 ativado, 0 desativado
ESPACO_VIRTUAL_LARGURA = LARGURA * ESCALA
ESPACO_VIRTUAL_ALTURA = ALTURA * ESCALA

# calcula o raio de um corpo em base a massa dele
def calcular_raio(massa):
    return (massa ** (1/3)) * RAIO_PROPORCIONALIDADE

# Classes para corpos celestes
class CorpoCeleste:
    def __init__(self, x, y, vx, vy, massa, raio):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.raio = raio
        self.ativo = True
        self.trajetoria = []  # Histórico da trajetória

    def atualizar_trajetoria(self):
        if len(self.trajetoria) > 10000:  # Limitar o número de pontos armazenados
            self.trajetoria.pop(0)
        self.trajetoria.append((self.x, self.y))

class Estrela(CorpoCeleste):
    pass

def criar_estrelas(num_estrelas):
    estrelas = []
    if NUM_ESTRELAS > 0:
        # Central star
        x = ESPACO_VIRTUAL_LARGURA / 2
        y = ESPACO_VIRTUAL_ALTURA / 2
        massa = 2000000000
        raio = calcular_raio(massa)
        estrelas.append(Estrela(x, y, 0, 0, massa, raio))

    if NUM_ESTRELAS > 1:
        # Calculate orbital parameters for circular orbit
        distancia_orbital = 30000  # Distance from central star
        massa_central = estrelas[0].massa
        
        # Calculate orbital velocity for a circular orbit
        # v = sqrt(G * M / r)
        velocidade_orbital = math.sqrt(G * massa_central / distancia_orbital)
        
        # Position the second star in a circular orbit
        angulo = math.pi / 4  # 45-degree angle, you can adjust this
        x = x + distancia_orbital * math.cos(angulo)
        y = y + distancia_orbital * math.sin(angulo)
        
        # Tangential velocity for circular orbit
        vx = -velocidade_orbital * math.sin(angulo)
        vy = velocidade_orbital * math.cos(angulo)
        
        massa = 100000
        raio = calcular_raio(massa) * 10
        estrelas.append(Estrela(x, y, vx, vy, massa, raio))

    if NUM_ESTRELAS > 2:
        # Similar approach for the third star
        distancia_orbital = 50000  # Different distance for third star
        velocidade_orbital = math.sqrt(G * massa_central / distancia_orbital)
        
        angulo = -math.pi / 4  # Opposite angle
        x = x + distancia_orbital * math.cos(angulo)
        y = y + distancia_orbital * math.sin(angulo)
        
        vx = -velocidade_orbital * math.sin(angulo)
        vy = velocidade_orbital * math.cos(angulo)
        
        massa = 100000
        raio = calcular_raio(massa) * 20
        estrelas.append(Estrela(x, y, vx, vy, massa, raio))

    if NUM_ESTRELAS > 3:
        for _ in range(num_estrelas-3):
            # Random positioning but closer to the center
            distancia_orbital = random.uniform(20000, 80000)
            angulo = random.uniform(0, 2 * math.pi)
            
            x = ESPACO_VIRTUAL_LARGURA / 2 + distancia_orbital * math.cos(angulo)
            y = ESPACO_VIRTUAL_ALTURA / 2 + distancia_orbital * math.sin(angulo)
            
            # Calculate orbital velocity
            velocidade_orbital = math.sqrt(G * massa_central / distancia_orbital)
            
            # Tangential velocity for circular orbit
            vx = -velocidade_orbital * math.sin(angulo)
            vy = velocidade_orbital * math.cos(angulo)
            
            massa = random.randint(10000, 50000)
            raio = calcular_raio(massa)
            estrelas.append(Estrela(x, y, vx, vy, massa, raio))

    return estrelas

def verificar_colisoes(estrelas):
    for i in range(len(estrelas)):
        if not estrelas[i].ativo:
            continue
        for j in range(i + 1, len(estrelas)):
            if not estrelas[j].ativo:
                continue
            dx = estrelas[j].x - estrelas[i].x
            dy = estrelas[j].y - estrelas[i].y
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia <= (estrelas[i].raio + estrelas[j].raio):
                # Massa total
                massa_total = estrelas[i].massa + estrelas[j].massa

                # Centro de massa
                cx = (estrelas[i].x * estrelas[i].massa + estrelas[j].x * estrelas[j].massa) / massa_total
                cy = (estrelas[i].y * estrelas[i].massa + estrelas[j].y * estrelas[j].massa) / massa_total

                # Momento angular total antes da fusão
                Lx = (estrelas[i].y - cy) * estrelas[i].massa * estrelas[i].vx + (estrelas[j].y - cy) * estrelas[j].massa * estrelas[j].vx
                Ly = -(estrelas[i].x - cx) * estrelas[i].massa * estrelas[i].vy - (estrelas[j].x - cx) * estrelas[j].massa * estrelas[j].vy

                # Velocidade resultante
                vx_resultante = (estrelas[i].vx * estrelas[i].massa + estrelas[j].vx * estrelas[j].massa) / massa_total
                vy_resultante = (estrelas[i].vy * estrelas[i].massa + estrelas[j].vy * estrelas[j].massa) / massa_total

                # Ajuste para conservar o momento angular
                vx_resultante += Lx / (massa_total * distancia**2)
                vy_resultante += Ly / (massa_total * distancia**2)

                # Atualizar estrela resultante
                if estrelas[i].massa >= estrelas[j].massa:
                    estrelas[i].vx = vx_resultante
                    estrelas[i].vy = vy_resultante
                    estrelas[i].massa = massa_total
                    estrelas[i].raio = (estrelas[i].raio**3 + estrelas[j].raio**3)**(1/3)
                    estrelas[j].ativo = False
                else:
                    estrelas[j].vx = vx_resultante
                    estrelas[j].vy = vy_resultante
                    estrelas[j].massa = massa_total
                    estrelas[j].raio = (estrelas[j].raio**3 + estrelas[i].raio**3)**(1/3)
                    estrelas[i].ativo = False


# Função para calcular gravidade
def calcular_gravidade_estrela(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    distancia = math.sqrt(dx * dx + dy * dy)

    if distancia > 0.01:
        forca = G * a.massa * b.massa / (distancia * distancia)
        ax_a = forca * dx / distancia / a.massa
        ay_a = forca * dy / distancia / a.massa
        ax_b = -forca * dx / distancia / b.massa
        ay_b = -forca * dy / distancia / b.massa
        a.vx += ax_a
        a.vy += ay_a
        b.vx += ax_b
        b.vy += ay_b

# Função para atualizar posições
def atualizar_estrelas(estrelas):
    for i in range(len(estrelas)):
        if not estrelas[i].ativo:
            continue
        for j in range(i + 1, len(estrelas)):
            if estrelas[j].ativo:
                calcular_gravidade_estrela(estrelas[i], estrelas[j])
        estrelas[i].x += estrelas[i].vx
        estrelas[i].y += estrelas[i].vy
        estrelas[i].atualizar_trajetoria()

# Função para desenhar objetos
def desenhar_objeto(x_virtual, y_virtual, raio, cor):
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))

# Função para desenhar trajetórias
def desenhar_trajetoria(estrela, cor):
    if estrela.ativo and estrela.trajetoria:
        pontos_tela = [(int(pos[0] / ESCALA), int(pos[1] / ESCALA)) for pos in estrela.trajetoria]
        if len(pontos_tela) > 1:
            pygame.draw.lines(tela, cor, False, pontos_tela, 1)

# Função para desenhar estrelas e trajetórias separadamente
def desenhar_estrelas(estrelas):
    # Primeiro, desenhe todas as trajetórias
    for idx, estrela in enumerate(estrelas):
        if idx == 0:  # Primeiro planeta (amarelo)
            cor_trajetoria = (255, 255, 0)
        elif idx == 1:  # Segundo planeta (azul)
            cor_trajetoria = (100, 100, 255)
        else:
            cor_trajetoria = (255, 255, 255)  # Cor padrão para outros objetos

        desenhar_trajetoria(estrela, cor_trajetoria)

    # Depois, desenhe todas as estrelas
    for idx, estrela in enumerate(estrelas):
        if idx == 0:  # Primeiro planeta (amarelo)
            cor_estrela = (255, 255, 0)
        elif idx == 1:  # Segundo planeta (azul)
            cor_estrela = (100, 100, 255)
        else:
            cor_estrela = (255, 255, 255)  # Cor padrão para outros objetos

        if estrela.ativo:
            desenhar_objeto(estrela.x, estrela.y, estrela.raio, cor_estrela)


# Função para desenhar objetos
def desenhar_objetoN(x_virtual, y_virtual, raio, cor):
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))

# Função para desenhar trajetórias
def desenhar_trajetoriaN(estrela, cor):
    if estrela.ativo and estrela.trajetoria:
        pontos_tela = [(int(pos[0] / ESCALA), int(pos[1] / ESCALA)) for pos in estrela.trajetoria]
        if len(pontos_tela) > 1:
            pygame.draw.lines(tela, cor, False, pontos_tela, 1)

# Gerar cores únicas para as estrelas
def gerar_cores_unicas(num_estrelas):
    random.seed(20)  # Para consistência nas cores geradas
    return [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(num_estrelas)]

# Função para desenhar estrelas e trajetórias
def desenhar_estrelasN(estrelas):
    # Gera cores diferentes para cada estrela
    cores = gerar_cores_unicas(len(estrelas))
    
    # Primeiro, desenhe todas as trajetórias
    for idx, estrela in enumerate(estrelas):
        desenhar_trajetoria(estrela, cores[idx])

    # Depois, desenhe todas as estrelas
    for idx, estrela in enumerate(estrelas):
        if estrela.ativo:
            desenhar_objeto(estrela.x, estrela.y, estrela.raio, cores[idx])


# Inicializar estrelas
estrelas = criar_estrelas(NUM_ESTRELAS)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estrelas[1].vx *= 1.15
                    estrelas[1].vy *= 1.15
     
        

    tela.fill((0, 0, 0))
    if COLISAO == 1:
        verificar_colisoes(estrelas)
    atualizar_estrelas(estrelas)
    if NUM_ESTRELAS <= 3:
        desenhar_estrelas(estrelas)
    else:
        desenhar_estrelasN(estrelas)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()