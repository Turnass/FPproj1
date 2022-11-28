"""
2o PROJETO DE FP
Antonio Delgado
ist1106658
LEIC-T
"""


# TAD GERADOR
# Operacoes basicas
# Construtores


def cria_gerador(b: int, s: int):
    """Recebe os bits(b) e a seed(s) e devolve o gerador"""
    if not isinstance(b, int) or not isinstance(s, int) or (b != 32 and b != 64) or s <= 0:
        raise ValueError("cria_gerador: argumentos invalidos")
    elif s > 2 ** b:
        raise ValueError("cria_gerador: argumentos invalidos")
    return [b, s]


def cria_copia_gerador(g):
    """Copia o gerador criado"""
    return g.copy()


# Seletores


def obtem_estado(g) -> int:
    """Devolve a seed"""
    return g[1]


# Modificadores


def define_estado(g, s: int) -> int:
    """Define o estado do gerador"""
    g[1] = s
    return obtem_estado(g)


def atualiza_estado(g) -> int:
    """Atualiza o estado do gerador utilizando xorshift"""
    if g[0] == 32:
        g[1] ^= (obtem_estado(g) << 13) & 0xFFFFFFFF
        g[1] ^= (obtem_estado(g) >> 17) & 0xFFFFFFFF
        g[1] ^= (obtem_estado(g) << 5) & 0xFFFFFFFF
    else:
        g[1] ^= (obtem_estado(g) << 13) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (obtem_estado(g) >> 7) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (obtem_estado(g) << 17) & 0xFFFFFFFFFFFFFFFF
    return obtem_estado(g)


# Reconhecedor


def eh_gerador(g) -> bool:
    """Retorna True se for gerador e False caso contrario"""
    return isinstance(g, list) and len(g) == 2 and isinstance(g[0], int) and isinstance(obtem_estado(g), int) and (
            g[0] == 32 or g[0] == 64) and 0 < obtem_estado(g) <= 2 ** g[0]


# Teste


def geradores_iguais(g1, g2) -> bool:
    """Retorna True se ambos os geradores recebidos forem iguais e False caso contrario"""
    return eh_gerador(g1) and eh_gerador(g2) and g1 == g2


# Transformador


def gerador_para_str(g) -> str:
    """Retorna o gerador em string"""
    return f"xorshift{g[0]}(s={g[1]})"


# Funcoes alto nivel


def gera_numero_aleatorio(g, n: int) -> int:
    """Gera um numero pseudoaleatorio"""
    s = atualiza_estado(g)
    return (s % n) + 1


def gera_carater_aleatorio(g, letra: str) -> str:
    """Gera um carater pseudoaleatorio"""
    cad = ""
    for i in range(ord("A"), ord(letra) + 1):
        cad += chr(i)
    return cad[atualiza_estado(g) % len(cad)]


# TAD COORDENADA
# Operacoes basicas
# Construtor


def cria_coordenada(col: str, lin: int) -> tuple:
    """Recebe uma coluna(col) e uma linha(lin) e retorna um coordenada, validando os argumentos de entrada"""
    if not isinstance(col, str) or col not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or len(col) != 1 or not isinstance(lin,
                                                                                                              int) or lin <= 0 or lin >= 100:
        raise ValueError("cria_coordenada: argumentos invalidos")
    return col, lin


# Seletores


def obtem_coluna(c) -> str:
    """Obtem coluna da coordenada"""
    return c[0]


def obtem_linha(c) -> int:
    """Obtem linha da coordenada"""
    return c[1]


# Reconhecedor


def eh_coordenada(c) -> bool:
    """Retorna True caso o argumento recebido seja uma coordenada e False caso contrario"""
    return isinstance(c, tuple) and len(c) == 2 and isinstance(obtem_coluna(c), str) and isinstance(obtem_linha(c),
                                                                                                    int) and obtem_coluna(
        c) in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and 0 < obtem_linha(c) < 100


# Teste


def coordenadas_iguais(c1, c2) -> bool:
    """Verifica se duas coordenadas sao coordenadas e se sao iguais"""
    return eh_coordenada(c1) and eh_coordenada(c2) and c1 == c2


# Transformador


def coordenada_para_str(c) -> str:
    """Devolve um cooordenada em string"""
    return obtem_coluna(c) + (str(obtem_linha(c))).zfill(2)


