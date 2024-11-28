<!-- MathJax script
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
-->
# Gravitação

## Descrição Básica do Projeto

Esse projeto é uma simulação das leis da gravitação entre estrelas e planetas. O propósito é aplicar na computação o que foi estudado na matéria Física Básica I. Para tanto, criamos uma simulação em Python utilizando como base a biblioteca Pygame.

Em essência, estrelas (pontos laranjas) influenciam outras estrelas e planetas (pontos azuis e verdes) de acordo com as leis da gravitação que serão discutidas mais adiante.

## Conceitos de Física e Modelo Matemático
### O problema de dois corpos sob a ação de uma força central
  Um sistema de dois corpos é um modelo teórico em que dois objetos interagem exclusivamente sob a influência de forças mútuas, como a gravidade. Nesse contexto, o centro de massa desempenha um papel crucial: ele é o ponto onde o momento total do sistema é conservado, e ambos os corpos orbitam ao seu redor. Em muitos casos, especialmente em sistemas isolados, assume-se que o momento angular total em relação ao centro de massa é constante. Isso significa que, se o momento angular inicial é zero, os corpos se moverão de maneira a preservar essa condição. Além disso, a energia total do sistema é a soma das energias cinética e potencial gravitacional, e sua conservação determina as possíveis trajetórias. A interação entre essas energias define se o movimento é uma órbita fechada (elipse ou círculo), aberta (parábola ou hipérbole), ou mesmo uma colisão direta. Esses princípios fornecem a base para compreender a dinâmica em sistemas gravitacionais, ajudando a prever as configurações e comportamentos possíveis.
  Inicialmente, estudaremos o movimento entre os dois corpos como partículas, pois para descrever a trajetória, a composição interna dos corpos não é relevante para o movimento, logo será estudando como o movimento de uma párticula sujeita a uma força central. Essas forças de interação, são forças centrais e conservativas.
  
  (imagem do sistema)
 
 A partir do desenho e da Lei da Gravitação Universal de Newton, obtém-se o módulo da força que 2 sofre por causa da presença de 1 ( $\vec{F_{21}}$ ), e a direção será dada por esse valor absoluto vezes a direção unitária, dada pelo vetor $|\vec{r_2} - \vec{r_1}|$ pelo seu módulo, sendo que sua direção é contrária a força, por isso sinal é negativo.

  <p>
  $$
  \begin{aligned}
  \left| \vec{F_{21}} \right| &= \frac{G m_1 m_2}{|\vec{r_2} - \vec{r_1}|^2} \\
  \vec{F_{21}} &= \frac{G m_1 m_2}{|\vec{r_2} - \vec{r_1}|^3} \left( |\vec{r_2} - \vec{r_1}| \right)
  \end{aligned}
  $$

  Tendo em vista que a força é conservativa, ela poderia ter sido obtida através da energia potencial, dada por:

  $$ 
 \begin{align}
 U(|\vec{r_2} - \vec{r_1}|) = -G\frac{m_1 m_2}{|\vec{r_2} - \vec{r_1}|}
 \end{align}
 $$
 </p>

Cabe destacar que a energia potencial depende apenas do módulo da diferença entre os vetores de posição. Isso significa que, se mudássemos a origem, os vetores de posição mudariam, mas o módulo da diferença entre eles continuaria o mesmo. Portanto, a energia potencial e a força não seriam afetadas por essa mudança de origem. Outro caso é uma possível translação do sistema para outro local, somando a $\vec{r_1}$ e $\vec{r_2}$ um vetor fixo. Nesse caso, os vetores de posição mudariam, mas a diferença entre eles permaneceria a mesma, pois a translação não afeta a distância relativa entre os corpos (sistema invariante por translação).

Coordenada relativa é definida como:
 <p>
 $$ 
 \begin{align}
 \vec{r} = \vec{r_1} - \vec{r_2} \\
  r = \left| \vec{r} \right|
\end{align}
 $$
 
Assim, como conhecemos a energia potencial associada ao problema, podemos tomar a lagrangiana associada a ele, buscando conhecer a descrição desse sistema a partir das energia cinética, $E_c$ , e potencial ( $U$ ):

$$ 
\begin{align}
 L = E_c - U = \frac{1}{2}m_1\dot{\vec{r_1}}^2 + \frac{1}{2}m_2\dot{\vec{r_2}}^2 - U(r)
\end{align}
$$
  
Além disso, usaremos o vetor posição do centro de massa dado por:

