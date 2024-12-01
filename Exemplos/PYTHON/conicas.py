"""
Simulação de Trajetórias Orbitais usando Pygame

Este programa utiliza o Pygame para simular uma trajetória orbital circular
ao redor de um centro de massa.

Classes e Funções:
- Sistema: Representa o sistema orbital, incluindo o centro de massa e o cálculo da trajetória.
- draw_text: Renderiza texto na tela com uma fonte configurada.
- main: Função principal que controla a lógica da simulação, eventos e renderização.

Configurações:
- Tela: Dimensão fixa de 800x600 pixels.
- Centro de Massa: Localizado no centro da tela.
- Cores: Definidas para elementos como rastro, corpo em movimento e centro de massa.
"""

import pygame
import math

# Inicializa o Pygame
pygame.init()

# Definições da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulação de Trajetórias Orbitais')

# Configurações de cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Fonte para renderizar texto
font = pygame.font.Font(None, 36)

class Sistema:
    """
    Classe para representar o sistema orbital.
    
    Atributos:
    - screen: Tela do Pygame onde os elementos serão desenhados.
    - width, height: Dimensões da tela.
    - origem: Posição central da tela.
    - centro_massa: Posição do centro de massa (fixo no centro da tela).
    """
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.origem = [width // 2, height // 2]  # Centro da tela
    
    def calcular_orbita(self, angle):
        """
        Calcula as coordenadas (x, y) de um corpo em órbita ao redor do centro de massa.
        
        Parâmetros:
        - angle: Ângulo em radianos para determinar a posição orbital.
        
        Retorna:
        - (x, y): Coordenadas ajustadas para a posição central da tela.
        """
        c = 100 # Constante de escala da órbita
        e = 1.5 # Excentricidade
        x = (c*math.cos(angle))/(1 + e*math.cos(angle)) + self.origem[0]
        y = (c*math.sin(angle))/(1 + e*math.cos(angle)) + self.origem[1]
        
        return x, y

    def desenhar_origem(self):
        """
        Desenha o centro de massa na tela como um círculo vermelho.
        """
        pygame.draw.circle(self.screen, RED, self.origem, 5)

def draw_text(screen, text, position, color=WHITE):
    """
    Renderiza texto na tela em uma posição específica.
    
    Parâmetros:
    - screen: Tela do Pygame onde o texto será desenhado.
    - text: Texto a ser renderizado.
    - position: Posição (x, y) onde o texto será exibido.
    - color: Cor do texto (branco por padrão).
    """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def main():
    """
    Função principal que controla a lógica do programa.
    
    - Cria um objeto da classe Sistema.
    - Atualiza e renderiza a posição do corpo, rastro e centro de massa.
    - Exibe informações na tela.
    """
    running = True
    clock = pygame.time.Clock()
    sistema = Sistema(screen, width, height)
    
    angle = 0  # Ângulo inicial da trajetória
    trail = []  # Rastro da trajetória

    while running:
        screen.fill(BLACK)
        
        # Manipula eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Atualiza a posição do corpo
        x, y = sistema.calcular_orbita(angle)
        
        # Adiciona a posição atual ao rastro
        trail.append((int(x), int(y)))
        if len(trail) > 200:  # Limita o comprimento do rastro
            trail.pop(0)

        # Desenha o centro de massa
        sistema.desenhar_origem()

        # Desenha o rastro da trajetória
        if len(trail) > 1:
            pygame.draw.lines(screen, WHITE, False, trail, 2)

        # Desenha o corpo em movimento
        pygame.draw.circle(screen, BLUE, (int(x), int(y)), 8)

        # Renderiza o nome da trajetória
        draw_text(screen, "Trajetória", (10, 10))

        # Atualiza o ângulo
        angle += 0.05

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)  # Limita a taxa de atualização da tela para 30 FPS

    pygame.quit()

# Executa o programa principal
if __name__ == '__main__':
    main()
