"""
Simulação Gravitacional com Corpos Celestes

Descrição:
Este programa simula interações gravitacionais entre corpos celestes utilizando o princípio da gravitação universal de Newton. 
Os corpos celestes (estrelas) interagem em um espaço virtual onde forças gravitacionais afetam suas velocidades e posições. 
O programa inclui funcionalidades como detecção de colisões, fusão de corpos em caso de colisão, e representação visual 
usando Pygame e Pygame GUI para controle da simulação.

Funcionalidades principais:
- Simulação de forças gravitacionais entre corpos.
- Representação gráfica dos corpos e suas trajetórias.
- Detecção e fusão de corpos celestes em caso de colisão.
- Interface para configurar a simulação, incluindo posicionamento inicial e propriedades dos corpos.
- Botão para reiniciar a simulação com parâmetros atualizados.

Estrutura:
1. Classe `CorpoCeleste`: Representa corpos celestes com atributos como posição, velocidade, massa e histórico de trajetórias.
2. Funções auxiliares:
   - `calcular_gravidade_estrela`: Calcula as forças gravitacionais entre dois corpos.
   - `verificar_colisoes`: Detecta e processa colisões entre corpos.
   - `atualizar_estrelas`: Atualiza posições e trajetórias dos corpos.
   - `desenhar_objeto` e `desenhar_trajetoria`: Gerenciam a visualização gráfica.
3. Interface gráfica:
   - Configuração inicial com campos para definir as propriedades das estrelas.
   - Botão para reiniciar a simulação.

Dependências:
- Pygame
- Pygame GUI

Instruções de uso:
- Execute o programa para iniciar a tela de configuração, onde é possível definir as propriedades iniciais dos corpos celestes.
- Inicie a simulação para visualizar as interações gravitacionais.
- Use o botão "Reiniciar Simulação" para ajustar parâmetros e reiniciar a simulação.

Constantes principais:
- `G`: Constante gravitacional.
- `ESCALA`: Fator de escala para converter coordenadas do espaço virtual para a tela.
- `COLISAO`: Ativa ou desativa a detecção de colisões.

"""


import pygame
import pygame_gui as pg_gui
import math
import random

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 950, 950
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação Gravitacional")
clock = pygame.time.Clock()

### PARÂMETROS DA SIMULAÇÃO ###
G = 6.67430                                 # Constante gravitacional
RAIO_PROPORCIONALIDADE = 10                 # Constante de ajuste para o raio
ESCALA = 100                                # Fator de escala
COLISAO = 1                                 # 1 ativado, 0 desativado
ESPACO_VIRTUAL_LARGURA = LARGURA * ESCALA
ESPACO_VIRTUAL_ALTURA = ALTURA * ESCALA

# Funções auxiliares
def calcular_raio(massa):
    return (massa ** (1/3)) * RAIO_PROPORCIONALIDADE

class CorpoCeleste:

    """
    Classe base para representar corpos celestes genéricos
        
    Atributos:
        x (float): Coordenada x no espaço
        y (float): Coordenada y no espaço
        vx (float): Velocidade no eixo x
        vy (float): Velocidade no eixo y
        massa (float): Massa do corpo celeste
        raio (float): Raio do corpo celeste
        ativo (bool): Estado do corpo (True se ativo, False se desativado)
        cor (tuple): Cor do corpo no formato RGB
    """

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


def verificar_colisoes(estrelas):
    """
    Verifica colisões entre objetos do tipo 'estrela' e realiza a fusão quando ocorre uma colisão.

    Explicação da função:
    Esta função percorre uma lista de objetos do tipo 'estrela' e verifica se há colisões entre elas. 
    Caso duas estrelas colidam (a distância entre os centros for menor ou igual à soma de seus raios), 
    elas se fundem em uma única estrela. A estrela resultante possui uma massa total equivalente à soma 
    das massas das estrelas envolvidas, uma nova velocidade calculada pela conservação do momento linear 
    e um novo raio proporcional ao volume combinado das estrelas.

    Parâmetros:
        estrelas (list): Lista de objetos representando estrelas.

    Retorno:
        None: A função modifica a lista `estrelas` diretamente, atualizando os atributos das estrelas 
        envolvidas em colisões e desativando as estrelas que foram absorvidas.
    """

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

                # Velocidade resultante
                vx_resultante = (estrelas[i].vx * estrelas[i].massa + estrelas[j].vx * estrelas[j].massa) / massa_total
                vy_resultante = (estrelas[i].vy * estrelas[i].massa + estrelas[j].vy * estrelas[j].massa) / massa_total

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

