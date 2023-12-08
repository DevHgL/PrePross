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
        # Remove espaços extras, trata parênteses e mantém espaços em branco entre aspas
        string_processada = ""
        palavras = string.replace(';','; ').replace('(', '( ').replace("{", "{ ").split()
        aspas = False

        for i, palavra in enumerate(palavras):
            if palavra.startswith('"') and len(palavra) > 1:
                aspas = True

            if aspas:
                string_processada += palavra + " "
            else:
                if i > 0 and palavras[i-1] in ["int", "float", "char", "return", "void", "unsigned", "double", "long", "short", "void"]:
                    string_processada += " "
                string_processada += palavra

            if palavra.endswith('"'):
                aspas = False

        return string_processada.strip()

    # Função para expandir macros #define no código
    def ExpandirDefine(linha):
        # Divide a linha em partes, extrai a variável e os parâmetros
        aux = linha.split()
        variavel = aux[1]
        parametros = ', '.join(aux[2:]).replace('(', '').replace(')', '')  # Obtém os parâmetros sem parênteses
        valor = f'({parametros})'  # Formata os parâmetros entre parênteses

        return variavel, valor

    # Função para extrair informações de uma linha de macro #define
    def DefineMacro(linha):
        # Usa expressões regulares para dividir a linha em partes
        partes = re.findall(r'\w+|\([^()]*\)|\S+', linha)
        partes_sem_parenteses = [parte.strip('()') for parte in partes]
        nome_macro = partes_sem_parenteses[1]
        parametros = partes_sem_parenteses[2].strip(',').replace(',', '')
        parametros = parametros.split()

        operadores = ['+', '-', '*', '/', '=']

        indice_operador = next((indice for indice, parte in enumerate(partes_sem_parenteses) if parte in operadores), None)

        operador_define = partes_sem_parenteses[indice_operador] if indice_operador is not None else ""

        return nome_macro, operador_define

    # Função para remover comentários do código
    def removerComentarios(texto):
        # Inicializa variáveis
        codigo_sem_comentarios = []
        comentario_aberto = False

        # Loop para processar cada linha do código
        for linha in texto:
            linha_sem_comentarios = ""

            i = 0
            while i < len(linha):
                # Verifica comentários de linha
                if not comentario_aberto and linha[i:i + 2] == "//":
                    break
                # Verifica comentários de bloco
                elif not comentario_aberto and linha[i:i + 2] == "/*":
                    comentario_aberto = True
                    i += 2
                    continue
                elif comentario_aberto and linha[i:i + 2] == "*/":
                    comentario_aberto = False
                    i += 2
                    continue
                elif not comentario_aberto:
                    linha_sem_comentarios += linha[i]
                i += 1

            # Adiciona a linha ao código sem comentários, se não estiver vazia
            if not comentario_aberto and linha_sem_comentarios.strip() != "":
                codigo_sem_comentarios.append(linha_sem_comentarios)

        return codigo_sem_comentarios

    # Função para processar linhas de inclusão (#include) substituindo-as pelo conteúdo do arquivo incluído
    def include(line):
        # Lista para armazenar nomes de arquivos já incluídos
        included_files = []
        # Caminho padrão para os arquivos de inclusão
        path = r"C:\MinGW\include" # Detalhe importante: Esse endereço é do Mingw do notebook.
        line_divided = line.split()

        # Verifica se a linha é um comando de inclusão (#include)
        if line_divided and len(line_divided) >= 2 and line_divided[0] == '#include':
            file_name = line_divided[1].strip('"<>')
            path += '\\' + file_name

            # Verifica se o arquivo já foi incluído
            if file_name not in included_files:
                included_files.append(file_name)

                # Lê o conteúdo do arquivo incluído
                with open(path, "r") as file:
                    file_lines = file.readlines()

                # Combina as linhas do arquivo incluído em uma string
                included_content = ''.join(file_lines)
                return included_content

        # Retorna a linha original se não for um comando de inclusão
        return line

    # Remove comentários do código
    texto = removerComentarios(texto)

    # Verifica se uma linha está marcada para exclusão
    def linha_para_excluir(linha):
        for i in index:
            if linha.startswith(texto[i]):
                return True
        return False

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
                index.append(i)
                auxiliar = DefineMacro(texto[i])
                nome_macro = auxiliar[0]
                operador_define = auxiliar[1]

                # Loop para encontrar chamadas da macro no código e substituí-las
                for j in range(len(texto)):
                    if nome_macro in texto[j]:
                        pattern = re.compile(rf'{nome_macro}\((.*?)\)', re.DOTALL)
                        match = pattern.search(texto[j])
                        if match:
                            parametros_str = match.group(1)
                            novo_parametros_str = parametros_str.replace(',', f' {operador_define} ')
                            texto[j] = pattern.sub(f'{nome_macro}({novo_parametros_str})', texto[j])
                            texto[j] = texto[j].replace(nome_macro, '')

            else:
                aux = ExpandirDefine(texto[i])
                index.append(i)

                # Loop para encontrar chamadas da macro no código e substituí-las
                for j in range(len(texto)):
                    if aux[0] in texto[j]:
                        texto[j] = texto[j].replace(aux[0], aux[1])

        else:
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
