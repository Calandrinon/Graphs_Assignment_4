from graph import DoubleDictGraph


class Menu:

    def __init__(self):
        self.filename = "graph1k.txt"
        self.running = True


    def exit(self):
        self.running = False


    def print_graph(self): 
        for node in self.graph.get_vertices():
            line = str(node) + ":"

            for neighbour in self.graph.get_outbound_neighbours_of_vertex_X(node):
                line += str(neighbour) + "  "

            print(line)


    def print_menu(self):
        print("""		
        1. get the number of vertices;
        2. parse (iterate) the set of vertices;
        3. given two vertices, find out whether there is an edge from the first one to the second one, and retrieve the Edge_id if there is an edge (the latter is not required if an edge is represented simply as a pair of vertex identifiers);
        4. get the in degree and the out degree of a specified vertex;
        5. parse (iterate) the set of outbound edges of a specified vertex (that is, provide an iterator). For each outbound edge, the iterator shall provide the Edge_id of the curren edge (or the target vertex, if no Edge_id is used).
        6. parse the set of inbound edges of a specified vertex (as above);
        7. retrieve or modify the information (the integer) attached to a specified edge.
        8. The graph shall be modifiable: it shall be possible to add and remove an edge, and to add and remove a vertex. Think about what should happen with the properties of existing edges and with the identification of remaining vertices. You may use an abstract Vertex_id instead of an int in order to identify vertices; in this case, provide a way of iterating the vertices of the graph.
        9. Read the graph from a text file (as an external function); see the format below.
        10. Write the graph to a text file (as an external function); see the format below.
        11.Create a random graph with specified number of vertices and of edges (as an external function). 
        12.Get the connected components of the graph.
        13. Restart graph
        14. Find the lowest cost walks with Floyd-Warshall
        15. Find the minimum spanning tree of the graph
        0. Exit the program
        """)


    def clear_screen(self):
        print("\n"*100)


    def num_of_vertices(self):
        print("There are ", self.graph.get_number_of_vertices(), " vertices in the graph.") 


    def parse_set_of_vertices(self):
        for vertex in self.graph.get_vertices():
            print(vertex, end=" ")


    def is_edge_between_vertices(self):
        vertex1 = int(input("Enter the first vertex: "))
        vertex2 = int(input("Enter the second vertex: "))

        if self.graph.is_edge(vertex1, vertex2):
            print("There is an edge between {} and {} with the cost {}".format(vertex1, vertex2, self.graph.retrieve_edge_cost(vertex1, vertex2)))
        else: 
            print("There is no edge between {} and {}!\n".format(vertex1, vertex2))


    def in_degree_out_degree(self): 
        vertex = int(input("Enter the vertex number:"))
        degrees = self.graph.get_in_and_out_degree(vertex)
        print("The in and out degree of the vertex are {}".format(str(degrees)))


    def outbound_edges(self):
        vertex = int(input("Specify the vertex: "))
        for neighbour in self.graph.get_outbound_neighbours_of_vertex_X(vertex):
            print(neighbour, " ")
        print("\n")


    def inbound_edges(self):
        vertex = int(input("Specify the vertex: "))
        for neighbour in self.graph.get_inbound_neighbours_of_vertex_X(vertex):
            print(neighbour, " ")
        print("\n")


    def retrieve_modify(self):
        first_vertex = int(input("Enter the first vertex of the edge: "))
        second_vertex = int(input("Enter the second vertex of the edge: "))

        print("1. Retrieve cost of the edge")
        print("2. Modify cost of the edge")

        option = int(input("Enter option: "))

        if option == 1:
            try:
                print(self.graph.retrieve_edge_cost(first_vertex, second_vertex))
            except KeyError as ke:
                print("The edge {} does not exist!".format(ke))
        else:
            try:
                new_cost = int(input("Enter the new cost of edge {}: ".format(str((first_vertex, second_vertex)))))
                self.graph.modify_edge_cost(first_vertex, second_vertex, new_cost)
            except KeyError as ke:
                print("The edge {} does not exist!".format(ke))


    def add_remove_vertex_edge(self):
        self.clear_screen()
        print("""
               1. Add a new vertex
               2. Remove a vertex
               3. Add a new edge
               4. Remove edge
                """)
        option = int(input("Enter an option:"))
        if option == 1:
            new_vertex = int(input("Enter the vertex number:"))
            self.graph.add_vertex(new_vertex)
        elif option == 2:
            removed_vertex = int(input("Enter the vertex number to remove:"))
            self.graph.remove_vertex(removed_vertex)
        elif option == 3:
            first_vertex = int(input("Enter the first vertex:"))
            second_vertex = int(input("Enter the second vertex:"))
            cost = int(input("Enter the cost:"))

            self.graph.add_edge(first_vertex, second_vertex, cost)
        elif option == 4:
            first_vertex = int(input("Enter the first vertex:"))
            second_vertex = int(input("Enter the second vertex:"))

            self.graph.remove_edge(first_vertex, second_vertex)


    def read_graph(self):
        self.filename = input("Enter the input filename of the graph:")
        self.graph = DoubleDictGraph.read_graph_from_text_file(self.filename, self._directed) 
        self.clear_screen()
		

    def write_graph(self):
        filename = input("Enter the filename of the output file:")
        self.graph.write_graph_to_text_file(filename)


    def random_graph(self):
        vertices = int(input("Enter the number of vertices:")) 
        edges = int(input("Enter the number of edges:")) 

        if edges > vertices * (vertices-1):
            print("The number of edges should be max. n*(n-1), where n is the number of vertices. ")
            return

        self.graph = DoubleDictGraph.create_random_graph(vertices, edges, self._directed) 
	
	
    def get_connected_components(self):
        print(self.graph.get_connected_components())		


    def restart_graph(self):
        number_of_nodes = int(input("Enter the number of nodes: "))

        self.graph = DoubleDictGraph(number_of_nodes, self._directed) 

    
    def fw(self):
        self.graph.floyd_warshall()        

    
    def kruskal(self):
        self.graph.kruskal()


    def main(self):
        print("\n\n")
        self._directed = True 

        print("1. Directed")
        print("2. Undirected")
        option = int(input("Enter an option: "))
        if option == 1:
            self._directed = True
        else:
            self._directed = False
		
				
        self.graph = DoubleDictGraph.read_graph_from_text_file(self.filename, self._directed)


        options = [self.exit, self.num_of_vertices, self.parse_set_of_vertices, self.is_edge_between_vertices,
                self.in_degree_out_degree, self.outbound_edges, self.inbound_edges, self.retrieve_modify, 
                self.add_remove_vertex_edge, self.read_graph, self.write_graph, self.random_graph, self.get_connected_components, self.restart_graph,
                self.fw, self.kruskal]

        print("\n\n")
        self.clear_screen()
        while self.running:
            self.print_menu()

            try:
                option = int(input("Enter an option: "))
                self.clear_screen()

                options[option]()
            except ValueError as ve:
                self.clear_screen()
                print(ve)
            except Exception as e:
                print(e)
            

        self.graph.write_graph_to_text_file("result.txt")
        
menu = Menu()
menu.main()