def str_para_coordenada(string: str):
    """Devolve uma string para coordenada"""
    return string[0], int(string[1:])


# Funcoes alto nivel


def obtem_coordenadas_vizinhas(c) -> tuple:
    """Obtem todas as coordenadas adjacentes a coordenada de entrada"""
    col = [-1, 0, 1, 1, 1, 0, -1, -1]
    lin = [-1, -1, -1, 0, 1, 1, 1, 0]
    t = ()
    for i in range(8):
        if chr(ord(obtem_coluna(c)) + col[i]) in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and 0 < obtem_linha(c) + lin[i] < 100:
            t += (cria_coordenada(chr(ord(obtem_coluna(c)) + col[i]), obtem_linha(c) + lin[i]),)
    return t


def obtem_coordenada_aleatoria(c, g):
    """Obtem uma coordenada pseudoalatoria"""
    return cria_coordenada(gera_carater_aleatorio(g, obtem_coluna(c)), gera_numero_aleatorio(g, obtem_linha(c)))


# TAD Parcela
# Operacoes Basicas
# Construtor


def cria_parcela():
    """Cria uma parcela"""
    return ["tapada", False]


def cria_copia_parcela(parcela):
    """Cria uma copia da parcela de entrada"""
    parcela_copia = parcela.copy()
    return parcela_copia


# Modificadores


def limpa_parcela(parcela):
    """Altera o estado da parcela para limpa"""
    parcela[0] = "limpa"
    return parcela


def marca_parcela(parcela):
    """Altera o estado da parcela para marcada"""
    parcela[0] = "marcada"
    return parcela


def desmarca_parcela(parcela):
    """Desmaraca a parcela, alterando o seu estado para tapada"""
    parcela[0] = "tapada"
    return parcela


def esconde_mina(parcela):
    """Coloca mina na parcela de entrada"""
    parcela[1] = True
    return parcela


# Reconhecer


def eh_parcela(parcela) -> bool:
    """Retorna True caso o argumento de entrada seja uma parcela e False caso contrario"""
    return isinstance(parcela, list) and len(parcela) == 2 and isinstance(parcela[0], str) and isinstance(parcela[1],
                                                                                                          bool) and \
           parcela[0] in ("tapada", "limpa", "marcada")


def eh_parcela_tapada(parcela) -> bool:
    """Devlove True caso a parcela seja tapada e False caso contrario"""
    return parcela[0] == "tapada"


def eh_parcela_marcada(paracela) -> bool:
    """Devlove True caso a parcela seja marcada e False caso contrario"""
    return paracela[0] == "marcada"


def eh_parcela_limpa(parcela) -> bool:
    """Devlove True caso a parcela seja limpa e False caso contrario"""
    return parcela[0] == "limpa"


def eh_parcela_minada(parcela) -> bool:
    """Devlove True caso a parcela seja minada e False caso contrario"""
    return parcela[1]


# Teste


def parcelas_iguais(p1, p2) -> bool:
    """Averigua se os dois argumentos sao parcelas e se sao iguais, devolvendo True caso for verdade e
     False noutra instancia"""
    return eh_parcela(p1) and eh_parcela(p2) and p1 == p2


# Transformadores


def parcela_para_str(parcela) -> str:
    """Devolve a parcela em string"""
    if parcela[0] == "tapada":
        return "#"
    elif parcela[0] == "marcada":
        return "@"
    elif parcela[0] == "limpa":
        if parcela[1]:
            return "X"
        return "?"


# Funcoes alto nivel


def alterna_bandeira(parcela) -> bool:
    """Marca a parcela caso esta se encontre tapada, desmarca caso esteja marcada retornando True.
     Retorna False noutra hipotese"""
    if eh_parcela_marcada(parcela):
        desmarca_parcela(parcela)
        return True
    elif eh_parcela_tapada(parcela):
        marca_parcela(parcela)
        return True
    return False


# TAD Campo
# Operacoes Basicas
# Construtor


def cria_campo(c: str, l: int):
    """Recebe uma coluna(c) e uma linha(l), verificando estes argumentos e cria o campo de comprimento
    (posicao de c no alfabeto) e largura l"""
    if not isinstance(c, str) or not isinstance(l, int) or len(
            c) != 1 or c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or not 0 < l < 100:
        raise ValueError("cria_campo: argumentos invalidos")
    lista = []
    n = 1
    while n != l + 1:
        a = ord("A")
        lista1 = []
        while a != ord(c) + 1:
            lista1.append(cria_parcela())
            a += 1
        lista.append(lista1)
        n += 1
    return lista


