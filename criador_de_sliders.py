import pygame as pg
import pygame_gui as pg_gui

# Tamanho dos sliders
SLIDER_LARG = 200
SLIDER_ALT = 20
LARGURA = 1250
def slider_estrelas(quant_estrelas,gui):
    """
    Retorna os objetos do slider do numero de estrelas
    """
    rot_quant_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((10, 10), (250, 50)), # Posição e tamanho do texto
    text = "Quantidade de Estrelas", # Texto a ser exibido
    manager = gui, 
    )
    rot_slider_quant_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((220, 10), (100, 50)), # Posição e tamanho do texto
    text = str(quant_estrelas), # numero de estrelas padrao em texto na tela
    manager = gui, 
    )
    slider_quant_estrelas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((30, 50), (SLIDER_LARG, SLIDER_ALT)), # Posição e tamanho do rótulo
    start_value = quant_estrelas, # Quantidade inicial padrão de estrelas
    value_range = (0, 500), # Limites do slider, se passar disso o pc nao guenta
    manager = gui,
    )
    return rot_quant_estrelas, rot_slider_quant_estrelas, slider_quant_estrelas

def slider_velocidade_min_estrelas(min_vel,gui):
    """
    Retorna os objetos do slider da velocidade minima das estrelas
    """
    rot_vel_inf_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((10, 70), (250, 50)),
    text = "Velocidade Mínima das Estrelas", 
    manager = gui, 
    )
    rot_slider_vel_inf_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((220, 70), (100, 50)), 
    text = str(min_vel), 
    manager = gui, 
    )
    slider_vel_inf_estrelas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((30, 110), (SLIDER_LARG, SLIDER_ALT)), 
    start_value = min_vel, 
    value_range = (-100, 100), 
    manager = gui,
    )
    return rot_vel_inf_estrelas, rot_slider_vel_inf_estrelas, slider_vel_inf_estrelas

def slider_velocidade_max_estrelas(max_vel,gui):
    """
    Retorna os objetos do slider da velocidade maxima das estrelas
    """
    rot_vel_sup_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((10, 130), (250, 50)),
    text = "Velocidade Máxima das Estrelas", 
    manager = gui, 
    )
    rot_slider_vel_sup_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((220, 130), (100, 50)),
    text = str(max_vel),
    manager = gui, 
    )
    slider_vel_sup_estrelas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((30, 170), (SLIDER_LARG, SLIDER_ALT)),
    start_value = max_vel,
    value_range = (-100, 100),
    manager = gui,
    )
    return rot_vel_sup_estrelas, rot_slider_vel_sup_estrelas, slider_vel_sup_estrelas

def slider_massa_min_estrelas(min_mass,gui):
    """
    Retorna os objetos do slider da massa minima das estrelas
    """
    rot_massa_inf_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((10, 190), (250, 50)), 
    text = "Massa Mínima das Estrelas", 
    manager = gui, 
    )
    rot_slider_massa_inf_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((220, 190), (100, 50)),
    text = str(min_mass), 
    manager = gui, 
    )
    slider_massa_inf_estrelas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((30, 230), (SLIDER_LARG, SLIDER_ALT)), 
    start_value = min_mass,
    value_range = (1, 1000000), 
    manager = gui,
    )
    return rot_massa_inf_estrelas, rot_slider_massa_inf_estrelas, slider_massa_inf_estrelas

def slider_massa_max_estrelas(max_mass,gui):
    """
    Retorna os objetos do slider da massa maxima das estrelas
    """
    rot_massa_sup_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((10, 250), (250, 50)), 
    text = "Massa Máxima das Estrelas", 
    manager = gui, 
    )
    rot_slider_massa_sup_estrelas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((220, 250), (100, 50)), 
    text = str(max_mass),
    manager = gui, 
    )
    slider_massa_sup_estrelas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((30, 290), (SLIDER_LARG, SLIDER_ALT)), 
    start_value = max_mass, 
    value_range = (1, 1000000),
    manager = gui,
    )
    return rot_massa_sup_estrelas, rot_slider_massa_sup_estrelas,slider_massa_sup_estrelas
def slider_quant_planetas(quant_planetas,gui):
    """
    Retorna os objetos do slider da quantidade de planetas
    """
    rot_quant_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 360, 30), (250, 30)),
    text = "Quantidade de Planetas", 
    manager = gui, 
    )
    rot_slider_quant_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 130, 30), (100, 50)), 
    text = str(quant_planetas), 
    manager = gui, 
    )
    slider_quant_planetas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((LARGURA - 320, 60), (SLIDER_LARG, SLIDER_ALT)), 
    start_value = quant_planetas, 
    value_range = (0, 1000),
    manager = gui,
    )
    return rot_quant_planetas, rot_slider_quant_planetas, slider_quant_planetas

