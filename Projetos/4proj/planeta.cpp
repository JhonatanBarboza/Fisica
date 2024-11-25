#include <GL/glut.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define G 6.67430  // Constante gravitacional (NÃO MEXER)
#define NUM_ESTRELAS 1
#define NUM_PLANETAS 10000
#define bordas 100000
#define mb 10                           // Mutiplica as bordas
#define almentar_raio 15                // Este valor é multiplicado ao raio (deixar os corpos visiveis em grandes escalas)
#define circulo_quadrado_estrela true  // Desenha as estrelas como um true circulo ou false quadrado
#define circulo_quadrado_planeta true  // Desenha os planetas como true circulo ou false quadrado
#define colisao_estrelas true          // Ativa acolisão das estrelas (true ativado, false desativado) 
#define colisao_planetas false         // Ativa acolisão das estrelas (true ativado, false desativado)

// Estrutura para armazenar as propriedades de cada planeta
typedef struct Estrela_ {
    float x, y;           // Posição do planeta
    float vx, vy;         // Velocidade do planeta
    double massa;          // Massa do planeta
    double raio;           // Raio do planeta
    int ativo;            // Planeta ativo ou não
} Estrela;

// Estrutura para armazenar as propriedades de cada planeta
typedef struct Planeta_{
    float x, y;           // Posição do planeta
    float vx, vy;         // Velocidade do planeta
    double massa;          // Massa do planeta
    double raio;           // Raio do planeta
    int ativo;            // Planeta ativo ou não
} Planeta;

Estrela estrelas [NUM_ESTRELAS];
Planeta planetas [NUM_PLANETAS];

// Função para gerar um valor detro de um limite determinado (controlar o intervalo em que os planetas podem ser gerados)
float gerar_valor_com_limite() {
    float valor;
    int intervalo = 100000;//(bordas /10) * 2;  // Limite de exclusão ao redor do centro
    do {
        valor = (rand() % (int)(bordas*2 + 1));
    } while (valor >= -intervalo && valor <= intervalo);  // Excluir o intervalo ex:[-200, 200]

    return valor;
}

// Função para inicializar os planetas com posições, velocidades e massas
void inicializar_estrelas() {
    for (int i = 0; i < NUM_ESTRELAS; i++) {
        estrelas[i].massa = 100000000;//(rand()%1000000 + 1)+1000;  // Massa do planeta (não pode ser zero)
        estrelas[i].raio = pow(estrelas[i].massa, 1.0f / 3.0f);  // Raio inicial do planeta
        estrelas[i].x = 0;//rand()%(bordas*2*mb+1)-(bordas*mb);  // Posição no eixo X
        estrelas[i].y = 0;//rand()%(bordas*2*mb+1)-(bordas*mb);  // Posição no eixo Y
        estrelas[i].vx = 0;//(rand() % 500) - 250;  // Velocidade inicial em X
        estrelas[i].vy = 0;//(rand() % 500) - 250;  // Velocidade inicial em Y
        estrelas[i].ativo = 1;  // Planeta começa ativo
    }
}

// Função para inicializar os planetas com posições, velocidades e massas
void inicializar_planetas() {
    for (int i = 0; i < NUM_PLANETAS; i++) {
        planetas[i].massa = rand() % 1000 + 1;  // Massa do planeta (não pode ser zero)
        planetas[i].raio = 100;//pow(planetas[i].massa, 1.0f / 3.0f); // Raio inicial do planeta
        planetas[i].x = gerar_valor_com_limite();  // Posição no eixo X
        planetas[i].y = gerar_valor_com_limite();  // Posição no eixo Y
        planetas[i].vx = -750;//(rand() % 20) - 10;  // Velocidade inicial em X
        planetas[i].vy = 250;//(rand() % 20) - 10; // Velocidade inicial em Y
        planetas[i].ativo = 1;  // Planeta começa ativo
    }
}

// Função para verificar colisões entre planetas
void verificar_colisoes_planetas() {
    for (int i = 0; i < NUM_PLANETAS; i++) {
        if (!planetas[i].ativo) continue;

        for (int j = i + 1; j < NUM_PLANETAS; j++) {
            if (!planetas[j].ativo) continue;

            // Calcular a distância entre os dois planetas
            float dx = planetas[j].x - planetas[i].x;
            float dy = planetas[j].y - planetas[i].y;
            float distancia = sqrt(dx * dx + dy * dy);

            // Verificar se há colisão (distância menor que a soma dos raios)
            if (distancia <= (planetas[i].raio*almentar_raio + planetas[j].raio*almentar_raio)) {
                // Colisão detectada, combinar os dois planetas
                if (planetas[i].massa >= planetas[j].massa) {
                    // Planeta i absorve o planeta j
                    float massa_total = planetas[i].massa + planetas[j].massa;

                    // Conservação do momento para calcular a nova velocidade
                    planetas[i].vx = (planetas[i].massa * planetas[i].vx + planetas[j].massa * planetas[j].vx) / massa_total;
                    planetas[i].vy = (planetas[i].massa * planetas[i].vy + planetas[j].massa * planetas[j].vy) / massa_total;

                    planetas[i].massa = massa_total;

                    // Atualizar o raio com base na nova massa (aproximadamente)
                    planetas[i].raio = pow(massa_total, 1.0f / 3.0f);

                    planetas[j].ativo = 0;  // Planeta j deixa de existir
                } else {
                    // Planeta j absorve o planeta i
                    float massa_total = planetas[i].massa + planetas[j].massa;

                    planetas[j].vx = (planetas[i].massa * planetas[i].vx + planetas[j].massa * planetas[j].vx) / massa_total;
                    planetas[j].vy = (planetas[i].massa * planetas[i].vy + planetas[j].massa * planetas[j].vy) / massa_total;

                    planetas[j].massa = massa_total;
                    planetas[j].raio = pow(massa_total, 1.0f / 3.0f);  // Atualizar o raio

                    planetas[i].ativo = 0;  // Planeta i deixa de existir
                }
            }
        }
    }
}

