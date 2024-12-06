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