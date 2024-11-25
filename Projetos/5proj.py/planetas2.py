# Importando as bibliotecas necessárias
import pygame
import pygame_gui #interface
import math
import random
import matplotlib.pyplot as plt
import numpy as np

class GraficoTempoReal:
    def __init__(self, max_pontos=200):
        self.max_pontos = max_pontos
        self.corpos_ativos = []
        self.velocidade_media = []

    def atualizar(self, estrelas, planetas):
        # Número de corpos ativos
        total_corpos_ativos = sum(1 for corpo in estrelas + planetas if corpo.ativo)
        self.corpos_ativos.append(total_corpos_ativos)

        # Velocidade média
        velocidades = [math.sqrt(corpo.vx**2 + corpo.vy**2) for corpo in estrelas + planetas if corpo.ativo]
        velocidade_media = np.mean(velocidades) if velocidades else 0
        self.velocidade_media.append(velocidade_media)

        # Limita o número de pontos
        self.corpos_ativos = self.corpos_ativos[-self.max_pontos:]
        self.velocidade_media = self.velocidade_media[-self.max_pontos:]

    def desenhar_grafico(self, tela):
        plt.figure(figsize=(6, 4))
        plt.subplot(2, 1, 1)
        plt.plot(self.corpos_ativos, label='Corpos Ativos')
        plt.title('Métricas da Simulação')
        plt.ylabel('Número')

        plt.subplot(2, 1, 2)
        plt.plot(self.velocidade_media, label='Velocidade Média', color='red')
        plt.xlabel('Tempo')
        plt.ylabel('Velocidade')

        plt.tight_layout()
        plt.savefig('simulation_metrics.png')
        plt.close()

        # Carrega a imagem salva
        grafico = pygame.image.load('simulation_metrics.png')
        grafico = pygame.transform.scale(grafico, (300, 200))
        tela.blit(grafico, (LARGURA - 320, 10))

# Inicializando o Pygame e criando a janela com opção de redimensionamento
pygame.init()
LARGURA, ALTURA = 920, 640  # Dimensões iniciais da janela
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)  # Criando a janela
pygame.display.set_caption("Space Simulation")  # Definindo o título da janela
clock = pygame.time.Clock()  # Inicializando o relógio para controlar a taxa de quadros

# Configurando o gerenciador de interface do usuário com Pygame GUI
gerenciador_interface = pygame_gui.UIManager((LARGURA, ALTURA))  # Gerenciador para widgets da interface

# Constantes usadas na simulação
G = 6.67430  # Constante gravitacional simplificada para a simulação
NUM_ESTRELAS = 500  # Número de estrelas no plano de fundo
NUM_PLANETAS = 0  # Número de planetas a serem simulados inicialmente

# Criando rótulos (labels) para exibir os valores atuais dos sliders(controle deslizante)
label_estrelas_valor = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 10), (100, 50)),  # Posição e tamanho do label
    text=str(NUM_ESTRELAS),  # Texto inicial exibindo o número de estrelas
    manager=gerenciador_interface,  # Gerenciador de interface
)

label_planetas_valor = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((220, 110), (100, 50)),  # Posição e tamanho do label
    text=str(NUM_PLANETAS),  # Texto inicial exibindo o número de planetas
    manager=gerenciador_interface,  # Gerenciador de interface
)

# Criando sliders horizontais para ajustar os números de estrelas e planetas
slider_estrelas = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 50), (200, 50)),  # Posição e tamanho do slider
    start_value=NUM_ESTRELAS,  # Valor inicial igual ao número de estrelas
    value_range=(0, 1000),  # Intervalo permitido de valores
    manager=gerenciador_interface,  # Gerenciador de interface
)

slider_planetas = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 150), (200, 50)),  # Posição e tamanho do slider
    start_value=NUM_PLANETAS,  # Valor inicial igual ao número de planetas
    value_range=(0, 1000),  # Intervalo permitido de valores
    manager=gerenciador_interface,  # Gerenciador de interface
)

# Criando labels para identificar os sliders
label_estrelas = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 10), (250, 50)),  # Posição e tamanho do label
    text="Número de estrelas",  # Texto descritivo
    manager=gerenciador_interface,  # Gerenciador de interface
)

label_planetas = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 110), (250, 30)),  # Posição e tamanho do label
    text="Número de planetas",  # Texto descritivo
    manager=gerenciador_interface,  # Gerenciador de interface
)

# Criando um botão para iniciar a simulação
botao_comecar = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 220), (100, 50)),  # Posição e tamanho do botão
    text="Iniciar",  # Texto exibido no botão
    manager=gerenciador_interface,  # Gerenciador de interface
)