$$ 
\begin{align}
\vec{R} = \frac{\vec{r_1}m_1 + \vec{r_2}m_2}{m_1 + m_2} 
\end{align}
$$

Buscaremos simplificar essa equação, visando retirar as redundâncias e deixarmos tudo em termos de r e $\vec{R}$, para isso, chamaremos $m_1$ + $m_2$ = $M$, e juntaremos a equação da coordenada relativa com a equação do vetor posição do centro de massa, de forma a deixar os vetores $\vec{r_1}$ e $\vec{r_2}$ em função de $\vec{r}$ e $\vec{R}$. Para isso, multiplica-se a equação da coordenada relativa por \frac{m_2}{M} e somado a equação da posição do centro de massa.

$$ 
\begin{align}
\vec{r}\frac{m_2}{M} = \vec{r_1}\frac{m_2}{M} - \vec{r_2}\frac{m_2}{M} \\
\vec{R} = \frac{\vec{r_1}m_1}{M} + \frac{\vec{r_2}m_2}{M} \\
\vec{r}\frac{m_2}{M} + \vec{R} = \vec{r_1}\frac{m_2}{M} + \frac{\vec{r_1}m_1}{M} \\
\vec{r_1} = \vec{r}\frac{m_2}{M} + \vec{R}
\end{align}
$$

Analogamente poderemos manipular as equações para obter $r_2$, que será dado por:

$$ 
\begin{align}
\vec{r_2} = \vec{R} - \vec{r}\frac{m_1}{M} 
\end{align}
$$

Para substituir na equação é necessário calcular $\dot{\vec{r_1}}$ e $\dot{\vec{r_2}}$:

$$ 
\begin{align}
\vec{r_1} = \vec{r}\frac{m_2}{M} + \vec{R} \to \dot{\vec{r_1}} = \dot{\vec{r}}\frac{m_2}{M} + \dot{\vec{R}} \\ 
\vec{r_2} = \vec{R} - \vec{r}\frac{m_1}{M} \to \dot{\vec{r_2}} = \dot{\vec{R}} - \dot{\vec{r}}\frac{m_1}{M} 
\end{align}
$$

Substituindo na equação da lagrangiana

$$ 
\begin{align}
L = \frac{1}{2} m_1 \left( \dot{\vec{r}} + \frac{m_2}{M} \dot{\vec{R}} \right)^2 + \frac{1}{2} m_2 \left( \dot{\vec{R}} - \frac{m_1}{M} \dot{\vec{r}} \right)^2 - U(r)
\end{align}
$$

Após feito os cálculos, ficaremos com

$$ 
\begin{align}
L = \frac{1}{2} M \dot{\vec{R}}^2 + \frac{1}{2} \frac{m_1 + m_2}{M} \dot{\vec{r}}^2 - U(r)
\end{align}
$$

Com esse resultado, obtemos que a trajetória depende apenas da coordenada do centro de masssa e da coordenada da posição relativa. No entanto, aparece um objeto novo, $\frac{m_1 + m_2}{M}$, com dimensão de massa. Tal resultado é esperado, tendo em vista que esse termo deve ter relação com o termo ligado ao $\dot{\vec{R}}$, pois são termos de dimensão de energia cinética( massa vezes o quadrado da velocidade ). Esse objeto ganha o nome de massa reduzida de um sistema de dois corpos definido por $\mu = \frac{m_1 m_2}{m_1 + m_2}$. Uma forma mnemônico dessa expressão é dada por  $\frac{1}{\mu} = \frac{1}{m_1} + \frac{1}{m_2}$. A massa reduzida tem um papel muito importante para o estudo das órbitas, pois em casos como Sol e Terra, onde um corpo possui uma massa muito grande em relação ao outro, uma das frações tendem a um número muito pequeno em relação ao outro, podendo assim, ser descartado. Portanto adotamos a lagrangiana como:

$$ 
\begin{align}
L = \frac{1}{2} M \dot{\vec{R}}^2 + \frac{1}{2} \mu \dot{\vec{r}}^2 - U(r)
\end{align}
$$

