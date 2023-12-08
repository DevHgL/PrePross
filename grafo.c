#include <stdio.h>

// Definindo o número de vértices do grafo
#define VERTICES 5

// Função para criar um grafo completo
void criarGrafoCompleto(int grafo[VERTICES][VERTICES]) {
    for (int i = 0; i < VERTICES; i++) {
        for (int j = 0; j < VERTICES; j++) {
            if (i != j) {
                grafo[i][j] = 1;  // Atribuir 1 para arestas entre diferentes vértices (grafo completo)
            } else {
                grafo[i][j] = 0;  // Atribuir 0 para a diagonal principal (sem laços)
            }
        }
    }
}

// Função para exibir o grafo
void exibirGrafo(int grafo[VERTICES][VERTICES]) {
    for (int i = 0; i < VERTICES; i++) {
        for (int j = 0; j < VERTICES; j++) {
            printf("%d ", grafo[i][j]);
        }
        printf("\n");
    }
}

int main() {
    // Declarar uma matriz para representar o grafo
    int grafo[VERTICES][VERTICES];

    // Criar um grafo completo
    criarGrafoCompleto(grafo);

    // Exibir o grafo
    printf("Grafo Completo:\n");
    exibirGrafo(grafo);

    return 0;
}