def atualizar_informacoes():
    """
    Atualiza os valores globais de número de estrelas e planetas com base nos sliders.
    """
    global NUM_ESTRELAS, NUM_PLANETAS
    NUM_ESTRELAS = int(slider_estrelas.get_current_value())  # Obtém o valor do slider de estrelas
    NUM_PLANETAS = int(slider_planetas.get_current_value())  # Obtém o valor do slider de planetas

# Constantes relacionadas às propriedades das estrelas e planetas
LIMITE_VELOCIDADE_INICIAL_ESTRELA = 20  # Velocidade inicial máxima para estrelas
LIMITE_VELOCIDADE_INICIAL_PLANETA = 40  # Velocidade inicial máxima para planetas

MASSA_PLANETA = 5  # Massa fixa atribuída aos planetas
LIMITE_INFERIOR_MASSA_ESTRELA = 1000  # Limite inferior da massa das estrelas
LIMITE_SUPERIOR_MASSA_ESTRELA = 1000  # Limite superior da massa das estrelas
COR_ESTRELA = (150, 70, 8)  # Cor padrão atribuída às estrelas (RGB)

# Constantes relacionadas ao tamanho dos corpos celestes
RAIO_PLANETA = 20  # Raio fixo atribuído aos planetas
RAIO_PROPORCIONALIDADE = 2  # Fator de proporcionalidade para calcular o raio da estrela
# O raio da estrela é calculado como: (massa ** (1/3)) * RAIO_PROPORCIONALIDADE

# Configuração do espaço virtual para simulação
ESCALA = 7  # O fator de escala para ajustar o espaço simulado
ESPACO_VIRTUAL_LARGURA = LARGURA * ESCALA  # Largura do espaço virtual em função da escala
ESPACO_VIRTUAL_ALTURA = ALTURA * ESCALA  # Altura do espaço virtual em função da escala

def modulo(x: float) -> float:
    """
    Retorna o valor absoluto de um número.
    
    Argumento:
        x (float): Número de entrada.
        
    Retorno:
        float: Valor absoluto de x.
    """
    if x < 0:
        x = -x
    return x


# Funções auxiliares

def calcular_raio_estrela(massa: float) -> float:
    """
    Calcula o raio de uma estrela com base em sua massa.
    
    O cálculo é baseado na raiz cúbica da massa, multiplicada por um fator de proporcionalidade.

    Argumento:
        massa (float): Massa da estrela.
        
    Retorno:
        float: Raio da estrela.
    """
    return (modulo(massa) ** (1 / 3)) * RAIO_PROPORCIONALIDADE


def calcular_massa_estrela() -> float:
    """
    Gera uma massa aleatória para uma estrela dentro dos limites estabelecidos.
    
    Retorno:
        float: Massa gerada aleatoriamente para uma estrela.
    """
    return random.uniform(LIMITE_INFERIOR_MASSA_ESTRELA, LIMITE_SUPERIOR_MASSA_ESTRELA)


def gerar_posicao_aleatoria() -> tuple:
    """
    Gera uma posição aleatória dentro do espaço virtual.
    
    Retorno:
        tuple: Coordenadas (x, y) da posição gerada aleatoriamente.
    """
    x = random.uniform(0, ESPACO_VIRTUAL_LARGURA)
    y = random.uniform(0, ESPACO_VIRTUAL_ALTURA)
    return x, y

# Classes para Estrelas e Planetas

class CorpoCeleste:
    """
    Classe base para representar corpos celestes genéricos.
    
    Atributos:
        x (float): Coordenada x no espaço.
        y (float): Coordenada y no espaço.
        vx (float): Velocidade no eixo x.
        vy (float): Velocidade no eixo y.
        massa (float): Massa do corpo celeste.
        raio (float): Raio do corpo celeste.
        ativo (bool): Estado do corpo (True se ativo, False se desativado).
        cor (tuple): Cor do corpo no formato RGB.
    """
    def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.raio = raio
        self.ativo = True
        self.cor = cor


class Estrela(CorpoCeleste):
    """
    Classe que representa uma estrela, herdando de CorpoCeleste.
    
    Utiliza os mesmos atributos e comportamento de CorpoCeleste.
    """
    def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
        super().__init__(x, y, vx, vy, massa, raio, cor)


