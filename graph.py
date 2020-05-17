import copy
import math
import random
from disjointsets import DisjointSet

"""
	The graph is represented with two dictionaries, dictIn and dictOut for
	the inbound and outbound edges connected to each vertex.
	The keys of the dictionary are the vertices.

	dictCosts is a dictionary with the keys being edges and the values being
	the costs of the edges.

	Name: Şut George
	Group: 917
"""


class DoubleDictGraph:

	def __init__(self, number_of_nodes, directed):
		self._dictOut = {}
		self._dictIn = {}
		self._dictCosts = {}
		self._directed = directed		
		self._number_of_edges = 0
		self._number_of_nodes = 0
		for i in range(number_of_nodes):
			self._dictOut[i] = []
			self._dictIn[i] = []

	"""
	def get_dict_out(self):
		return self._dictOut


	def get_dict_in(self):
		return self._dictIn

	"""

	def change_type(self, directed):	
		self._directed = directed

	def get_vertices(self):
		"""
			Returns an iterable containing all the vertices
		"""
		return self._dictOut.keys()

	def get_number_of_vertices(self):
		"""
			Returns the number of vertices in the graph
		"""
		return len(self.get_vertices())

	def get_outbound_neighbours_of_vertex_X(self, x):
		"""
			Returns a list containing the outbound neighbours of x
		"""
		return self._dictOut[x]

	def get_inbound_neighbours_of_vertex_X(self, x):
		"""
			Returns a list containing the inbound neighbours of x
		"""
		return self._dictIn[x]

	def is_edge(self, x, y):
		"""
			Returns True if there is an edge from x to y, False otherwise
		"""
		try:
			if self._directed == False:
				if y in self._dictOut[x] and x in self._dictOut[y]:
					return True
				return False
			return y in self._dictOut[x]
		except KeyError:
			return False

	def add_edge(self, x, y, cost):
		"""
			Adds an edge from x to y with the cost "cost".
			Precondition: there is no edge from x to y
		"""
		if self.is_edge(x, y):
			print("There is already an edge from {} to {}!\n".format(x, y))
			return

		self._dictOut[x].append(y)
		self._dictIn[y].append(x)
		self._dictCosts[(x, y)] = cost
		self._number_of_edges += 1
		if self._directed == False:
			self._dictOut[y].append(x)
			self._dictIn[x].append(y)
			self._dictCosts[(y, x)] = cost	


	def remove_edge(self, x, y):
		"""
			Removes the edge from x to y.
			Precondition: there is an edge from x to y.
		"""

		if not self.is_edge(x, y):
			print("There is no edge between x and y!")
			return

		for node_index in range(0, len(self._dictOut[x])):
			if self._dictOut[x][node_index] == y:
				del self._dictOut[x][node_index]
				break

		for node_index in range(0, len(self._dictIn[y])):
			if self._dictIn[y][node_index] == x:
				del self._dictIn[y][node_index]
				break

		del self._dictCosts[(x, y)]
		if self._directed == False:
			del self._dictCosts[(y, x)]


	def get_in_and_out_degree(self, vertex_number):
		"""
			Returns the in degree and out degree of a vertex in a tuple.
		"""
		return (len(self._dictIn[vertex_number]), len(self._dictOut[vertex_number]))

	def get_iterator_for_outbound_edges_of_vertex_x(self, vertex_number):
		"""
			Returns an iterator for the outbound edges of vertex "vertex_number".
		"""
		return iter(self._dictOut[vertex_number])

	def get_iterator_for_inbound_edges_of_vertex_x(self, vertex_number):
		"""
			Returns an iterator for the outbound edges of vertex "vertex_number".
		"""
		return iter(self._dictIn[vertex_number])

	def parse_outbound_edges_of_vertex_x(self, vertex_x):
		"""
			Returns a list with all the outbound edges starting from the
			vertex x.
		"""
		iterator = self.get_iterator_for_outbound_edges_of_vertex_x(vertex_x)
		outbound_edges_endpoints = []

		try:
			while True:
				outbound_edges_endpoints.append(next(iterator))
		except StopIteration:
			pass

		return outbound_edges_endpoints

	def parse_inbound_edges_of_vertex_x(self, vertex_x):
		"""
			Returns a list with all the inbound edges startpoints which end
			in the vertex x.
		"""
		iterator = self.get_iterator_for_inbound_edges_of_vertex_x(vertex_x)
		inbound_edges_startpoints = []

		try:
			while True:
				inbound_edges_startpoints.append(next(iterator))
		except StopIteration:
			pass

		return inbound_edges_startpoints

	def retrieve_edge_cost(self, vertex_x, vertex_y):
		"""
			Returns the cost of an edge.
		"""
		return self._dictCosts[(vertex_x, vertex_y)]

	def modify_edge_cost(self, vertex_x, vertex_y, new_cost):
		"""
			Modifies the cost of an edge which is stored in the
			dictCosts dictionary of edges.
		"""
		self._dictCosts[(vertex_x, vertex_y)] = new_cost

	def add_vertex(self, vertex_x):
		"""
			Adds a vertex to the graph.
		"""

		if vertex_x in self.get_vertices():
			print("The vertex already exists!\n")
			return

		self._dictOut[vertex_x] = []
		self._dictIn[vertex_x] = []

	def remove_vertex(self, vertex_x):
		"""
			Removes a vertex from the graph and all the edges associated
			with it.
		"""
		# Removing inbound edges of vertex x from the neighbouring vertices
		for node_index in range(0, len(self._dictIn[vertex_x])):
			for node_index_2 in range(0, len(self._dictOut[self._dictIn[vertex_x][node_index]])):
				if self._dictOut[self._dictIn[vertex_x][node_index]][node_index_2] == vertex_x:
					removed_edge = (
						self._dictIn[vertex_x][node_index], vertex_x)
					del self._dictCosts[removed_edge]
					del self._dictOut[self._dictIn[vertex_x]
									  [node_index]][node_index_2]
					break

		# Removing outbound edges of vertex x from the neighbouring vertices
		for node_index in range(0, len(self._dictOut[vertex_x])):
			for node_index_2 in range(0, len(self._dictIn[self._dictOut[vertex_x][node_index]])):
				if self._dictIn[self._dictOut[vertex_x][node_index]][node_index_2] == vertex_x:
					removed_edge = (
						vertex_x, self._dictOut[vertex_x][node_index])
					del self._dictCosts[removed_edge]
					del self._dictIn[self._dictOut[vertex_x]
									 [node_index]][node_index_2]
					break

		del self._dictOut[vertex_x]
		del self._dictIn[vertex_x]

	def copy(self):
		"""
			Creates a copy of the graph and returns it.
		"""
		copy_of_the_graph = copy.deepcopy(self)
		return copy_of_the_graph

	@staticmethod
	def read_graph_from_text_file(filename, directed):
		"""
			A static method which reads from a file a graph,
			creates it and returns it.
		"""
		f = open(filename, "r")
		lines = f.readlines()

		number_of_nodes = int(lines[0].split()[0])
		number_of_edges = int(lines[0].split()[1])

		graph = DoubleDictGraph(number_of_nodes, directed)
		index = 0

		for line_index in range(1, len(lines)):
			split_line = lines[line_index].strip().split()
			first_node = int(split_line[0])
			second_node = int(split_line[1])
			cost = int(split_line[2])
			graph.add_edge(first_node, second_node, cost)
			if directed == False:
				graph.add_edge(second_node, first_node, cost)

		return graph


	def write_graph_to_text_file(self, file_name):
		"""
			A method which writes to a text file the graph on which
			it is applied.
		"""
		number_of_nodes = self.get_number_of_vertices()
		number_of_edges = 0

		for node in self.get_vertices():
			number_of_edges += len(self._dictOut[node])

		f = open(file_name, "w")

		f.write(str(number_of_nodes))
		f.write(" ")
		f.write(str(number_of_edges))
		f.write("\n")

		for node in range(0, self.get_number_of_vertices()):
			for neighbour_of_node in self._dictOut[node]:
				f.write(str(node))
				f.write(" ")
				f.write(str(neighbour_of_node))
				f.write(" ")
				f.write(str(self._dictCosts[(node, neighbour_of_node)]))
				f.write("\n")

	@staticmethod
	def create_random_graph(number_of_vertices, number_of_edges, directed):
		"""
			Creates a random graph with a certain number of vertices and
			edges and returns it
		"""

		graph = DoubleDictGraph(number_of_vertices, directed)

		for edge in range(0, number_of_edges):
			first_node = random.randrange(0, number_of_vertices)
			second_node = random.randrange(0, number_of_vertices)

			while graph.is_edge(first_node, second_node):
				first_node = random.randrange(0, number_of_vertices)
				second_node = random.randrange(0, number_of_vertices)

			cost = random.randrange(0, 9)
			graph.add_edge(first_node, second_node, cost)

		return graph

	def accessible(self, starting_vertex):
		acc = set()
		acc.add(starting_vertex)
		queue = [starting_vertex]

		while len(queue) > 0:
			x = queue[0]
			queue = queue[1:]

			for y in self.get_outbound_neighbours_of_vertex_X(x):
				if y not in acc:
					#print("{} {}".format(x, y))
					acc.add(y)
					queue.append(y)

		return acc


	def get_the_cost_of_the_spanning_tree(self, starting_node):
		accessed = set()
		accessed.add(starting_node)
		queue = [starting_node]
		cost = 0

		while len(queue) > 0:
			node = queue[0]
			del queue[0]

			for neighbour in self.get_outbound_neighbours_of_vertex_X(node):
				if neighbour not in accessed:
					print("({},{}) with cost {}".format(node, neighbour, self._dictCosts[(node, neighbour)]))
					cost += self._dictCosts[(node, neighbour)]
					queue.append(neighbour)
					accessed.add(neighbour)

		return cost


	def get_connected_components(self):
		components = []
		visited = set()		

		for vertex in self.get_vertices():
			if vertex not in visited:
				component = self.accessible(vertex)	
				visited = visited.union(component)
				components.append(component)
			
		
		return components


	def floyd_warshall(self):
		n = self.get_number_of_vertices()
		m = self._number_of_edges

		cost_matrix = [[0 for x in range(n)] for y in range(n)]
		p = [[0 for x in range(n)] for y in range(n)]

		for x in range(0, n):
			for y in range(0, n):
				if x == y:
					cost_matrix[x][y] = 0
					continue
				try:
					cost_matrix[x][y] = self.retrieve_edge_cost(x, y)
				except KeyError:
					cost_matrix[x][y] = float("inf")	

				if cost_matrix[x][y] != float("inf") and x != y:
					p[x][y] = x
				else:
					p[x][y] = 0

		f = open("warshall_floyd_result.txt", "w")

		for k in range(0, n):
			for i in range(0, n):
				for j in range(0, n):
					if  cost_matrix[i][j] > cost_matrix[i][k] + cost_matrix[k][j]:
						cost_matrix[i][j] = cost_matrix[i][k] + cost_matrix[k][j]
						p[i][j] = p[k][j]

		print("Cost matrix:")
		f.write("Cost matrix:\n")
		for line in cost_matrix:
			for element in line:
				if element == float("inf"):
					print("i", end=" ")
					f.write("i ")
				else:
					print(element, end=" ")
					f.write(str(element))
					f.write(" ")
			print("\n")
			f.write("\n")

		print("Path matrix:")
		f.write("Path matrix:\n")
		for line in p:
			for element in line:
				print(element, end=" ")
				f.write(str(element))
				f.write(" ")
			print("\n")
			f.write("\n")


		x = int(input("Enter the first vertex:"))
		y = int(input("Enter the second vertex:"))

		### Finding the path
		k = n
		u = y
		path = []
		path.append(u)
		while u != x:
			u = p[x][u]
			k -= 1
			path.append(u)

		f.write("The path between {} and {} is:\n".format(x, y))
		f.write(str(list(reversed(path))))
		print(list(reversed(path)))
		f.write("\nIts cost is: ")
		f.write(str(cost_matrix[x][y]))
		print("Cost: ", cost_matrix[x][y])


	def getDictCosts(self):
		return self._dictCosts


	def kruskal(self):
		sets = DisjointSet(self.get_number_of_vertices())
		dictCostsCopy = copy.deepcopy(self._dictCosts)
		dictCostsCopySorted = {k: v for k, v in sorted(dictCostsCopy.items(), key=lambda item: item[1])}
		dictCostsCopySortedWithoutDuplicates = copy.deepcopy(dictCostsCopySorted)

		counter = 0
		for key in dictCostsCopySorted:
			if counter % 2 == 1:
				del dictCostsCopySortedWithoutDuplicates[key]	
			counter += 1

		result = copy.deepcopy(dictCostsCopySortedWithoutDuplicates)

		for key in dictCostsCopySortedWithoutDuplicates:
			if sets.find_set(key[0]) != sets.find_set(key[1]):
				sets.merge_sets(key[0], key[1])
			else:
				del result[key]

		resulting_graph = DoubleDictGraph(self.get_number_of_vertices(), False)	
		for key in result:
			resulting_graph.add_edge(key[0], key[1], self._dictCosts[key])


		print("The number of minimum spanning trees in the graph is ", sets.get_number_of_sets())
		components = resulting_graph.get_connected_components() 

		counter = 1
		for component in components:
			print("Minimum spanning tree #{}".format(counter))
			print(component)
			e = next(iter(component))
			print("The cost of this spanning tree is {}".format(resulting_graph.get_the_cost_of_the_spanning_tree(e)))
			counter += 1