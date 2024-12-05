"""
Simulação de Transferência Orbital de Hohmann

Descrição do Projeto:
Esta simulação em Python utiliza a biblioteca Pygame para demonstrar a transferência orbital de Hohmann, 
um método fundamental na mecânica orbital para mudar a órbita de um corpo celeste entre duas órbitas circulares.

O que é a Transferência de Hohmann?
A transferência de Hohmann é uma técnica de mudança de órbita que utiliza a menor quantidade de energia possível 
para transferir um corpo de uma órbita circular para outra. No nosso caso, a simulação mostra a transferência de 
uma órbita inicial com raio R para uma órbita final com raio 2R, passando por uma trajetória elíptica intermediária.

Como Funciona a Simulação:

Componentes Principais:
 - Uma estrela central (amarela) com massa fixa
 - Um corpo celeste secundário (azul) que realiza a transferência orbital

Controles:
 - Tecla Espaço: Ativa/Desativa a transferência orbital
 - Quando ativada, o corpo celeste azul iniciará a transferência de Hohmann

Detalhes Técnicos:
 - Simulação usa física gravitacional newtoniana
 - Escala virtual para representar grandes distâncias
 - Visualização em tempo real da trajetória orbital

 Passos para Executar:
 1. Certifique-se de ter Python instalado
 2. Instale as bibliotecas necessárias:
    pip install pygame
 3. Execute o script Python
 4. Observe a simulação da transferência orbital
 5. Pressione a tecla Espaço para iniciar/parar a transferência
 6. Feche a janela para encerrar a simulação

Observações:
 - A simulação demonstra os princípios básicos da transferência orbital
 - Variáveis como escala, massa e velocidade podem ser ajustadas no código
 - Ideal para entusiastas de astronomia, física e mecânica orbital

Divirta-se explorando a mecânica celeste!
"""
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

def calcular_raio(massa):
    """
    Calcula o raio de um corpo celeste baseado em sua massa.

    Argumento:
        massa (float): Massa do corpo celeste.

    Retorno:
        float: Raio calculado do corpo celeste, ajustado pela constante de proporcionalidade.
    """
    return (massa ** (1/3)) * RAIO_PROPORCIONALIDADE

