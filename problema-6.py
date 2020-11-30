#
# UFABC - Teoria dos Grafos
# Prof. Maycon Sambinelli
# --------------------------
# Nome: Julio Novais da Fonseca  RA: 21073215
# 
# Problema 6
#
# O problema pode ser transformado num problema de ordenação topológica
# utilizando digrafos. Apesar de nao utilizar o algoritmo de descoberta
# da ordenação topológica a lógica que utilizei foi de inserir os arcos
# ao digrafo de forma que fiquem ordenados, a partir daí uma busca em
# profundidade para capturar todas as dependências de um módulo é suficiente
# para imprirmos as instruções do makefile em ordem correta e recompilarmos
# a solução.
# Meu programa utiliza duas classes auxiliares: GraphHandler, que tem métodos
# de adicionar arcos ao digrafo e iniciar uma DFS no grafo; e Modules, que é
# uma representação em forma de objeto dos módulos do makefile, contendo o
# nome, a lista de suas dependências e suas instruções

# Classe auxilias GraphHandler que possui os métodos de inserir aresta (arco)
# e a Busca por Profundidade (DFS)
class GraphHandler(object):

  # Método construtor do digrafo que apenas guarda os vertices visitados
  def __init__(self):
    self._vis = []

  # Método para inserir um arco ao digrafo recebendo como parâmetro o digrafo
  # e uma tupla com dois valores que representam um arco entre os vértices x,y
  def insert_edge(self, d, edge):
    (u,v) = edge

    if u in d:
      d[u].append(v)
    elif v is None:
      d[u] = []
    else:
      d[u] = [v]

  # Método para inicializar a DFS populando os vertices visitados como falso
  # e passando o vertice inicial para a DFS_Search.
  # Como o p
  def dfs(self, g, s):
    for x in g.items():
      self._vis.append(False)

    self._dfs_search(g, s)

  # DFS Search adaptada para utilizar o objeto Modules imprimindo os comandos
  # da instância de Modules ao final da busca do nó
  def _dfs_search(self, g, u):
    self._vis[u.index] = True

    for v in g[u]:
      # Recuperando o objeto pelo nome dele
      v_obj = next((x for x in g if x.name == v), None)

      # Se for um modulo que não é alvo de alguma regra, ou seja,
      # não está no digrafo, apenas ignoramos
      if v_obj is None: continue

      if self._vis[v_obj.index] == False:
        self._dfs_search(g, v_obj)

    # Após chegar ao final da busca de uma dependencia, imprimimos suas regras
    print(*u.commands, sep='\n')


# Classe auxiliar com o nome, index, dependências e comandos de um dado modulo
# usado como objeto para manusear o digrafo
class Modules(object):
  def __init__(self, name, index, dependencies):
    self.name = name
    self.index = index
    self.dependencies = dependencies
    self.commands = []
 
  def add_command(self, cmd):
    self.commands.append(cmd)


if __name__ == "__main__":
  # Lista de instancias de Modules, representando os modulos
  # a serem recompilados
  modules_list = []

  # Dict que representa o digrafo dos modulos e instancia da classe
  # utilitaria GraphHandler
  modules_digraph = {}
  graph_handler = GraphHandler()

  # Capturando o alvo inicial do makefile
  make = input().split()[1]

  index = 0
  # Enquanto recebemos entradas no programa...
  while True:
    line = input()

    # Se a entrada for 'FIM' fechamos o input
    if line == 'FIM': break

    # Se não começar com TAB, sabemos que é uma entrada de alvo e suas deps
    if not line.startswith('\t'):
      # Splitamos a entrada para capturar o alvo em si e suas dependencias
      # em variaveis separadas, target e target_deps respectivamente.
      splitted_line = line.split(':')
      target = str(splitted_line[0]);
      target_deps = splitted_line[1].strip().split()

      # Adicionamos o modulo na lista de modulos a recompilar
      modules_list.append(Modules(target, index, target_deps))

      # Incrementamos o indice para o proximo modulo
      index += 1
    else:
      # Se a entrada começar com TAB sabemos que são instruções do ultimo
      # alvo adicionado na lista, portanto usamos a função add_command
      # da classe utilitária Modules para adicionar seus comandos
      modules_list[-1].add_command(str(line).strip())

  # Percorrando a lista de modulos e suas dependencias e adicionando os
  # arcos ao digrafo, precisamos checar se o ALVO não tem nenhuma dependencia
  # pois precisamos adicioná-lo ao grafo mesmo assim
  for mdl in modules_list:
    if len(mdl.dependencies) != 0:
      for dep in mdl.dependencies:
        graph_handler.insert_edge(modules_digraph, (mdl, dep))
    else:
      graph_handler.insert_edge(modules_digraph, (mdl, None))

  # Capturando o objeto com o nome do alvo inicial do makefile e utilizando-o
  # para iniciar a busca DFS ao digrafo
  make_obj = next((x for x in modules_digraph if x.name == make), None)
  graph_handler.dfs(modules_digraph, make_obj)