def slider_vel_min_planetas(min_vel, gui):
    """
    Retorna os objetos do slider da velocidade minima dos planetas
    """
    rot_vel_inf_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 360, 70), (250, 50)), # Posição e tamanho do rótulo
    text = "Velocidade Mínima dos Planetas", # Exibe a velocidade mínima das planetas atualmente selecionada
    manager = gui, 
    )
    rot_slider_vel_inf_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 130, 70), (100, 50)), # Posição e tamanho do rótulo
    text = str(min_vel), # Exibe a velocidade mínima das planetas atualmente selecionada
    manager = gui, 
    )
    slider_vel_inf_planetas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((LARGURA - 320, 110), (SLIDER_LARG, SLIDER_ALT)), # Posição e tamanho do rótulo
    start_value = min_vel, # Velocidade mínima inicial padrão de planetas
    value_range = (-100, 100), # Limites do slider
    manager = gui,
    )
    return rot_vel_inf_planetas, rot_slider_vel_inf_planetas, slider_vel_inf_planetas

def slider_vel_max_planetas(max_vel,gui):
    """
    Retorna os objetos do slider da velocidade maxima dos planetas
    """
    rot_vel_sup_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 360, 130), (250, 50)), # Posição e tamanho do rótulo
    text = "Velocidade Máxima dos Planetas", # Exibe a velocidade mínima das planetas atualmente selecionada
    manager = gui, 
    )
    rot_slider_vel_sup_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 130, 130), (100, 50)), # Posição e tamanho do rótulo
    text = str(max_vel), # Exibe a velocidade mínima das planetas atualmente selecionada
    manager = gui, 
    )
    slider_vel_sup_planetas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((LARGURA - 320, 170), (SLIDER_LARG, SLIDER_ALT)), # Posição e tamanho do rótulo
    start_value = max_vel, # Velocidade mínima inicial padrão de planetas
    value_range = (-100, 100), # Limites do slider
    manager = gui,
    )
    return rot_vel_sup_planetas,rot_slider_vel_sup_planetas,slider_vel_sup_planetas
def slider_massa_min_planeta(min_massa,gui):
    """
    Retorna os objetos do slider da massa minima dos planetas
    """
    rot_massa_inf_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 360, 190), (250, 50)), # Posição e tamanho do rótulo
    text = "Massa Mínima dos Planetas", # Exibe a velocidade mínima das estrelas atualmente selecionada
    manager = gui, 
    )
    rot_slider_massa_inf_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 130, 190), (100, 50)), # Posição e tamanho do rótulo
    text = str(min_massa), # Exibe a velocidade mínima das estrelas atualmente selecionada
    manager = gui, 
    )
    slider_massa_inf_planetas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((LARGURA - 320, 230), (SLIDER_LARG, SLIDER_ALT)), # Posição e tamanho do rótulo
    start_value = min_massa, # Velocidade mínima inicial padrão de estrelas
    value_range = (1, 10), # Limites do slider
    manager = gui,
    )
    return rot_massa_inf_planetas,rot_slider_massa_inf_planetas,slider_massa_inf_planetas

def slider_massa_max_planeta(max_massa,gui):
    """
    Retorna os objetos do slider da massa maxima dos planetas
    """
    rot_massa_sup_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 360, 250), (250, 50)), # Posição e tamanho do rótulo
    text = "Massa Máxima dos Planetas", # Exibe a velocidade mínima das estrelas atualmente selecionada
    manager = gui, 
    )
    rot_slider_massa_sup_planetas = pg_gui.elements.UILabel(
    relative_rect = pg.Rect((LARGURA - 130, 250), (100, 50)), # Posição e tamanho do rótulo
    text = str(max_massa), # Exibe a velocidade mínima das estrelas atualmente selecionada
    manager = gui, 
    )
    slider_massa_sup_planetas = pg_gui.elements.UIHorizontalSlider(
    relative_rect = pg.Rect((LARGURA - 320, 290), (SLIDER_LARG, SLIDER_ALT)), # Posição e tamanho do rótulo
    start_value = max_massa, # Velocidade mínima inicial padrão de estrelas
    value_range = (1, 10), # Limites do slider
    manager = gui,
    )
    return rot_massa_sup_planetas, rot_slider_massa_sup_planetas,slider_massa_sup_planetas