class CorpoCeleste:
    """
    Representa um corpo celeste com propriedades físicas e de movimento.

    Atributos:
        x (float): Coordenada x do corpo no espaço virtual.
        y (float): Coordenada y do corpo no espaço virtual.
        vx (float): Velocidade na direção x.
        vy (float): Velocidade na direção y.
        massa (float): Massa do corpo celeste.
        raio (float): Raio do corpo celeste.
        ativo (bool): Indica se o corpo está ativo na simulação.
        trajetoria (list): Histórico de posições do corpo.
        orbitaeliptica (bool): Indica se o corpo está em mudança de órbita.
        transferencia (bool): Indica se o usuário deseja mudar a órbita.
    """

    def __init__(self, x, y, vx, vy, massa, raio):
        """
        Inicializa um novo corpo celeste.

        Args:
            x (float): Posição inicial x.
            y (float): Posição inicial y.
            vx (float): Velocidade inicial em x.
            vy (float): Velocidade inicial em y.
            massa (float): Massa do corpo.
            raio (float): Raio do corpo.
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.raio = raio
        self.ativo = True
        self.trajetoria = []  # Histórico da trajetória
        self.orbitaeliptica = False # Verifica se o corpo está mudando de orbita
        self.transferencia = False # Variavel que checa se o usuario quer mudar de orbita

    def atualizar_trajetoria(self):
        """
        Atualiza o histórico de trajetória do corpo celeste.

        Limita o número de pontos armazenados a 10.000 para eficiência de memória.
        Adiciona a posição atual à lista de trajetória.
        """
        if len(self.trajetoria) > 10000:  # Limitar o número de pontos armazenados
            self.trajetoria.pop(0)
        self.trajetoria.append((self.x, self.y))

class Estrela(CorpoCeleste):
    """
    Subclasse de CorpoCeleste representando uma estrela.
    
    Atualmente não adiciona novos comportamentos, serve como um marcador 
    para objetos estelares na simulação.
    """
    pass

def criar_estrelas(num_estrelas):
    """
    Cria um conjunto de estrelas para a simulação.

    Args:
        num_estrelas (int): Número de estrelas a serem criadas.

    Returns:
        list: Lista de objetos Estrela criados.

    Comportamento:
    - Sempre cria uma estrela central fixa
    - Se num_estrelas > 1, cria uma segunda estrela em órbita circular
    """
    estrelas = []

    # Estrela central
    x_sol = ESPACO_VIRTUAL_LARGURA / 2
    y_sol = ESPACO_VIRTUAL_ALTURA / 2
    massa_sol = 2000000000
    raio = calcular_raio(massa_sol)
    estrelas.append(Estrela(x_sol, y_sol, 0, 0, massa_sol, raio))

    
    # Calcular parâmetros orbitais para órbita circular
    distancia_orbital = 30000  # Distância da estrela central
    massa_central = estrelas[0].massa
    
    # Calcular velocidade orbital para órbita circular
    # v = sqrt(G * M / r)
    velocidade_orbital = math.sqrt(G * massa_central / distancia_orbital)
    
    # Posicionar a segunda estrela em órbita circular
    angulo = math.pi / 4  # Ângulo de 45 graus, ajustável
    x = x_sol + distancia_orbital * math.cos(angulo)
    y = y_sol + distancia_orbital * math.sin(angulo)
    
    # Velocidade tangencial para órbita circular
    vx = -velocidade_orbital * math.sin(angulo)
    vy = velocidade_orbital * math.cos(angulo)
    
    massa = 100000
    raio = calcular_raio(massa) * 10
    estrelas.append(CorpoCeleste(x, y, vx, vy, massa, raio))

    return estrelas

def calcular_gravidade_estrela(a, b):
    """
    Calcula e aplica a força gravitacional entre dois corpos celestes.

    Args:
        a (CorpoCeleste): Primeiro corpo celeste.
        b (CorpoCeleste): Segundo corpo celeste.

    Comportamento:
    - Calcula a força gravitacional entre os dois corpos
    - Atualiza as velocidades de ambos os corpos baseado na força gravitacional
    """
    dx = b.x - a.x # Distância relativa entre os dois corpos no eixo x (dx)
    dy = b.y - a.y # Distância relativa entre os dois corpos no eixo y (dy)
    distancia = math.sqrt(dx * dx + dy * dy) # Distancia entre os dois corpos

    if distancia > 0.01:
        forca = G * a.massa * b.massa / (distancia * distancia) # Força gravitacional
        
        # Aceleração do corpo a no eixo x e y
        ax_a = forca * dx / distancia / a.massa
        ay_a = forca * dy / distancia / a.massa
        
        # Aceleração do corpo b no eixo x e y
        ax_b = -forca * dx / distancia / b.massa
        ay_b = -forca * dy / distancia / b.massa
        
        # Aplicação do teorema de Euler para velocidade
        # Atualização da velocidade no corpo a
        a.vx += ax_a
        a.vy += ay_a
        # Atualização da velocidade no corpo b
        b.vx += ax_b
        b.vy += ay_b

def atualizar_estrelas(estrelas):
    """
    Atualiza as posições e velocidades de todas as estrelas na simulação.

    Args:
        estrelas (list): Lista de corpos celestes a serem atualizados.

    Comportamento:
    - Calcula interações gravitacionais entre estrelas ativas
    - Atualiza posições das estrelas
    - Registra trajetória de cada estrela
    """
    for i in range(len(estrelas)):
        if not estrelas[i].ativo:
            continue
        for j in range(i + 1, len(estrelas)):
            if estrelas[j].ativo:
                calcular_gravidade_estrela(estrelas[i], estrelas[j])
        estrelas[i].x += estrelas[i].vx
        estrelas[i].y += estrelas[i].vy
        estrelas[i].atualizar_trajetoria()

def desenhar_objeto(x_virtual, y_virtual, raio, cor):
    """
    Desenha um objeto circular na tela.

    Args:
        x_virtual (float): Posição x no espaço virtual.
        y_virtual (float): Posição y no espaço virtual.
        raio (float): Raio do objeto.
        cor (tuple): Cor RGB do objeto.
    """
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))

def desenhar_trajetoria(estrela, cor):
    """
    Desenha a trajetória de um corpo celeste.

    Args:
        estrela (CorpoCeleste): Corpo celeste cuja trajetória será desenhada.
        cor (tuple): Cor RGB da trajetória.
    """
    if estrela.ativo and estrela.trajetoria:
        pontos_tela = [(int(pos[0] / ESCALA), int(pos[1] / ESCALA)) for pos in estrela.trajetoria]
        if len(pontos_tela) > 1:
            pygame.draw.lines(tela, cor, False, pontos_tela, 1)

def desenhar_estrelas(estrelas):
    """
    Desenha as trajetórias e estrelas na simulação.

    Args:
        estrelas (list): Lista de corpos celestes a serem desenhados.

    Comportamento:
    - Desenha trajetórias em cores específicas
    - Desenha estrelas em cores específicas baseado no índice
    """
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

def main():
    """
    Função principal que executa a simulação de corpos celestes.

    Comportamento:
    - Inicializa as estrelas
    - Gerencia o loop principal do Pygame
    - Permite interação para transferência orbital
    - Atualiza e desenha os corpos celestes
    """
    # Inicializar estrelas
    estrelas = criar_estrelas(NUM_ESTRELAS)

    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                # Não permitir/permitir transferência de orbita.
                if evento.key == pygame.K_SPACE:
                    estrelas[1].transferencia = not (estrelas[1].transferencia)    
                                
        # Lógica de transferência orbital
        if(estrelas[1].transferencia and abs(estrelas[1].y - (ESPACO_VIRTUAL_ALTURA / 2)) < 300):
            if(not estrelas[1].orbitaeliptica):
                # Aceleração necessária para o corpo iniciar transferência de Hohmann.
                estrelas[1].vx *= 1.15
                estrelas[1].vy *= 1.15
                # Corpo está em uma trajetória eliptica.
                estrelas[1].orbitaeliptica = True
            else:
                # Aceleração necessária para o corpo fixar na trajetória circular.
                estrelas[1].vx *= 1.22
                estrelas[1].vy *= 1.22
                # Corpo não está mais na transferência de trajetória.
                estrelas[1].orbitaeliptica = False
        
        # Limpar tela
        tela.fill((0, 0, 0))
        
        # Atualizar e desenhar
        atualizar_estrelas(estrelas)
        desenhar_estrelas(estrelas)
        
        # Atualizar display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()