Tendo em vista que a equação não depende de $\vec{R}$, apenas depende de \dot{\vec{R}}, portanto, essa coordenada é cíclica( ignorável ), tendo uma lei de conservação associada a essa coordenda sobre o momento total do sistema, logo o momento total do sistema é conservado. Outra conclusão é que podemos imaginar essa equação como compostas por duas partes, uma dependente da coordenada $\dot{\vec{R}}$ e a outra só dependendo de $\vec{r}$ e $\dot{\vec{r}}$, ou seja, mostra-nos que temos dois problemas separáveis, distintos e independentes. Bom, como a R é coordenada ignorável, significa que $M\ddot{\vec{R}} = 0$ e isso está associado ao fato de um sistema isolado, que só depende de forças externas e como não há forças externas, logo, seu momento associado ao centro de massa é constante, por consequência, $M\dot{\vec{R}} = constante$ ( momento total do sistema ), velocidade do centro de massa é uma constante do movimento, ou seja, centro de massa executa um movimento uniforme.
 Analisando, a equação de movimento para coordenada relativa. Toma-se a derivada de L em relação a posição, denotada por $q_i$, e como é um vetor, significa tomar o seu gradiente dessa função escalar, e menos resultado, obtém-se a força.

$$ 
\begin{align}
\frac{\partial L}{\partial q_i} = \frac{d}{dt} \left( \frac{\partial L}{\partial \dot{q}_i} \right) \\
\frac{\partial L}{\partial \vec{r}} = \frac{d}{dt} \left( \frac{\partial L}{\partial \dot{\vec{r}}} \right)\\
\- \nabla U(r) = \mu \ddot{\vec{r}}
\end{align}
$$

Essa equação é uma forma de visualizar a segunda lei de newton, com a força que age sobre uma partícula fictícia e é igualada a massa dessa particula vezes sua aceleração. Tais conclusões e resoluções sobre objetos inexistentes servem para que quando obtivermos as soluções para R e r, podermos obter $r_1$ e $r_2$, e para alguns casos, isso não importa, pois vendo o caso Terra e Sol, o centro de massa ficara dentro do sol, de forma que o movimento que buscamos, a órbita da Terra, é descrita aproxidamente pelo r, tendo em vista que o sol vai ter um movimento mínimo, podendo ser ignorado. Portanto, adotaremos um referencial com origem no centro de massa do sistema. Como o centro de massa se move com velocidade constante em relação a um referencial inercial (na ausência de forças externas), esse novo referencial também será inercial. Dessa forma, com o referencial no centro de massa, ignorando o movimento do centro de massa, e quando ele coincide com a partícula mais massiva, o problema foi reduzido a um problema de apenas uma partícula, assim usaremos ferramentas de problemas unidimensionais.

(imagem novo sistema com centro de massa como origem)

Nesse novo referencial, o momento total é zero, assim dado um movimento em $m_1$, $m_2$ terá movimento na mesma direção, porém em sentido contrário com velocidade menor, dado um $m_2$ > $m_1$. Reescrevendo as coordenadas na nova origem(sendo \vec{R} = \vec{0}), temos:

$$
\begin{align}
\vec{r_1} = \vec{r}\frac{m_2}{M} \\
\vec{r_2} = \- \vec{r}\frac{m_1}{M} 
\end{align}
$$

Lembrando que o sistema é isolado, então o momento angular total será conservado, pois não há forças externas e o torque externo é 0. Escrevendo o momento angular($\vec{L}$):

$$
\begin{align}
\vec{L} = \vec{r_1} \times \vec{p_1} + \vec{r_2} \times \vec{p_2} \\
\vec{L} = m_1\vec{r_1} \times \dot{\vec{r_1}} + m_2\vec{r_2} \times \dot{\vec{r_2}}
\end{align}
$$

Calculando para o centro de massa e deixando a equação em termos de r:

$$
\begin{align}
\vec{L} = m_1\left(\frac{m_2}{M} \right)^2 \times \dot{\vec{r}} + m_2\left(\frac{m_1}{M} \right)^2 \times \dot{\vec{r}} \\
\vec{L} = \frac{m_1 m_2}{M} \vec{r} \times \dot{\vec{r}} = \vec{r} \times \mu \dot{\vec{r}}
\end{align}
$$