def calcular_gravidade_estrela(a, b):
    """
    Calcula e aplica as forças gravitacionais entre duas estrelas, atualizando suas velocidades.

    Explicação da função:
    Esta função calcula a força gravitacional entre duas estrelas (a e b) com base na lei da gravitação universal 
    de Newton. A força é aplicada para atualizar as velocidades de ambas as estrelas, considerando suas massas 
    e posições relativas. Para evitar problemas numéricos com distâncias muito pequenas, há um limite mínimo 
    definido como 0.01.

    Parâmetros:
        a (objeto): Objeto representando a primeira estrela.
        b (objeto): Objeto representando a segunda estrela. 

    Retorno:
        None: A função modifica diretamente os atributos `vx` e `vy` das estrelas `a` e `b`, 
        atualizando suas velocidades de acordo com a interação gravitacional.

    Constantes utilizadas:
        G (float): Constante gravitacional.
    """
    # Calcula as diferenças nas posições (distância em x e y) entre as estrelas a e b
    dx = b.x - a.x
    dy = b.y - a.y

    # Calcula a distância euclidiana entre as duas estrelas
    distancia = math.sqrt(dx * dx + dy * dy)

    # Verifica se a distância é maior que um valor mínimo para evitar divisões por zero ou forças excessivas
    if distancia > 0.01:
        # Calcula a força gravitacional usando a lei da gravitação universal
        forca = G * a.massa * b.massa / (distancia * distancia)
        
        # Calcula as componentes da aceleração de a devido à força gravitacional de b
        ax_a = forca * dx / distancia / a.massa
        ay_a = forca * dy / distancia / a.massa
        
        # Calcula as componentes da aceleração de b devido à força gravitacional de a (em direção oposta)
        ax_b = -forca * dx / distancia / b.massa
        ay_b = -forca * dy / distancia / b.massa

        # Atualiza as velocidades de a com base nas acelerações calculadas
        a.vx += ax_a
        a.vy += ay_a

        # Atualiza as velocidades de b com base nas acelerações calculadas
        b.vx += ax_b
        b.vy += ay_b



def atualizar_estrelas(estrelas):
    # Itera sobre todas as estrelas
    for i in range(len(estrelas)):
        if not estrelas[i].ativo:
            continue  # Ignora estrelas inativas
        # Calcula a interação gravitacional com as outras estrelas
        for j in range(i + 1, len(estrelas)):
            if estrelas[j].ativo:
                calcular_gravidade_estrela(estrelas[i], estrelas[j])
        # Atualiza a posição da estrela com base em sua velocidade
        estrelas[i].x += estrelas[i].vx
        estrelas[i].y += estrelas[i].vy
        # Atualiza o histórico de posições da estrela
        estrelas[i].atualizar_trajetoria()

def desenhar_objeto(x_virtual, y_virtual, raio, cor):
    # Converte coordenadas do espaço virtual para coordenadas da tela
    x_tela = x_virtual / ESCALA
    y_tela = y_virtual / ESCALA
    raio_tela = raio / ESCALA
    # Desenha o círculo representando o objeto
    pygame.draw.circle(tela, cor, (int(x_tela), int(y_tela)), int(raio_tela))

def desenhar_trajetoria(estrela, cor):
    # Desenha a trajetória de uma estrela se ela estiver ativa e tiver histórico
    if estrela.ativo and estrela.trajetoria:
        # Converte as posições da trajetória para coordenadas da tela
        pontos_tela = [(int(pos[0] / ESCALA), int(pos[1] / ESCALA)) for pos in estrela.trajetoria]
        if len(pontos_tela) > 1:
            # Desenha linhas conectando os pontos da trajetória
            pygame.draw.lines(tela, cor, False, pontos_tela, 1)