class Planeta(CorpoCeleste):
    """
    Classe que representa um planeta, herdando de CorpoCeleste.
    
    Utiliza os mesmos atributos e comportamento de CorpoCeleste.
    """
    def __init__(self, x: float, y: float, vx: float, vy: float, massa: float, raio: float, cor: tuple):
        super().__init__(x, y, vx, vy, massa, raio, cor)


# Função para criar estrelas
def criar_estrelas(num_estrelas: int) -> list:
    """
    Cria uma lista de objetos Estrela com atributos gerados aleatoriamente.

    Argumento:
        num_estrelas (int): Número de estrelas a serem criadas.

    Retorno:
        list: Lista de objetos Estrela.
    """
    estrelas = []
    for _ in range(num_estrelas):
        x, y = gerar_posicao_aleatoria()
        massa = calcular_massa_estrela()
        raio = calcular_raio_estrela(massa)
        # Cria uma estrela com velocidade aleatória
        lim = LIMITE_VELOCIDADE_INICIAL_ESTRELA
        estrelas.append(Estrela(
            x, y, 
            random.uniform(-lim, lim), random.uniform(-lim, lim),
            massa, raio, COR_ESTRELA
        ))
    return estrelas


# Função para criar planetas
def criar_planetas(num_planetas: int) -> list:
    """
    Cria uma lista de objetos Planeta com atributos gerados aleatoriamente.

    Argumento:
        num_planetas (int): Número de planetas a serem criados.

    Retorno:
        list: Lista de objetos Planeta.
    """
    planetas = []
    for _ in range(num_planetas):
        x, y = gerar_posicao_aleatoria()
        lim = LIMITE_VELOCIDADE_INICIAL_PLANETA
        # Cria um planeta com cor aleatória (tons de verde-azulado)
        planetas.append(Planeta(
            x, y,
            random.uniform(-lim, lim), random.uniform(-lim, lim),
            MASSA_PLANETA, RAIO_PLANETA,
            (0, random.uniform(50, 170), random.uniform(50, 170))
        ))
    return planetas

# Criação das estrelas e planetas
estrelas = criar_estrelas(NUM_ESTRELAS)
planetas = criar_planetas(NUM_PLANETAS)


def verificar_colisoes():
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
                if estrelas[i].massa >= estrelas[j].massa:  # Estrela i absorve j
                    massa_total = estrelas[i].massa + estrelas[j].massa
                    estrelas[i].vx = (estrelas[i].vx * estrelas[i].massa + estrelas[j].vx * estrelas[j].massa) / massa_total
                    estrelas[i].vy = (estrelas[i].vy * estrelas[i].massa + estrelas[j].vy * estrelas[j].massa) / massa_total
                    estrelas[i].massa = massa_total
                    estrelas[i].raio = (estrelas[i].raio ** 3 + estrelas[j].raio ** 3) ** (1 / 3)
                    estrelas[j].ativo = False  # Desativar estrela j
                else:  # Estrela j absorve i
                    massa_total = estrelas[j].massa + estrelas[i].massa
                    estrelas[j].vx = (estrelas[j].vx * estrelas[j].massa + estrelas[i].vx * estrelas[i].massa) / massa_total
                    estrelas[j].vy = (estrelas[j].vy * estrelas[j].massa + estrelas[i].vy * estrelas[i].massa) / massa_total
                    estrelas[j].massa = massa_total
                    estrelas[j].raio = (estrelas[j].raio ** 3 + estrelas[i].raio ** 3) ** (1 / 3)
                    estrelas[i].ativo = False  # Desativar estrela i

    # Verificar colisões entre planetas
    for i in range(NUM_PLANETAS):
        if not planetas[i].ativo:
            continue
        for j in range(i + 1, NUM_PLANETAS):
            if not planetas[j].ativo:
                continue

            # Calcular a distância entre dois planetas
            dx_planetas = planetas[j].x - planetas[i].x
            dy_planetas = planetas[j].y - planetas[i].y
            distancia_planetas = math.sqrt(dx_planetas ** 2 + dy_planetas ** 2)

            if distancia_planetas <= (planetas[i].raio + planetas[j].raio):  # Colisão detectada
                if planetas[i].massa >= planetas[j].massa:  # Planeta i absorve j
                    massa_total = planetas[i].massa + planetas[j].massa
                    planetas[i].vx = (planetas[i].vx * planetas[i].massa + planetas[j].vx * planetas[j].massa) / massa_total
                    planetas[i].vy = (planetas[i].vy * planetas[i].massa + planetas[j].vy * planetas[j].massa) / massa_total
                    planetas[i].massa = massa_total
                    planetas[i].raio = (planetas[i].raio ** 3 + planetas[j].raio ** 3) ** (1 / 3)
                    planetas[j].ativo = False  # Desativar planeta j
                else:  # Planeta j absorve i
                    massa_total = planetas[j].massa + planetas[i].massa
                    planetas[j].vx = (planetas[j].vx * planetas[j].massa + planetas[i].vx * planetas[i].massa) / massa_total
                    planetas[j].vy = (planetas[j].vy * planetas[j].massa + planetas[i].vy * planetas[i].massa) / massa_total
                    planetas[j].massa = massa_total
                    planetas[j].raio = (planetas[j].raio ** 3 + planetas[i].raio ** 3) ** (1 / 3)
                    planetas[i].ativo = False  # Desativar planeta i