Tal resultado remete ao momento angular de uma partícula, que é o produto do vetor posição pelo vetor momento associado a ele, sendo a massa pela derivada do vetor posição, sendo a massa representada pela massa reduzida. Bom, como o momento angular total é uma quantidade conservada, a direção do momento angular é fixa, assim, o movimento dessa partícula ficticia se da em uma plano que é perpendicular a esse momento angular, assim, como a coordenada relativa está associada a essa partícula, isso significa que vetor vai trafegar em um plano perpendicular ao momento angular. Logo, a primeira consequência da Lei da Gravitação Universal é que o movimento planetário é um movimento plano, assim, só é preciso duas coordenadas escalares para determinar o vetor coordenada relativa, que será medida a partir de um centro de massa, que para o sistema planetária, irá estar associada a distância do planeta ao Sol. Dessa forma, serão adotadas coordenadas polares bidimensionais. Portanto, iremos, inicialmente, escrever os termos da energia cinética nesse novo sistema de coordenadas dado por:

$$
\begin{align}
\hat{r} = \cos\phi \, \hat{i} + \sin\phi \, \hat{j}, \quad \\
\hat{\phi} = -\sin\phi \, \hat{i} + \cos\phi \, \hat{j}.
\end{align}
$$
 Assim, substituindo os termos teremos:
$$
\begin{align}
\vec{r} = r\hat{r} \\
\dot{\vec{r}} = \dot{r}\hat{r} + r\dot{\hat{r}} = \dot{r}\hat{r} + r\dot{\phi}\hat{\phi} \\
\dot{\vec{r}}^2 = \dot{r}^2 + r^2{\dot{\phi}}^2 \\
L_{rel} = \frac{1}{2} \mu \left(\dot{r}^2 + r^2{\dot{\phi}}^2 \right) - U(r) \\
\end{align}
$$

Analisando o resultado da equação, temos que ela não depende de $\phi$, sendo uma coordenada ignorável, e dessa forma, temos uma lei de conservação. Então analisando esse fato, que está associado a:

$$ 
\begin{align}
\frac{\partial L}{\partial q_i} = \frac{d}{dt} \left( \frac{\partial L}{\partial \dot{q}_i} \right) \\
\frac{\partial L}{\partial \dot{\phi}} = \mu r^2 \dot{\phi} = constante = l \\
\dot{\phi} = \frac{l}{\mu r^2}
\end{align}
$$

Sendo que nesse caso, que está assumindo papel de $q_i$ é o $\phi$, e não tem dependencia em $\phi$, logo a derivada do lado esquerdo é zero, logo a quantidade da direita da equação é uma quantidade conservada. Tal expressão possui dimensão de momento angular, tendo em vista o produto do momento de inércia de $\mu r^2$ pela velocidade angular $\dot{\phi}$, dando o momento angular da partícula ficticia que é conservado. Dessa forma, isola-se a velocidade angular, obtém-se que quanto maior a distancia, menor é a velocidade angular. Agora, vamos obter a equação para a coordenada radial, achando a força generalizada e a taxa de variação temporal do momento generalizado, igualando-as, note que $\phi$ aparecerá na equação mas usaremos a relação encontrada anteriormente.

$$ 
\begin{align}
\frac{\partial L}{\partial r} = \mu r \dot{\phi}^2 - \frac{\partial U}{\partial r} \\
\frac{\partial L}{\partial \dot{r}} = \mu \dot{r} \\
\dot{\phi} = \frac{l}{\mu r^2} \\
\mu r \dot{\frac{l^2}{\mu^2 r^4}} - \frac{\partial U}{\partial r} = \mu \ddot{r} \\
\dot{\frac{l^2}{\mu r^3}} - \frac{\partial U}{\partial r} = \mu \ddot{r}
\end{align}
$$

Temos como resposta "algo" junto a força generalizada, e do outro lado a massa vezes a aceleração. Esse "algo" é chamado de força centrífuga, pois é um termo sempre positivo, causando um aumento do r que o faz fugir do centro, vale ressaltar que é uma força ficticia, pois estamos trabalhando com uma partícula ficticia, por conta disso, podemos escrever uma energia potencial associada a essa força, assim se integrarmos a expressão obtida e fizermos uma relação com a energia potencial, teremos:

$$ 
\begin{align}
U_{cf} = \displaystyle\int \frac{l^2}{\mu r^3} = \frac{l^2}{2\mu r^2} \\
U_{total} = U + U_{cf} = U(r) = \frac{l^2}{2\mu r^2}
\end{align}
$$

Dessa forma, possuímos um problema de dois corpos sujeitos a uma força central, travestido ao problema de uma partícula em uma dimensão, com massa reduzida(ficticia), e essa dimensão única é uma quantidade escalar que é a distância entre as duas partículas que compunham o problema original, e dessa forma, pode-se utiklizar ferramentas de método unidimensionais.




</p>

 

 

 

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
