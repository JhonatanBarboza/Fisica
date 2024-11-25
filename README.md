# Gravitação

## Descrição Básica do Projeto

Esse projeto é uma simulação das leis da gravitação entre estrelas e planetas. O propósito é aplicar na computação o que foi estudado na matéria Física Básica I. Para tanto, criamos uma simulação em Python utilizando como base a biblioteca Pygame.

Em essência, estrelas (pontos laranjas) influenciam outras estrelas e planetas (pontos azuis e verdes) de acordo com as leis da gravitação que serão discutidas mais adiante.

## Conceitos de Física e Modelo Matemático

## O problema de três corpos
O Problema de Três Corpos consiste em determinar o movimento de três corpos, dadas suas 
massas, posições e velocidades iniciais e considerando que estes corpos interagem gravitacionalmente
entre si (isto é, com uma força de atração, central e proporcional às massas e ao inverso do quadrado
da distância entre os corpos).
Este problema começou a ser estudado por Newton, em seu livro Principia e a partir de trabalhos
de Heinrich Bruns (1887) e Henri Poincaré (1890) chegou-se à conclusão que o problema não pode ser
resolvido em termos de expressões algébricas e integrais. Entretanto, o problema ainda é objeto
de pesquisa, sendo interessante determinar condições iniciais que levam a órbitas limitadas (onde um
corpo não é ejetado do sistema) e com órbitas periódicas (este tipo de trajetória é interessante, pois
estas podem vir a ser encontradas na natureza, especialmente se forem estáveis).
Exemplos de ocorrência deste problema são a interação entre uma estrela, um planeta e seu satélite
e a interação entre estrelas (sistemas com múltiplas estrelas são comuns na galáxia!)

### O problema dos três corpos restritos
O Problema de Três Corpos Restrito é uma simplificação do problema anterior introduzida por
Euler. Neste caso, consideramos um terceiro corpo de massa desprezível, isto é, ele sofre influência
gravitacional dos outros dois corpos, mas não interfere em seu movimento. Esta simplificação facilita
a resolução do problema, dado que as soluções do problema de dois corpos é conhecida ( os dois
corpos orbitam seu centro de massa em órbitas elípticas, seguindo as leis de Kepler) e ainda assim é
útil para modelar sistemas físicos, como por exemplo a interferência do Sol no movimento da Lua em
torno da Terra e o movimento de uma nave espacial entre a Terra e a Lua.

## Implementação



## Como Usar

Executar os seguintes comandos dentro do repósito ```./Fisica```:

```bash
source venv/bin/activate
pip install pygame
pip install pygame_gui
python spaceSim.py
```

## Referências
https://github.com/JhonatanBarboza/Simulacao_Universo