# Função para calcular a interação gravitacional entre duas estrelas
def calcular_gravidade_estrela(a, b):
    """
    Calcula a interação gravitacional entre duas estrelas.

    Parâmetros:
    a (Estrela): Primeira estrela envolvida na interação
    b (Estrela): Segunda estrela envolvida na interação

    Descrição:
    - Calcula a força gravitacional entre duas estrelas usando a Lei da Gravitação Universal
    - Atualiza as velocidades de ambas as estrelas com base na força gravitacional calculada
    - Evita divisão por zero com uma verificação de distância mínima

    Cálculos realizados:
    - Distância entre as estrelas
    - Força gravitacional
    - Componentes de aceleração nos eixos X e Y
    - Atualização das velocidades das estrelas

    Observações:
    - A função modifica diretamente as velocidades das estrelas passadas como parâmetro
    - Usa constante gravitacional G definida previamente no código
    """
    
    # Calcula a distância entre as estrelas nos eixos x e y
    dx = b.x - a.x
    dy = b.y - a.y
    distancia = math.sqrt(dx * dx + dy * dy)

    # Verifica se a distância é maior que um limite mínimo
    if distancia > 0.01:  # Evitar divisão por zero
        # Calcula a força gravitacional
        forca = G * a.massa * b.massa / (distancia * distancia)

        # Calcula acelerações para a estrela A
        ax_a = forca * dx / distancia / a.massa
        ay_a = forca * dy / distancia / a.massa

        # Calcula acelerações para a estrela B (em direção oposta)
        ax_b = -forca * dx / distancia / b.massa
        ay_b = -forca * dy / distancia / b.massa

        # Atualiza as velocidades das estrelas
        a.vx += ax_a
        a.vy += ay_a

        b.vx += ax_b
        b.vy += ay_b


# Função para atualizar a posição das estrelas na simulação
def atualizar_estrelas():
    """
    Atualiza as posições e velocidades de todas as estrelas na simulação.

    Processo:
    1. Itera sobre todas as estrelas ativas
    2. Calcula interações gravitacionais entre estrelas
    3. Atualiza posições baseado nas velocidades
    """
    for i in range(NUM_ESTRELAS):
        # Pula estrelas inativas
        if not estrelas[i].ativo:
            continue

        # Calcula interações gravitacionais com outras estrelas
        for j in range(i + 1, NUM_ESTRELAS):
            if estrelas[j].ativo:
                calcular_gravidade_estrela(estrelas[i], estrelas[j])

        # Atualiza posição da estrela baseado na velocidade
        estrelas[i].x += estrelas[i].vx
        estrelas[i].y += estrelas[i].vy


def atualizar_planetas():
    """
    Atualiza as posições e velocidades dos planetas na simulação.

    Processo:
    1. Itera sobre todos os planetas ativos
    2. Calcula forças gravitacionais de cada estrela sobre o planeta
    3. Atualiza velocidade e posição do planeta
    """
    for i in range(NUM_PLANETAS):
        # Processa apenas planetas ativos
        if planetas[i].ativo:
            # Calcula interação gravitacional com todas as estrelas
            for j in range(NUM_ESTRELAS):
                # Calcula distância entre planeta e estrela
                dx = estrelas[j].x - planetas[i].x
                dy = estrelas[j].y - planetas[i].y
                distancia = math.sqrt(dx ** 2 + dy ** 2)
                
                # Calcula força gravitacional se a distância for válida
                if distancia > 0:
                    F = G * estrelas[j].massa * planetas[i].massa / (distancia ** 2)
                    ax = F * dx / distancia / planetas[i].massa
                    ay = F * dy / distancia / planetas[i].massa
                    
                    # Atualiza velocidade do planeta
                    planetas[i].vx += ax
                    planetas[i].vy += ay
            
            # Atualiza posição do planeta
            planetas[i].x += planetas[i].vx
            planetas[i].y += planetas[i].vy

