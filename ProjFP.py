"""
1o PROJETO DE FP
Antonio Delgado
ist1106658
LEIC-T
"""


def limpa_texto(texto: str) -> str:
    """retira whitespaces de texto"""
    return " ".join(texto.split())


def corta_texto(texto: str, largura: int) -> tuple:
    """Esta função devolve um tuplo estando o 1º elemento cortado do resto"""
    texto = limpa_texto(texto)
    posicao = largura - 1  # Um elemento de uma string/lista começa do 0
    if posicao < len(texto) and texto[posicao] != " ":
        if posicao + 1 < len(texto) and texto[posicao + 1] != " ":
            while posicao >= 0 and texto[posicao] != " ":
                posicao -= 1
    return texto[:posicao + 1].strip(), texto[posicao + 1:].strip()


def insere_espacos(texto: str, largura: int) -> str:
    """Esta função distribui os espaços (resultantes da diferença entre a largura e o tamanho da string) ordenadamente"""
    texto = limpa_texto(texto)
    size = len(texto)
    espacos = largura - size
    texto = texto.split()  # Como uma string não é alterável passei para uma lista
    i = 0
    if largura >= size:
        if len(texto) >= 2:  # O enunciado diz 2 ou mais palavras
            while espacos != 0:
                texto[i] = texto[i] + " "
                i += 1
                espacos -= 1
                if i == len(texto) - 1:  # O último elemento não conta, o ciclo recomeça
                    i = 0
            return " ".join(texto)
        espacos = largura - size
        while espacos != 0:
            texto[0] = texto[0] + " "
            espacos -= 1
        return texto[0]


def justifica_texto(texto: str, largura: int) -> tuple:
    """Esta função devolve o texto justificado"""
    if not isinstance(texto, str) or not isinstance(largura, int) or largura < 0:
        raise ValueError("justifica_texto: argumentos invalidos")
    texto = limpa_texto(texto)
    if texto == "":
        raise ValueError("justifica_texto: argumentos invalidos")
    contador = 0
    palavras = texto.split()  # Qualquer palavra tem de ser menor do que a largura
    tamanho_lista = len(palavras)
    while contador != tamanho_lista:
        if len(palavras[contador]) >= largura:
            raise ValueError("justifica_texto: argumentos invalidos")
        contador += 1
    resultado_final = []
    texto_cortado = corta_texto(texto, largura)
    while texto_cortado != ("", ""):  # Cortar texto em cada elemento
        tamanho_lista = texto_cortado[0]
        texto_cortado = (texto_cortado[1],)
        texto_cortado = corta_texto(texto_cortado[0], largura)
        resultado_final = resultado_final + [tamanho_lista]
    contador = 0
    while contador != len(resultado_final) - 1:  # Adicionar espaços, -1 porque o ultimo elemento não segue esta regra
        resultado_final[contador] = insere_espacos(resultado_final[contador], largura)
        contador += 1
    len_elemento_final = len(resultado_final[-1])
    while len_elemento_final != largura:  # ultimo elmento tem de ter espaços até ao fim
        resultado_final[-1] = resultado_final[-1] + " "
        len_elemento_final += 1
    return tuple(resultado_final)


def calcula_quocientes(dic1: dict, num: int) -> dict:
    """devolve o dicionário com as mesmas chaves do dicionário argumento"""
    l = []
    dic2 = {}
    for i in dic1:
        for x in range(1, num + 1):
            dic2[i] = dic1[i] / x
            l += [dic2[i]]
        dic2[i] = l
        l = []
    return dic2


def atribui_mandatos(dic1: dict, num: int) -> list:
    """devolve uma lista ordenada contendo as cadeias de carateres dos partidos que obtiveram cada mandato"""
    final = []
    dic2 = calcula_quocientes(dic1, num)
    a = list(dic2.values())

    for h in range(num):
        b = [x[0] for x in a]
        ind = len(b) - 1 - b[::-1].index(max(b))
        a[ind].pop(0)
        final.append(list(dic2.keys())[ind])

    return final


def obtem_partidos(dic1: dict) -> list:
    """devolve a lista por ordem alfabética com o nome de todos os partidos"""
    res = []
    for i in dic1:
        for n in dic1[i]["votos"]:
            res += [n]
    res = set(res)
    res = list(res)
    res.sort()
    return res


def remove_itens(test_list: list, item) -> list:
    """Remove um item para todas as suas ocorrências"""
    c = test_list.count(item)
    for i in range(c):
        test_list.remove(item)
    return test_list