def cria_copia_campo(m):
    """Cria uma copia VERDADEIRA do campo de entrada"""
    if isinstance(m, list):
        return [cria_copia_campo(e) for e in m]
    return m


# Reconhecedores


def eh_campo(m) -> bool:
    """Retorna True caso o argumento de entrada seja um campo e False para qualquer outro caso"""
    if not isinstance(m, list) or m == []:
        return False
    for i in m:
        if not isinstance(i, list) and i == []:
            return False
        for n in i:
            if not eh_parcela(n):
                return False
    return True


def eh_coordenada_do_campo(m, c) -> bool:
    """Retorna True caso coordenada(c) esteja dentro do campo(m) e False em outrora"""
    if len(m) >= obtem_linha(c):
        for i in m:
            if len(i) > ord(obtem_coluna(c)) - 65:
                return True
    return False


# Seletores


def obtem_ultima_coluna(m) -> str:
    """Retorna a ultima coluna do campo"""
    return chr(len(m[0]) + 64)


def obtem_ultima_linha(m) -> int:
    """Retorna a ultima linha do campo"""
    return len(m)


def obtem_parcela(m, c):
    """Devolve a parcela correspondente a coordenada do campo"""
    return m[obtem_linha(c) - 1][ord(obtem_coluna(c)) - 65]


def obtem_coordenadas(m, s: str) -> tuple:
    """Devolve todas as coordenadas que se presupoem uma determinada condicao(limpas, tapadas, marcadas, minadas)"""
    t = ()
    for k in range(1, obtem_ultima_linha(m) + 1):
        for n in range(ord(obtem_ultima_coluna(m)) - 64):
            c = cria_coordenada(chr(n + 65), k)
            if s == "limpas":
                if eh_parcela_limpa(obtem_parcela(m, c)):
                    t += (c,)
            elif s == "tapadas":
                if eh_parcela_tapada(obtem_parcela(m, c)):
                    t += (c,)
            elif s == "marcadas":
                if eh_parcela_marcada(obtem_parcela(m, c)):
                    t += (c,)
            else:
                if eh_parcela_minada(obtem_parcela(m, c)):
                    t += (c,)
    return t


def obtem_numero_minas_vizinhas(m, c) -> int:
    """Retribui a quantidade de parcelas minadas na redondesa da coordenada"""
    a = obtem_coordenadas_vizinhas(c)
    num = 0
    for i in a:
        if eh_coordenada_do_campo(m, i):
            if eh_parcela_minada(obtem_parcela(m, i)):
                num += 1
    return num


# Teste


def campos_iguais(m1, m2) -> bool:
    """Confirma se os dois argumentos sao campos e iguais, devolvendo True se sim e False se nao"""
    return eh_campo(m1) and eh_campo(m2) and m1 == m2


# Transformador


def campo_para_str(m) -> str:
    """Representa o campo em forma de string"""
    b = ""
    for i in range(ord(obtem_ultima_coluna(m)) - 64):
        b += chr(i + 65)
    c = f"   {b}" + "\n  +" + "-" * len(b) + "+"
    for n in range(1, obtem_ultima_linha(m) + 1):
        c += "\n" + f"{obtem_linha(cria_coordenada('A', n))}".zfill(2) + "|"
        for i in range(ord(obtem_ultima_coluna(m)) - 64):
            if parcela_para_str(obtem_parcela(m, cria_coordenada(chr(i + 65), n))) != "?":
                c += parcela_para_str(obtem_parcela(m, cria_coordenada(chr(i + 65), n)))
                continue
            elif obtem_numero_minas_vizinhas(m, cria_coordenada(chr(i + 65), n)) != 0:
                c += str(obtem_numero_minas_vizinhas(m, cria_coordenada(chr(i + 65), n)))
                continue
            c += " "
        c += "|"
    c += "\n  +" + "-" * len(b) + "+"
    return c


# Funcoes alto nivel


def coloca_minas(m, c, g, n: int):
    """Distribui n minas no campo(m) de forma pseudoaleatoria(utilizando o gerador(g)), de maneira a nao coicidirem com
     a coordenada(c)"""
    bombas = []
    for i in range(n):
        a = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        while a in obtem_coordenadas_vizinhas(c) or a in bombas or coordenadas_iguais(a, c):
            a = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        bombas.append(a)
    for coordenadas in bombas:
        esconde_mina(obtem_parcela(m, coordenadas))
    return m


