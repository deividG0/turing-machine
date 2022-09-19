import sys
class Aresta:

    # Classe Aresta
    def __init__(self, inicio, read_letter, fim, written_letter, direction):
        self.inicio = inicio
        self.read_letter = read_letter
        self.fim = fim
        self.written_letter = written_letter
        self.direction = direction

class Vertice:
    # Classe Vertice
    isInitial = False
    isFinal = False

    def __init__(self, dado):
        self.dado = dado

class Grafo:

    # Classe Grafo
    def __init__(self):
        self.verticeInitial = None
        self.arestas = []
        self.vertices = []

    def adicionarVertice(self, dado):
        vertice = Vertice(dado)
        self.vertices.append(vertice)

    def adicionarAresta(self, dadoInicio, read_letter, dadoFim, written_letter, direction):
        inicio = self.getVertice(dadoInicio)
        fim = self.getVertice(dadoFim)

        aresta = Aresta(inicio, read_letter, fim, written_letter, direction)

        self.arestas.append(aresta)

    def getVertice(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                return v

    def setInitial(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                v.isInitial = True
                self.verticeInitial = v
                break

    def setFinal(self, dado):
        for v in self.vertices:
            if v.dado == dado:
                v.isFinal = True
                break

    def isRecognized(self, w, lim_left, lim_right):  # MT
        word = list(w)
        word.insert(0, lim_left)
        word.insert(word.__len__(), lim_right)

        T = [(self.verticeInitial, 1, word)]
        end = False
        accepted = False

        while True:
            for t in T:
                found = False
                for a in self.arestas:
                    if a.inicio == t[0] and (a.read_letter == t[2][t[1]]):

                        # Mudando a palavra
                        nextWord = t[2].copy()
                        nextWord[t[1]] = a.written_letter

                        # Mudando posição do cabeçote
                        if a.direction == 'D':
                            head = t[1] + 1
                        elif a.direction == 'E':
                            head = t[1] - 1
                        else:
                            head = t[1]

                        # Caso o cabeçote tenha chegado ao fim da lista "word" adiciono mais espaços vazios no final
                        # da lista para representar o infinito de espaço vazios à direita da MT
                        if head == nextWord[nextWord.__len__()-1]:
                            nextWord.insert(nextWord.__len__(), lim_right)

                        nextState = a.fim
                        T.append((nextState, head, nextWord))
                        found = True

                if found is False and t[0].isFinal:
                    accepted = True
                    end = True
                    break

                T.remove(t)

                if T.__len__() == 0:
                    end = True
                    break

            if end is True:
                break

        if accepted:
            return "S"
        else:
            return "N"

if __name__ == '__main__':

    grafo = Grafo()

    word = ''
    words = []
    out = sys.stdout

    showLabels = False

    # Entrada de estados
    if showLabels:
        print("Entrada de estados")
    estados = sys.stdin.readline()
    for s in estados.rstrip():
        if s != ' ':
            grafo.adicionarVertice(s)

    # Entrada do alfabeto
    if showLabels:
        print("Entrada do alfabeto de entrada")
    alfabeto = sys.stdin.readline()
    for a in alfabeto:
        if a != ' ':
            alfabeto = alfabeto + a

    # Entrada do alfabeto de fita
    if showLabels:
        print("Entrada do alfabeto de fita")
    alfabetoFita = sys.stdin.readline()
    for a in alfabetoFita:
        if a != ' ':
            alfabeto = alfabetoFita + a

    # Entrada do limitador a esquerda
    if showLabels:
        print("Entrada do limitador a esquerda")
    lim_left = sys.stdin.readline().rstrip()

    # Entrada do limitador a direita
    if showLabels:
        print("Entrada do limitador a direita")
    lim_right = sys.stdin.readline().rstrip()

    # Entrada do numero de transicoes
    if showLabels:
        print("Entrada do numero de transicoes")
    n_transicoes = sys.stdin.readline().rstrip()

    # Entrada transicoes
    if showLabels:
        print("Entrada transicoes")
    n = 0
    while n < int(n_transicoes):  ## LEMBRAR DO <=
        transicoes = sys.stdin.readline()
        if transicoes.rstrip() != '':
            n = n + 1
            grafo.adicionarAresta(dadoInicio=transicoes[0], read_letter=transicoes[2], dadoFim=transicoes[4], written_letter=transicoes[6], direction=transicoes[8])

    # Entrada do estado inicial
    if showLabels:
        print("Estado inicial")
    estado_inicial = sys.stdin.readline()
    grafo.setInitial(estado_inicial.rstrip())

    # Entrada de estados finais
    if showLabels:
        print("Entrada estados finais")
    estados_finais = sys.stdin.readline()
    for s in estados_finais.rstrip():
        if s != ' ':
            grafo.setFinal(s)

    # Entrada das palavras
    palavras = sys.stdin.readline()
    cont = 0
    for p in palavras.rstrip():
        if p != ' ':
            word = word + p
        else:
            words.append(word)
            word = ''

        cont = cont + 1

        if cont == len(palavras.rstrip()):
            words.append(word)

    for w in words:
        out.write(grafo.isRecognized(w, lim_left, lim_right) + '\n')