def obtem_resultado_eleicoes(dic1: dict) -> list:
    """Organiza as eleições ordenadamete por deputados e votos"""
    if not isinstance(dic1, dict) or dic1 == {}:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    for n in dic1:
        if not isinstance(dic1[n], dict) or dic1[n] == {} or dic1[n]["votos"] == {} \
                or not isinstance(dic1[n]["votos"], dict) or len(dic1[n]) != 2:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        for g in dic1[n]["votos"]:
            if not isinstance(g, str) or not isinstance(dic1[n]["votos"][g], int) or n == "" or g == "" \
                    or dic1[n]["deputados"] < 1 or dic1[n]["votos"][g] < 1 or not isinstance(n, str):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    megalista = []
    res = []
    for i in dic1:
        lista = atribui_mandatos(dic1[i]["votos"], dic1[i]["deputados"])
        megalista += lista
    for q in dic1:
        for p in dic1[q]["votos"]:
            if p not in megalista and p not in (k[0] for k in res):
                res += [[p, 0, 0]]
    while megalista:
        qnt = megalista.count(megalista[0])
        res += [[megalista[0], qnt, 0]]
        megalista = remove_itens(megalista, megalista[0])
    for m in dic1:
        for a in dic1[m]["votos"]:
            contador = 0
            while contador != len(res):
                if res[contador][0] == a:
                    res[contador][2] += dic1[m]["votos"][a]
                    break
                contador += 1
    contador = 0
    while contador != len(res):
        res[contador] = tuple(res[contador])
        if contador != 0 and res[contador][1] > res[contador - 1][1]:
            res[contador], res[contador - 1] = res[contador - 1], res[contador]
            contador = 0
            continue
        if res[contador][1] == res[contador - 1][1]:
            if res[contador][2] > res[contador - 1][2]:
                res[contador], res[contador - 1] = res[contador - 1], res[contador]
                contador = 0
                continue
        contador += 1
    return res


def produto_interno(tuplo1: tuple, tuplo2: tuple) -> float:
    """Calcula o produto interno/escalar entre dois vetores"""
    contador = 0
    auxiliar = 0
    tamanho_tuplo = len(tuplo1)
    while contador != tamanho_tuplo:
        auxiliar += tuplo1[contador] * tuplo2[contador]
        contador += 1
    return float(auxiliar)


def verifica_convergencia(matriz: tuple, tpl_res: tuple, tpl_sol: tuple, real: float) -> bool:
    """Verifica a convergência da solução com um determinado valor real"""
    a1 = ()
    for i in range(len(matriz)):
        a1 += (produto_interno(matriz[i], tpl_sol),)
    contador = 0
    while contador != len(a1):
        if abs(a1[contador] - tpl_res[contador]) >= real:
            return False
        contador += 1
    return True


def retira_zeros_diagonal(matriz: tuple, vetor: tuple) -> tuple:
    tamanho_mat = len(matriz)
    matriz = list(matriz)
    vetor = list(vetor)
    contador = 0
    while contador != tamanho_mat:
        while matriz[contador][contador] == 0:  # Verificar se há um zero na diagonal
            for i in range(tamanho_mat):
                if i == contador:
                    continue
                if matriz[i][contador] != 0 and matriz[contador][i] != 0:
                    matriz[contador], matriz[i], vetor[contador], vetor[i] = matriz[i], matriz[contador], vetor[i], \
                                                                             vetor[contador]
                    break
        contador += 1
    return tuple(matriz), tuple(vetor)


def soma_tpl(tpl: tuple) -> float:
    """Soma todos os elementos de um tuplo"""
    contador = 0
    tam = len(tpl)
    soma = 0
    while contador != tam:
        soma += abs(tpl[contador])
        contador += 1
    return soma


def eh_diagonal_dominante(matriz: tuple) -> bool:
    """Verifica se a matriz é diagonalmente dominante"""
    contador = 0
    tamanho_mat = len(matriz)
    while contador != tamanho_mat:
        if soma_tpl(matriz[contador]) - 2 * abs(matriz[contador][contador]) > 0:
            return False
        contador += 1
    return True


def resolve_sistema(matriz: tuple, tpl_res: tuple, real: float) -> tuple:
    """Resolve um sistema utilizando o método de jacobi"""
    if not isinstance(matriz, tuple) or not isinstance(tpl_res, tuple) or len(matriz) != len(tpl_res) or not isinstance(
            real, float) or matriz == () or tpl_res == () or real <= 0:
        raise ValueError("resolve_sistema: argumentos invalidos")
    for k2 in tpl_res:
        if not isinstance(k2, int or float):
            raise ValueError("resolve_sistema: argumentos invalidos")
    for k1 in matriz:
        if not isinstance(k1, tuple) or len(k1) != len(matriz[0]):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for i in k1:
            if not isinstance(i, int or float):
                raise ValueError("resolve_sistema: argumentos invalidos")
    (matriz, tpl_res) = retira_zeros_diagonal(matriz, tpl_res)
    if not eh_diagonal_dominante(matriz):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")

    tpl_sol = [0] * len(matriz)
    while not verifica_convergencia(matriz, tpl_res, tuple(tpl_sol), real):
        x = tpl_sol.copy()
        for i in range(len(tpl_sol)):
            tpl_sol[i] = x[i] + ((tpl_res[i] - (produto_interno(matriz[i], tuple(x)))) / matriz[i][i])
    return tuple(tpl_sol)