def limpa_campo(m, c) -> list:
    """Devolve o campo limpo na coordenada(c), isto e, limpa todas as parcelas iterativamente, parando (inclusive) naquelas
     que contenham minas nas parcelas adjacentes"""
    l = [c]
    while len(l) > 0:
        new_c = l.pop(0)
        limpa_parcela(obtem_parcela(m, new_c))
        if obtem_numero_minas_vizinhas(m, new_c) == 0 and not eh_parcela_minada(obtem_parcela(m, new_c)):
            for i in obtem_coordenadas_vizinhas(new_c):
                if not eh_coordenada_do_campo(m, i) or eh_parcela_limpa(obtem_parcela(m, i)) or eh_parcela_marcada(
                        obtem_parcela(m, i)) or i in l:
                    continue
                l += [i]
    return m


# Funcoes adicionais


def jogo_ganho(m) -> bool:
    """Retorna True caso o jogador consiga vencer o jogo, retornando False caso ainda nao"""
    if len(obtem_coordenadas(m, "tapadas")) + len(obtem_coordenadas(m, "marcadas")) != len(
            obtem_coordenadas(m, "minadas")):
        return False
    return True


def turno_jogador(m) -> bool:
    """Pede ao jogador para fazer um input (repetindo o mesmo ate ser valido), retornando False caso o tenha limpado uma
     parcela minada e True noutra instancia"""
    while True:
        escolha = input("Escolha uma ação, [L]impar ou [M]arcar:")
        if escolha == "L" or escolha == "M":
            break
    while True:
        c = ()
        try:
            coordenada = input("Escolha uma coordenada:")
            if len(coordenada) == 3:
                if eh_coordenada(str_para_coordenada(coordenada)):
                    c = str_para_coordenada(coordenada)
                    if eh_coordenada(c) and eh_coordenada_do_campo(m, c):
                        break
        except ValueError:
            continue
    if escolha == "L":
        limpa_campo(m, c)
        if eh_parcela_minada(obtem_parcela(m, c)):
            return False
    else:
        alterna_bandeira(obtem_parcela(m, c))
    return True


def minas(c: str, l: int, n: int, d: int, s: int) -> bool:
    """Esta representa a funcao final do jogo das minas. Recebe uma coluna(c) e uma linha(l) para criar o campo, o numero
     de minas n, seguido pelos bits(d) e a seed(s) para criar o gerador. Esta utiliza funcoes anteriores de maneira a correr
      o jogo, deixando ainda o jogador ver o numero de bandeiras que estao ao seu dispor"""
    try:
        m = cria_campo(c, l)
        g = cria_gerador(d, s)
        if not isinstance(n, int) or n <= 0 or n > (ord(obtem_ultima_coluna(m)) - 64) * obtem_ultima_linha(m) - 10:
            raise ValueError
    except ValueError:
        raise ValueError("minas: argumentos invalidos")
    print(f"   [Bandeiras {len(obtem_coordenadas(m, 'marcadas'))}/{n}]")
    print(campo_para_str(m))
    while True:
        coordenada = ""
        try:
            coordenada = input("Escolha uma coordenada:")
            if len(coordenada) == 3:
                if eh_coordenada(str_para_coordenada(coordenada)):
                    c = str_para_coordenada(coordenada)
                    if eh_coordenada(c) and eh_coordenada_do_campo(m, c):
                        break
        except ValueError:
            continue
    c = str_para_coordenada(coordenada)
    coloca_minas(m, c, g, n)
    limpa_campo(m, c)
    print(f"   [Bandeiras {len(obtem_coordenadas(m, 'marcadas'))}/{n}]")
    print(campo_para_str(m))
    while turno_jogador(m):
        print(f"   [Bandeiras {len(obtem_coordenadas(m, 'marcadas'))}/{n}]")
        print(campo_para_str(m))
        if jogo_ganho(m):
            print("VITORIA!!!")
            return True
    print(f"   [Bandeiras {len(obtem_coordenadas(m, 'marcadas'))}/{n}]")
    print(campo_para_str(m))
    print("BOOOOOOOM!!!")
    return False

minas("Z", 5, 13, 64, 313414)