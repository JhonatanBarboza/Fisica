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
NUM_ESTRELAS = 3
RAIO_PROPORCIONALIDADE = 2  # Constante de ajuste para o raio
ESCALA = 200  # Fator de escala
COLISAO = 1   #1 ativado, 0 desativado
ESPACO_VIRTUAL_LARGURA = LARGURA * ESCALA
ESPACO_VIRTUAL_ALTURA = ALTURA * ESCALA

# Funções auxiliares
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

# Função para criar estrelas
def criar_estrelas(num_estrelas):
    estrelas = []
    if NUM_ESTRELAS > 0:
        x = ESPACO_VIRTUAL_LARGURA / 2 - 10000
        y = ESPACO_VIRTUAL_ALTURA / 2 - 1000
        massa = 20000000
        raio = calcular_raio(massa)
        estrelas.append(Estrela(x, y, 300, 300, massa, raio))

    if NUM_ESTRELAS > 1:
        x = ESPACO_VIRTUAL_LARGURA / 2 - 20000
        y = ESPACO_VIRTUAL_ALTURA / 2 + 20000
        massa = 200000000
        raio = calcular_raio(massa)
        estrelas.append(Estrela(x, y, -300, -300, massa, raio))

    if NUM_ESTRELAS > 2:
        x = ESPACO_VIRTUAL_LARGURA / 2 + 30000
        y = ESPACO_VIRTUAL_ALTURA / 2 - 30000
        massa = 20000000
        raio = calcular_raio(massa)
        estrelas.append(Estrela(x, y, -300, -300, massa, raio))


    if NUM_ESTRELAS > 3:
        for _ in range(num_estrelas-3):
            x = ESPACO_VIRTUAL_LARGURA / 2 + random.randint(-100000, 100000)
            y = ESPACO_VIRTUAL_ALTURA / 2 + random.randint(-100000, 100000)
            massa = random.randint(100000, 100000000)
            raio = calcular_raio(massa)
            estrelas.append(Estrela(x, y, random.randint(-300, 300), random.randint(-300, 300), massa, raio))

    return estrelas
    
def calcular_velocidade(vx, vy):
    """Calcula a magnitude da velocidade a partir das componentes."""
    return math.sqrt(vx**2 + vy**2)

def calcular_velocidade_relativa(corpoA, corpoB : CorpoCeleste):
    """Calcula a velocidade relativa entre duas estrelas."""
    vel1 = calcular_velocidade(corpoA.vx, corpoA.vy)
    vel2 = calcular_velocidade(corpoB.vx, corpoB.vy)
    return abs(vel1 - vel2)

def verificar_colisoes(estrelas):
    """
    Detecta e processa colisões entre estrelas e entre planetas.

    Para cada par de estrelas ou planetas, verifica se há colisão com base na distância
    entre os centros e os raios dos corpos. Quando ocorre uma colisão, aplica as regras
    de conservação do momento linear para calcular a nova velocidade, soma as massas 
    e ajusta o raio do corpo resultante. O corpo de menor massa é "absorvido" e marcado 
    como inativo.

    Operações:
        1. Verifica colisões entre estrelas:
            - Se duas estrelas colidem, a estrela maior absorve a menor.
            - A nova estrela resultante conserva o momento linear e acumula a massa e o volume.
            - A estrela absorvida é desativada.

        2. Verifica colisões entre planetas:
            - Mesma lógica aplicada às estrelas, mas considerando planetas.

    Nota: Os corpos desativados são ignorados nas verificações subsequentes.

    Retorna:
        None.
    """
    # Verificar colisões entre estrelas
    for i in range(NUM_ESTRELAS):
        if not estrelas[i].ativo:
            continue
        for j in range(i + 1, NUM_ESTRELAS):
            if not estrelas[j].ativo:
                continue

            # Calcular a distância entre duas estrelas
            dx_estrelas = estrelas[j].x - estrelas[i].x
            dy_estrelas = estrelas[j].y - estrelas[i].y
            distancia_estrelas = math.sqrt(dx_estrelas ** 2 + dy_estrelas ** 2)

            if distancia_estrelas <= (estrelas[i].raio + estrelas[j].raio):  # Colisão detectada
                massa_relativa = (estrelas[i].massa/(estrelas[i].massa + estrelas[j].massa))
                velocidade_destruicao = 600
                velocidade_relativa = calcular_velocidade_relativa(estrelas[i], estrelas[j])
                # Caso em que corpos possuem massa semelhantes e velocidades altas, destroem-se.
                if(0.4 <= massa_relativa and massa_relativa <= 0.6 and velocidade_relativa > velocidade_destruicao):
                  estrelas[i].ativo = False  
                  estrelas[j].ativo = False  
                else:  
                  if estrelas[i].massa >= estrelas[j].massa:  # Estrela i absorve j
                      absorver_corpo(estrelas[i], estrelas[j])
                  else:  # Estrela j absorve i
                      absorver_corpo(estrelas[j], estrelas[i])                

                   
def absorver_corpo(corpoA, corpoB : CorpoCeleste):
  """"
  corpoA absorve corpoB.
  
  Conservação do momento linear:
  - (v_A * m_A + v_B * m_B)/ m_A + m_B
  
  Parâmetros:
    corpoA: corpo que irá absorver.
    corpoB: corpo a ser absorvido. 
  
  Retorno:
    None
  """
  
  massa_total = corpoA.massa + corpoB.massa # Massa total do sistema.
  # Preserva momento linear na direção x.
  corpoA.vx = (corpoA.vx * corpoA.massa + corpoB.vx * corpoB.massa) / massa_total 
  # Preserva momento linear na direção y.
  corpoA.vy = (corpoA.vy * corpoA.massa + corpoB.vy * corpoB.massa) / massa_total
  # Nova massa de A é a soma da massa dos dois corpos.
  corpoA.massa = massa_total
  # A partir da conservação do volume, temos o novo raio dado por:
  corpoA.raio = (corpoA.raio ** 3 + corpoB.raio ** 3) ** (1 / 3)
  corpoB.ativo = False  # Desativar corpoB

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