// Função para verificar colisões entre estrelas
void verificar_colisoes_estrelas() {
    for (int i = 0; i < NUM_ESTRELAS; i++) {
        if (!estrelas[i].ativo) continue;

        for (int j = i + 1; j < NUM_ESTRELAS; j++) {
            if (!estrelas[j].ativo) continue;

            // Calcular a distância entre as duas estrelas
            float dx = estrelas[j].x - estrelas[i].x;
            float dy = estrelas[j].y - estrelas[i].y;
            float distancia = sqrt(dx * dx + dy * dy);

            // Verificar se há colisão (distância menor que a soma dos raios)
            if (distancia <= (estrelas[i].raio*almentar_raio + estrelas[j].raio*almentar_raio)) {
                // Colisão detectada, combinar as duas estrelas
                if (estrelas[i].massa >= estrelas[j].massa) {
                    // Estrela i absorve a estrela j
                    float massa_total = estrelas[i].massa + estrelas[j].massa;

                    // Conservação do momento para calcular a nova velocidade
                    estrelas[i].vx = (estrelas[i].massa * estrelas[i].vx + estrelas[j].massa * estrelas[j].vx) / massa_total;
                    estrelas[i].vy = (estrelas[i].massa * estrelas[i].vy + estrelas[j].massa * estrelas[j].vy) / massa_total;

                    estrelas[i].massa = massa_total;

                    // Atualizar o raio com base na nova massa (aproximadamente)
                    estrelas[i].raio = pow(massa_total, 1.0f / 3.0f);

                    estrelas[j].ativo = 0;  // Estrela j deixa de existir
                } else {
                    // Estrela j absorve a estrela i
                    float massa_total = estrelas[i].massa + estrelas[j].massa;

                    estrelas[j].vx = (estrelas[i].massa * estrelas[i].vx + estrelas[j].massa * estrelas[j].vx) / massa_total;
                    estrelas[j].vy = (estrelas[i].massa * estrelas[i].vy + estrelas[j].massa * estrelas[j].vy) / massa_total;

                    estrelas[j].massa = massa_total;
                    estrelas[j].raio = pow(massa_total, 1.0f / 3.0f);  // Atualizar o raio

                    estrelas[i].ativo = 0;  // Estrela i deixa de existir
                }
            }
        }
    }
}

float distancia(float x1, float y1, float x2, float y2) {
    return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
}

// Função para calcular a força gravitacional entre duas estrelas
void calcular_gravidade_estrela(Estrela* a, Estrela* b) {
    float dx = b->x - a->x;  // Distância no eixo X entre estrela a e estrela b
    float dy = b->y - a->y;  // Distância no eixo Y entre estrela a e estrela b
    float distancia = sqrt(dx * dx + dy * dy);

    if (distancia > 0.01f) {  // Evitar divisão por zero
        // Força gravitacional
        float forca = G * a->massa * b->massa / (distancia * distancia);

        // Aceleração no eixo X e Y para a (direção oposta à estrela b)
        float ax_a = forca * dx / distancia / a->massa;
        float ay_a = forca * dy / distancia / a->massa;

        // Aceleração no eixo X e Y para b (direção oposta à estrela a)
        float ax_b = -forca * dx / distancia / b->massa;
        float ay_b = -forca * dy / distancia / b->massa;

        // Atualizar as velocidades das estrelas
        a->vx += ax_a;
        a->vy += ay_a;

        b->vx += ax_b;
        b->vy += ay_b;
    }
}

// Função para atualizar a posição das estrelas
void atualizar_estrelas() {
    for (int i = 0; i < NUM_ESTRELAS; i++) {
        if (estrelas[i].x > bordas*2*mb && estrelas[i].y > bordas*2*mb){
            estrelas[i].ativo = 0;
        }
        if (!estrelas[i].ativo) continue;

        // Calcular a interação gravitacional com as outras estrelas
        for (int j = i + 1; j < NUM_ESTRELAS; j++) {
            if (estrelas[j].ativo) {
                calcular_gravidade_estrela(&estrelas[i], &estrelas[j]);
            }
        }

        // Atualizar a posição das estrelas com base na velocidade
        estrelas[i].x += estrelas[i].vx;
        estrelas[i].y += estrelas[i].vy;
    }
    if (colisao_estrelas == 1){
        verificar_colisoes_estrelas();
    }
}