def desenhar_objeto(x_virtual: float, y_virtual: float, raio: float, cor):
    # Converte as coordenadas do espaço virtual para o espaço da tela (com escala)
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA

    # Desenha o círculo na tela
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))
    # pygame.draw.rect(tela, cor, pygame.Rect(int(x_tela), int(y_tela), int(raio_tela*2), int(raio_tela*2)))


def desenhar_estrelas():
    """
    Desenha todas as estrelas ativas na tela.

    Processo:
    1. Itera sobre todas as estrelas
    2. Verifica se a estrela está ativa
    3. Imprime os valores RGB da cor da estrela (para depuração)
    4. Desenha a estrela na posição atual com sua cor e raio
    
    Observações:
    - Usa a função desenhar_objeto() para renderizar cada estrela
    - Imprime valores de cor (r, g, b) para possível análise ou debug
    """
    for estrela in estrelas:
        if estrela.ativo:
            # Extrai valores RGB da cor da estrela
            r = estrela.cor[0]  
            g = estrela.cor[1]
            b = estrela.cor[2]
            
            # Imprime valores de cor para depuração
            print(r)
            print(g)
            print(b)
            
            # Desenha a estrela na tela
            desenhar_objeto(estrela.x, estrela.y, estrela.raio, (r, g, b))


def desenhar_planetas():
    """
    Desenha todos os planetas ativos na tela.

    Processo:
    1. Itera sobre todos os planetas
    2. Verifica se o planeta está ativo
    3. Desenha o planeta em sua posição atual com sua cor e raio específicos
    
    Diferenças em relação a desenhar_estrelas():
    - Não imprime valores de cor
    - Usa diretamente a cor do planeta
    """
    for planeta in planetas:
        if planeta.ativo:
            # Desenha o planeta na tela com sua cor original
            desenhar_objeto(planeta.x, planeta.y, planeta.raio, planeta.cor)

# Loop principal da simulação
rodando = True  # Flag para controle do loop principal
simulacao_ativa = False  # Estado inicial da simulação (não iniciada)

grafico_tempo_real = GraficoTempoReal()

while rodando:
    """
    Ciclo principal de execução do programa.
    Gerencia eventos, atualização da interface e lógica da simulação.
    
    Componentes principais:
    1. Controle de taxa de quadros (FPS)
    2. Processamento de eventos do usuário
    3. Gerenciamento da interface gráfica
    4. Atualização e renderização da simulação
    """
    # Controla a taxa de quadros e calcula o tempo entre quadros
    tempo_delta = clock.tick(60) / 1000.0  # Limita a 60 FPS

    # Processamento de eventos do Pygame
    for evento in pygame.event.get():
        # Evento de fechamento da janela
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Redimensionamento da janela
        if evento.type == pygame.VIDEORESIZE:
            LARGURA, ALTURA = evento.size
            tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
            gerenciador_interface.set_window_resolution((LARGURA, ALTURA))
        
        # Atualização de valores dos sliders
        if evento.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if evento.ui_element == slider_estrelas:
                label_estrelas_valor.set_text(str(int(slider_estrelas.get_current_value())))
            elif evento.ui_element == slider_planetas:
                label_planetas_valor.set_text(str(int(slider_planetas.get_current_value())))
        
        # Processamento de eventos de botões
        if evento.type == pygame.USEREVENT:
            if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if evento.ui_element == botao_comecar:
                    # Iniciar simulação
                    atualizar_informacoes()
                    estrelas = criar_estrelas(NUM_ESTRELAS)
                    planetas = criar_planetas(NUM_PLANETAS)
                    simulacao_ativa = True

        # Processa eventos da interface gráfica
        gerenciador_interface.process_events(evento)

    # Atualiza a interface gráfica
    gerenciador_interface.update(tempo_delta)
    
    # Limpa a tela com cor preta
    tela.fill((0, 0, 0))  

    # Lógica da simulação (só executa quando ativa)
    if simulacao_ativa:
        verificar_colisoes()      # Verifica colisões entre objetos
        atualizar_estrelas()      # Atualiza posições das estrelas
        atualizar_planetas()      # Atualiza posições dos planetas
        desenhar_estrelas()       # Renderiza estrelas
        desenhar_planetas()       # Renderiza planetas
        grafico_tempo_real.atualizar(estrelas, planetas)
        grafico_tempo_real.desenhar_grafico(tela)

    # Desenha elementos da interface
    gerenciador_interface.draw_ui(tela)
    
    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
