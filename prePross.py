# Importa as bibliotecas necessárias
import os, sys, re

# Loop para percorrer os argumentos passados na linha de comando (sys.argv)
for Y in range(1, len(sys.argv)):

    # Obtém o diretório atual
    cwd = os.getcwd()

    # Obtém o caminho do arquivo a ser processado a partir dos argumentos da linha de comando
    path = sys.argv[Y]
    path = cwd + "\\" + path

    # Inicializa listas para armazenar linhas de texto e índices de linhas marcadas para exclusão
    texto = []
    index = []

    # Lê o conteúdo do arquivo e armazena cada linha em uma lista
    with open(path, "r") as arquivo:
        texto = arquivo.readlines()

    # Função para remover espaços em branco desnecessários em uma linha de código
    def RemoverEspaços(string):
        # ...

    # Função para expandir macros #define no código
    def ExpandirDefine(linha):
        # ...

    # Função para extrair informações de uma linha de macro #define
    def DefineMacro(linha):
        # ...

    # Função para remover comentários do código
    def removerComentarios(texto):
        # ...

    # Função para processar linhas de inclusão (#include) substituindo-as pelo conteúdo do arquivo incluído
    def include(line):
        # ...

    # Remove comentários do código
    texto = removerComentarios(texto)

    # Verifica se uma linha está marcada para exclusão
    def linha_para_excluir(linha):
        # ...

    # Lista para armazenar índices de linhas marcadas para exclusão
    indice = []

    # Loop para verificar e processar linhas marcadas para exclusão, #include e #define
    for i in range(len(texto)):
        if linha_para_excluir(texto[i]):
            continue

        # Processa linhas #include
        if texto[i].startswith("#include"):
            indice.append(i)
            
        # Processa linhas #define
        elif texto[i].startswith("#define"):
            # Verifica se a linha contém parênteses (indica uma macro com parâmetros)
            if '(' in texto[i]:
                # ...
            else:
                # ...
        else:
            # Remove espaços em branco desnecessários nas linhas de código
            texto[i] = RemoverEspaços(texto[i])

    # Processa linhas #include, substituindo-as pelo conteúdo dos arquivos incluídos
    for i in indice:
        texto[i] = include(texto[i])

    # Cria uma lista de código final excluindo linhas marcadas para exclusão
    codigo_final = []
    for i in range(len(texto)):
        if not linha_para_excluir(texto[i]):
            codigo_final.append(texto[i])

    # Atualiza a variável 'texto' com o código final
    texto = codigo_final

    # Gera um nome de arquivo para o código preprocessado
    nome_arquivo = "AqrPreProcessado" + str(Y) + ".c"

    # Escreve o código preprocessado no arquivo
    with open(nome_arquivo, "w") as arq:
        arq.write("".join(texto))
