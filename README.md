# Gravitação

## Descrição Básica do Projeto
O projeto é uma simulação de interações gravitacionais entre planetas e estrelas no espaço. O propósito é aplicar conceitos da Física para resolver um problema real e verificar esse resultado, usando computação.
### Problema dos $2$ Corpos
Dado dois corpos celestes, interagindo entre si pelas leis da gravitação, como podemos saber a trajetória desses corpos?

A solução mais intuitiva é aquela estudada no curso, em que obtemos explicitamente as equações das trajetórias de ambos os corpos (ver README na pasta ```./Exemplos``` para mais detalhes nessa solução). Esta é uma solução **analítica**, ou seja, com essas equações conseguimos prever completamente os movimentos no sistema.
### Problema dos $3$ e $N$ Corpos
Mas o que acontece se adicionarmos um terceiro corpo a esse sistema?

Caso a massa desse terceiro corpo seja muito pequena em relação aos outros dois, ainda podemos aproximá-lo a um problema de $2$ corpos (*problema de $3$ corpos restrito*). No entanto, caso a massa desses $3$ corpos seja similar, ao tentarmos obter as equações das trajetórias de cada corpo, teremos mais variáveis desconhecidas que equações descrevendo essas variáveis isoladamente.

Em outras palavras, teremos um sistema impossível de equações! Mesmo utilizando o conceito de *centro de massa*, que reduz a quantidade de variáveis desconhecidas, ainda não conseguimos obter uma solução geral para o sistema.

Esse é o problema de $3$ (e, consequentemente) de $N$ corpos. Não conseguimos obter (salvo algumas exceções, em que as condições iniciais permitem que as equações sejam resolvidas, como os casos *Euler* e *Lagrange*) as equações das trajetórias dos corpos. Então como saber o comportamento dos corpos nesse sistema?

A solução é aproximar e resolver as equações **numericamente**, calculando iterativamente as velocidades e posições de cada corpo conforme eles interagem entre si em pequenos intervalos de tempo. Há múltiplos métodos de simular esse sistema, e o utilizado pos nós foi o mais simples, o **método de Euler**.

## Conceitos de Física e Modelo Matemático
Colocaremos como origem do nosso sistema de coordendas ortonormal um ponto que não é nenhuma das massas. Temos assim um referencial inercial. Seja também o nosso sistema de coordenadas ortonormal dado pelos versores $(\hat{i}, \hat{j})$ ao longo dos eixos $(x, y)$, respectivamente.

### Gravitação
Segundo a Lei da Gravitação Universal, a força gravitacional $\vec{F_g}$ entre duas massas $m_1$ e $m_2$, a uma distância $r$ uma da outra é

$$ \begin{align} \vec{F_g} = - \frac{G m_1 m_2}{r^2} \hat{r}, \end{align} $$

onde $G$ é a constante gravitacional. O versor $\hat{r}$ é o vetor unitário que aponta de uma massa para outra:
$$ \begin{align} \hat{r} = \frac{ \vec{r_2} - \vec{r_1} }{\left\| \vec{r_2} - \vec{r_1} \right\|}, \end{align} $$

sendo $r = \left\| \vec{r_2} - \vec{r_1} \right\|$.

Note que $\vec{r_2} = \vec{r_2} (t)$ e $\vec{r_1} = \vec{r_1} (t)$ indicam os vetores posição das massas $2$ e $1$ (respectivamente) no instante $t$ em relação a uma origem.

![Coordenadas](./Imagens/Coord.png)

### Leis de Newton
A segunda lei de Newton descreve que a força atuando sobre um corpo $i$ é dada por:

$$ \begin{align} \vec{F_i}(t) &= m_i \vec{a_i}(t). \end{align} $$

Como a única força atuante no sistema é a gravitacional, temos:

$$ \begin{align} \vec{a_i}(t) &= \dot{\vec{v_i}}(t), \\ \vec{v_i}(t) &= \dot{\vec{r_i}}(t), \\ \ddot{\vec{r_i}}(t) &= \frac{\vec{F_g}}{m_i}. \end{align} $$

Como discutido anteriormente, é díficil obter a equação explícita de $x(t)$ e $y(t)$ em $\vec{r}(t) = x(t) \hat{i} + y(t) \hat{j}$ com a EDO obtida. Utilizamos, então, o Método de Euler.

### Método de Euler
1. Para cada corpo $i$, somamos as forças gravitacionais exercidas por todos os outros corpos ($j$):

$$ \begin{align} \vec{F_i} &= - G \sum_{j \neq i} \frac{m_i m_j}{r_{ij}^2} \hat{r_{ij}}. \end{align} $$

2. Calculamos a aceleração do corpo $i$ pela segunda lei de Newton:

$$ \begin{align} \vec{a_i}(t) &= \frac{\vec{F_i}}{m_i}. \end{align} $$

3. Atualizamos a velocidade e a posição do corpo $i$:

$$ \begin{align} \vec{v_i}(t + \Delta t) &= \vec{a_i}(t) \Delta t + \vec{v_i}(t), \\ \vec{r_i}(t + \Delta t) &= \vec{v_i}(t) \Delta t + \vec{r_i}(t). \end{align} $$

## Implementação


## Como Usar


## Referências