void atualizar_planetas() {
    for (int i = 0; i < NUM_PLANETAS; i++) {
        if (planetas[i].x > bordas*2*mb && planetas[i].y > bordas*2*mb){
            planetas[i].ativo = 0;
        }
        if (!planetas[i].ativo) continue;

        float ax = 0, ay = 0;  // Acelerações resultantes

        // Força gravitacional das duas estrelas
        for (int j = 0; j < NUM_ESTRELAS; j++) {
            if (!estrelas[j].ativo) continue;

            float dx = estrelas[j].x - planetas[i].x;
            float dy = estrelas[j].y - planetas[i].y;
            float distancia = sqrt(dx * dx + dy * dy);

            if (distancia > 0.01f) {  // Evitar divisão por zero
                float forca = G * (estrelas[j].massa * planetas[i].massa) / (distancia * distancia);

                // Aceleração causada pela estrela j
                ax += forca * dx / distancia;
                ay += forca * dy / distancia;
            }
        }

        // Atualizar velocidade com a aceleração calculada
        planetas[i].vx += ax;
        planetas[i].vy += ay;

        // Atualizar posição dos planetas
        planetas[i].x += planetas[i].vx;
        planetas[i].y += planetas[i].vy;
    }
    if (colisao_planetas){
        verificar_colisoes_planetas();
    }
}

// Função para desenhar um círculo (estrela/planetas)
void desenhar_circulo(float cx, float cy, float raio) {
    glBegin(GL_POLYGON);
    for (int i = 0; i < 100; i++) {
        float theta = 2.0f * M_PI * i / 100;
        float x = raio * cosf(theta);
        float y = raio * sinf(theta);
        glVertex2f(cx + x, cy + y);
    }
    glEnd();
}

// Função para desenhar um quadrado
void desenhar_quadrado(float cx, float cy, float tamanho) {
    glBegin(GL_POLYGON);
        glVertex2f(cx - tamanho, cy - tamanho); // canto inferior esquerdo
        glVertex2f(cx + tamanho, cy - tamanho); // canto inferior direito
        glVertex2f(cx + tamanho, cy + tamanho); // canto superior direito
        glVertex2f(cx - tamanho, cy + tamanho); // canto superior esquerdo
    glEnd();
}

// Desenho na tela
void exibir() {
    glClear(GL_COLOR_BUFFER_BIT);

    // Desenhar estrelas
    for (int i = 0; i < NUM_ESTRELAS; i++) {
        if (estrelas[i].ativo) {
            glColor3f(1.0f, 1.0f, 0.0f);  // cor das estrelas
            if (circulo_quadrado_estrela == 1){
                desenhar_circulo(estrelas[i].x, estrelas[i].y, estrelas[i].raio*almentar_raio);
            }
            else if(circulo_quadrado_estrela == 0){
                desenhar_quadrado(estrelas[i].x, estrelas[i].y, estrelas[i].raio*almentar_raio);
            }
        }
    }

    // Desenhar os planetas
    for (int i = 0; i < NUM_PLANETAS; i++) {
        if (planetas[i].ativo) {
            glColor3f(1.0f, 1.0f, 1.0f);  // Cor dos planetas
            if (circulo_quadrado_planeta == 1){
                desenhar_circulo(planetas[i].x, planetas[i].y, (planetas[i].raio*almentar_raio)/2);
            }
            else if(circulo_quadrado_planeta == 0){
                desenhar_quadrado(planetas[i].x, planetas[i].y, (planetas[i].raio*almentar_raio)/2);
            }
        }
    }

    glutSwapBuffers();
}

// Função Timer para atualização
void timer(int valor) {
    atualizar_estrelas();
    atualizar_planetas();
    glutPostRedisplay();
    glutTimerFunc(1000 / 60, timer, 0);  // 60 FPS
}

// Configurações do OpenGL
void inicializarOpenGL() {
    glClearColor(0.0, 0.0, 0.0, 1.0);  // Fundo preto
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-bordas*mb, bordas*mb, -bordas*mb, bordas*mb);  // Ambiente 2D
}

// Função principal
int main(int argc, char** argv) {
    srand(time(0));  // Inicializar o gerador de números aleatórios

    // Inicializar GLUT
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(900, 900);
    glutCreateWindow("Simulacao de orbita com Gravidade");

    // Inicializar planetas e OpenGL
    inicializar_estrelas();
    inicializar_planetas();
    inicializarOpenGL();

    // Registrar callbacks
    glutDisplayFunc(exibir);
    glutTimerFunc(0, timer, 0);

    // Iniciar loop principal
    glutMainLoop();
    return 0;
}
