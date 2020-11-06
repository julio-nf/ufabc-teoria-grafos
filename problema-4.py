#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
# Problema 4
#
# Meu programa usa uma classe de apoio Graph que recebe uma dict no construtor
# aonde as chaves são os vértices do grafo e os valores das chaves são listas
# que representam as arestas a qual o vértice está conectado.
# Ao iniciar o programa precisamos inserir as entradas n (no de terminais),
# m (no de ferrovias) e [x,y]*m (cada conexão de ferrovia).
# Após receber as entradas usamos o no de terminais como uma lista (range) e
# convertemos essa lista como dict de entrada para a classe Graph, que cria
# uma chave para cada item da lista e uma nova lista vazia para cada valor das
# chaves.
# Com a entrada das ligações das ferrovias usamos o metodo insert_edge para
# inserir as arestas no grafo.
# Um terminal é um possível alvo se sua destruição causa desconexão de pelo
# menos dois terminais e por isso podemos "reduzir" esse problemas ao de
# encontrar vértices de corte.
# Sendo assim chamamos o método search_vertices_corte da classe Graph que
# percorre todas as componentes conexas do grafo usando uma busca DFS
# pelo método _dfs_search_corte e retorna a lista de vértices de corte
# ordenada para o programa.
# Já com a lista apenas imprimimos a quantidade dos vertices de corte e os 
# vertices em si, representando os possíveis terminais alvo.
#


class Graph(object):

  # Método construtor do gráfico que recebe uma dict aonde as keys são os
  # vértices e os values são listas que mostram a quais outros vértices
  # este vértice está ligado
  def __init__(self, g):
    # Dict do grafo, reproduzindo uma lista de adjacências
    self._graph_dict = g
    self._initialize_dict()

    # Vetores auxiliares do 
    self._vis = []
    self._pred = []
    self._ord = []
    self._low = []
    self._count = 0

    # Vetor com os vertices de corte a ser retornado pela classe
    self._vertices_corte = []


  # Inicializa a dict do grafo fazendo cada valor das chaves que seja nulo
  # virar uma lista vazia
  def _initialize_dict(self):
    for u, v in self._graph_dict.items():
      if v is None:
        self._graph_dict[u] = []


  # Método para inserir uma aresta recebendo como parâmetro uma tupla com dois
  # valores (x,y) que representam uma aresta entre os vértices x e y
  def insert_edge(self, edge):
    (u,v) = edge

    if u in self._graph_dict:
      self._graph_dict[u].append(v)
      self._graph_dict[v].append(u)
    else:
      self._graph_dict[u] = v
      self._graph_dict[v] = u


  # Método que busca os vértices de corte do grafo e os retorna como uma lista
  def search_vertices_corte(self):
    # Limpando os atributos de ajuda
    self._vis.clear
    self._pred.clear
    self._ord.clear
    self._low.clear
    self._vertices_corte.clear

    # Populando vetores de visitados e predecessores com Falso, Nulo e -1
    for x in self._graph_dict:
      self._vis.append(False)
      self._pred.append(None)
      self._ord.append(-1)
      self._low.append(-1)

    # Inicializando o contador
    self._count = 0

    # Executando uma busca DFS em cada componente conexa do grafo e capturando
    # os vertices de corte
    for v in self._graph_dict:
      if not self._vis[v]:
        self._dfs_search_corte(v)

    # Retornando a lista com os vertices de corte
    self._vertices_corte.sort()
    return self._vertices_corte


  # Método de busca em profundidade (DFS) utilizando o algoritmo apresentado
  # em aula, com modificações para identificar a adicionar vertices de corte
  def _dfs_search_corte(self, u, father = -1):
    # Marcando o vetor da iteração como visitado, incrementando o contador
    # e usando-o para definir a ordem e o low
    self._vis[u] = True
    self._count += 1
    self._ord[u] = self._low[u] = self._count

    # Auxiliar para contar os filhos de um vertice, para verificarmos se a
    # raiz também é um vertice de corte
    children = 0

    # Percorrendo os vizinhos do vértice
    for v in self._graph_dict[u]:
      # Se for o mesmo, pula
      if v == father: pass

      # Caso nao tenhamos visitado esse vizinho ainda, marcamos como seu
      # predecessor o vertice atual e fazemos uma chamada recursiva para
      # a DFS passando o vizinho como vertice e o v atual como pai
      if self._vis[v] == False:
        self._pred[v] = u
        self._dfs_search_corte(v, u)

        # Se existir um low maior ou igual a ordem do vizinho v, e, se nao
        # estivermos falando da raiz da árvore DFS, então o vertice u é um
        # vertice de corte e incluimos ele na lista
        if (self._low[v] >= self._ord[v]) and father != -1:
          self._vertices_corte.append(u)

        # Atualizamos o low pois agora chegamos em um vertice com tempo melhor
        # do que já tinhamos em low
        self._low[u] = min(self._low[u], self._low[v])

        # Incrementamos o filho desse vértice para cada chamada recursiva
        children += 1

      else:
        # Se já tivermos visitado v e se ela for diferente do predecessor
        # então é uma aresta de retorno e daí atualizamos low
        if v != self._pred[u]:
          self._low[u] = min(self._low[u], self._ord[v])

    # Caso estejamos falando da raiz adicionamos o vértice a lista de corte
    # apenas se esse tiver mais de um filho na árvore DFS
    if father == -1 and children > 1:
      self._vertices_corte.append(u)


if __name__ == "__main__":

  # Recebe o inteiro do número de terminais e transforma em uma lista
  # contendo o range do tamanho do int passado
  n_terminais = list(range(int(input())))

  # Inicia o grafo usando uma dict aonde as chaves vem da lista de terminais
  # do comando anterior, inicialmente com valores vazios em todas as chaves
  graph = Graph(dict.fromkeys(n_terminais))

  # Recebe o número de ferrovias da malha inimiga
  n_ferrovias = int(input())

  # Para cada ferrovia, recebe a entrada dos vertices separado por espaço
  # (u v) e insere a aresta no grafo
  for x in range(n_ferrovias):
    a, b = map(int, input().split())
    graph.insert_edge((a, b))

  # Chama o método que procura os vértices de corte e guarda a lista
  vertices_corte = graph.search_vertices_corte()

  # Caso o retorno não seja vazio, imprimimos a quantidade e os v de corte
  if len(vertices_corte) > 0:
    print(f'# de alvos possiveis: {len(vertices_corte)}')
    print(*vertices_corte, sep="\n")