def gerar_cores_unicas(num_estrelas):
    # Gera uma lista de cores únicas para cada estrela
    random.seed(20)  # Define uma semente para resultados consistentes
    return [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(num_estrelas)]

def desenhar_estrelasN(estrelas):
    cores = gerar_cores_unicas(len(estrelas))  # Gera cores para todas as estrelas
    
    # Primeiro, desenha todas as trajetórias
    for idx, estrela in enumerate(estrelas):
        desenhar_trajetoria(estrela, cores[idx])

    # Depois, desenha as estrelas ativas
    for idx, estrela in enumerate(estrelas):
        if estrela.ativo:
            desenhar_objeto(estrela.x, estrela.y, estrela.raio, cores[idx])

def criar_botao_reiniciar(gerenciador):
    """Cria um botão de reinício na tela de simulação"""
    botao_reiniciar = pg_gui.elements.UIButton(
        relative_rect=pygame.Rect((LARGURA - 250, 10), (200, 50)),  # Define posição e tamanho do botão
        text='Reiniciar Simulação',  # Texto exibido no botão
        manager=gerenciador  # Gerenciador de interface gráfica
    )
    return botao_reiniciar

# [Mantenha o código anterior até a função main()]
def tela_configuracao(valores_primeira_simulacao=None, valores_ultima_simulacao=None):
    # Configurações do Pygame GUI
    gerenciador = pg_gui.UIManager((LARGURA, ALTURA), 'theme.json')
    
    # Posicionamento dos elementos
    pos_x_inicial = LARGURA // 4
    espacamento_y = 50
    
    # Elementos de entrada para o número de estrelas
    label_num_estrelas = pg_gui.elements.UILabel(
        relative_rect=pygame.Rect((pos_x_inicial, 50), (300, 30)),
        text='Número de Estrelas:',
        manager=gerenciador
    )
    
    # Dropdown para escolher configuração inicial
    opcoes_configuracao = ['Nova Configuração', 'Primeira Simulação', 'Última Simulação']
    dropdown_configuracao = pg_gui.elements.UIDropDownMenu(
        options_list=opcoes_configuracao,
        starting_option='Nova Configuração',
        relative_rect=pygame.Rect((pos_x_inicial + 350, 50), (200, 30)),
        manager=gerenciador
    )
    
    # Determinar número inicial de estrelas e valores iniciais
    num_estrelas_inicial = 0
    valores_selecionados = None
    
    entrada_num_estrelas = pg_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((pos_x_inicial + 250, 50), (100, 30)),
        manager=gerenciador
    )
    
    # Texto para mensagens de erro
    label_erro = pg_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, ALTURA - 150), (LARGURA - 100, 50)),
        text='',
        manager=gerenciador
    )
    
    # Listas para armazenar entradas dinâmicas
    labels_estrelas = []
    entradas_x = []
    entradas_y = []
    entradas_massa = []
    entradas_vx = []
    entradas_vy = []
    
    def criar_entradas_estrelas(num_estrelas, valores=None):
        # Limpar entradas antigas, se existirem
        for label in labels_estrelas:
            label.kill()
        for entrada in entradas_x + entradas_y + entradas_massa + entradas_vx + entradas_vy:
            entrada.kill()
        
        labels_estrelas.clear()
        entradas_x.clear()
        entradas_y.clear()
        entradas_massa.clear()
        entradas_vx.clear()
        entradas_vy.clear()
        
        # Criar novas entradas para cada estrela
        for i in range(num_estrelas):
            # Labels
            label_estrela = pg_gui.elements.UILabel(
                relative_rect=pygame.Rect((50, 150 + i * espacamento_y), (300, 30)),
                text=f'Estrela {i+1}:',
                manager=gerenciador
            )
            labels_estrelas.append(label_estrela)
            
            # Preparar valores padrão
            valor_x = ''
            valor_y = ''
            valor_massa = ''
            valor_vx = ''
            valor_vy = ''
            
            # Se houver valores anteriores, preencher com esses valores
            if valores and i < len(valores):
                valor_x = str(int((valores[i].x - (ESPACO_VIRTUAL_LARGURA / 2))))
                valor_y = str(int(-(valores[i].y - (ESPACO_VIRTUAL_ALTURA / 2))))
                valor_massa = str(int(valores[i].massa))
                valor_vx = str(int(valores[i].vx))
                valor_vy = str(int(-valores[i].vy))
            
            # Entradas para cada estrela
            entrada_x = pg_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((pos_x_inicial, 150 + i * espacamento_y), (100, 30)),
                placeholder_text='x',
                manager=gerenciador
            )
            entrada_x.set_text(valor_x)
            
            entrada_y = pg_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((pos_x_inicial + 120, 150 + i * espacamento_y), (100, 30)),
                placeholder_text='y',
                manager=gerenciador
            )
            entrada_y.set_text(valor_y)
            
            entrada_massa = pg_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((pos_x_inicial + 240, 150 + i * espacamento_y), (100, 30)),
                placeholder_text='Massa',
                manager=gerenciador
            )
            entrada_massa.set_text(valor_massa)
            
            entrada_vx = pg_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((pos_x_inicial + 360, 150 + i * espacamento_y), (100, 30)),
                placeholder_text='Vel X',
                manager=gerenciador
            )
            entrada_vx.set_text(valor_vx)
            
            entrada_vy = pg_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((pos_x_inicial + 480, 150 + i * espacamento_y), (100, 30)),
                placeholder_text='Vel Y',
                manager=gerenciador
            )
            entrada_vy.set_text(valor_vy)
            
            entradas_x.append(entrada_x)
            entradas_y.append(entrada_y)
            entradas_massa.append(entrada_massa)
            entradas_vx.append(entrada_vx)
            entradas_vy.append(entrada_vy)

    def main_configuracao_loop():
        nonlocal num_estrelas_inicial, valores_selecionados
        configuracao_concluida = False
        estrelas = []

        while not configuracao_concluida:
            tempo_delta = clock.tick(60)/1000.0
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                
                if evento.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if evento.ui_element == dropdown_configuracao:
                        # Resetar campos baseado na seleção
                        if evento.text == 'Nova Configuração':
                            valores_selecionados = None
                            entrada_num_estrelas.set_text('')
                            criar_entradas_estrelas(0)
                        elif evento.text == 'Primeira Simulação' and valores_primeira_simulacao:
                            valores_selecionados = valores_primeira_simulacao
                            num_estrelas_inicial = len(valores_primeira_simulacao)
                            entrada_num_estrelas.set_text(str(num_estrelas_inicial))
                            criar_entradas_estrelas(num_estrelas_inicial, valores_primeira_simulacao)
                        elif evento.text == 'Última Simulação' and valores_ultima_simulacao:
                            valores_selecionados = valores_ultima_simulacao
                            num_estrelas_inicial = len(valores_ultima_simulacao)
                            entrada_num_estrelas.set_text(str(num_estrelas_inicial))
                            criar_entradas_estrelas(num_estrelas_inicial, valores_ultima_simulacao)
                
                if evento.type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                    if evento.ui_element == entrada_num_estrelas:
                        try:
                            num_estrelas = int(evento.text)
                            criar_entradas_estrelas(num_estrelas, valores_selecionados)
                            num_estrelas_inicial = num_estrelas
                        
                        except ValueError:
                            label_erro.set_text("Entrada inválida para número de estrelas!")
                
                if evento.type == pg_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == botao_iniciar:
                        # Validar e coletar entradas
                        try:
                            # Verificar se número de estrelas foi definido
                            if num_estrelas_inicial == 0:
                                label_erro.set_text("Defina o número de estrelas primeiro!")
                                continue
                            
                            estrelas = []
                            for i in range(num_estrelas_inicial):
                                # Verificar se todos os campos estão preenchidos
                                x_texto = entradas_x[i].get_text().strip()
                                y_texto = entradas_y[i].get_text().strip()
                                massa_texto = entradas_massa[i].get_text().strip()
                                vx_texto = entradas_vx[i].get_text().strip()
                                vy_texto = entradas_vy[i].get_text().strip()
                                
                                if not (x_texto and y_texto and massa_texto and vx_texto and vy_texto):
                                    label_erro.set_text(f"Preencha todos os campos para a Estrela {i+1}!")
                                    break
                                
                                x = (float(x_texto) + (ESPACO_VIRTUAL_LARGURA / 2))
                                y = (-float(y_texto) + (ESPACO_VIRTUAL_ALTURA / 2))
                                massa = (float(massa_texto))
                                vx = float(vx_texto)
                                vy = -float(vy_texto)
                                
                                raio = calcular_raio(massa)
                                estrela = CorpoCeleste(x, y, vx, vy, massa, raio)
                                estrelas.append(estrela)
                            else:  # Se o loop completar sem break
                                configuracao_concluida = True
                                label_erro.set_text("")
                        
                        except ValueError as e:
                            label_erro.set_text(f"Erro de conversão: {str(e)}")
                
                gerenciador.process_events(evento)
            
            gerenciador.update(tempo_delta)
            
            tela.fill((0, 0, 0))
            gerenciador.draw_ui(tela)
            pygame.display.update()
        
        return estrelas

    # Botão de início
    botao_iniciar = pg_gui.elements.UIButton(
        relative_rect=pygame.Rect((LARGURA // 2 - 100, ALTURA - 100), (200, 50)),
        text='Iniciar Simulação',
        manager=gerenciador
    )

    return main_configuracao_loop()

def main():
    # Variáveis para armazenar os valores da primeira e última simulação
    valores_primeira_simulacao = None
    valores_ultima_simulacao = None
    
    # Flag para controlar o loop principal
    continuar_simulacao = True
    
    while continuar_simulacao:
        # Capturar os valores passados pelo usuário antes da simulação
        estrelas = tela_configuracao(valores_primeira_simulacao, valores_ultima_simulacao)
        
        if not estrelas:
            pygame.quit()
            return
        
        # Armazenar a primeira configuração imediatamente após a entrada do usuário
        if valores_primeira_simulacao is None:
            # Criar uma cópia dos valores originais passados pelo usuário
            valores_primeira_simulacao = [
                CorpoCeleste(
                    estrela.x, 
                    estrela.y, 
                    estrela.vx, 
                    estrela.vy, 
                    estrela.massa, 
                    estrela.raio
                ) for estrela in estrelas
            ]
        
        # Gerenciador para eventos durante a simulação
        gerenciador = pg_gui.UIManager((LARGURA, ALTURA))
        botao_reiniciar = criar_botao_reiniciar(gerenciador)
        
        # Loop principal
        rodando = True
        while rodando:
            tempo_delta = clock.tick(60)/1000.0
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    continuar_simulacao = False
                
                # Processar eventos do Pygame GUI
                gerenciador.process_events(evento)
                
                # Verificar clique no botão de reinício
                if evento.type == pg_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == botao_reiniciar:
                        # Armazenar valores da simulação atual para próxima iteração
                        valores_ultima_simulacao = [
                            CorpoCeleste(
                                estrela.x, 
                                estrela.y, 
                                estrela.vx, 
                                estrela.vy, 
                                estrela.massa, 
                                estrela.raio
                            ) for estrela in estrelas
                        ]
                        rodando = False  # Sair do loop de simulação atual
            
            # Atualizar gerenciador de GUI
            gerenciador.update(tempo_delta)
            
            tela.fill((0, 0, 0))
            
            if COLISAO == 1:
                verificar_colisoes(estrelas)
            atualizar_estrelas(estrelas)
            
            if len(estrelas) <= 3:
                cores = [(255, 255, 0), (100, 100, 255), (255, 255, 255)]
                for idx, estrela in enumerate(estrelas):
                    desenhar_trajetoria(estrela, cores[idx % len(cores)])
                    if estrela.ativo:
                        desenhar_objeto(estrela.x, estrela.y, estrela.raio, cores[idx % len(cores)])
            else:
                desenhar_estrelasN(estrelas)
            
            # Desenhar botão de reinício
            gerenciador.draw_ui(tela)
            
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
