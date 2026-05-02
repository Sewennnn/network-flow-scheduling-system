from graph import Vertex, Edge
from collections import deque

class FlowNetwork:
    def __init__(self, V):
        """
        This is the init function for my FlowNetwork class.
        
        Written by Choong Yu Xin

        Precondition: V > 0
        Postcondition: After all attributes are initialized, terminate

        Input: V where V is number of vertexes

        Return: Returns nothing

        Time complexity: 
            Best case analysis: O(V), because i initialize array with size V
            Worst case analysis: O(V), because i initialize array with size V
        Space complexity: 
            Input space analysis: O(1), where V is integer
            Aux space analysis: O(V), because i initialize 2 array with size V
        """
        if V <=0:
            raise ValueError("Number of vertices must be positive")
       
        self.flow_network = [None] * (V)
        self.residual_network = [None] * (V)
        for i in range(V):
            self.flow_network[i] = Vertex(i)
            self.residual_network[i] = Vertex(i)
        

    def add_edges(self, argv_edges):
        """
        This is the function to add edges to my networkflow graph and residualnetwork graph.
        
        Written by Choong Yu Xin

        Precondition: argv_edges(param) is not empty, and is a list of tuples consisting of (u,v,w)
        Postcondition: all edges in argv_edges are added to the graphs

        Input: argv_edges is list of edges to be added to the graphs

        Return: Returns nothing

        Time complexity: 
           Best time analysis: O(len(argv_edges)), because you loop for all edge in argv_adges
            Worst time analysis: O(len(argv_edges)), because you loop for all edge in argv_adges

        Space complexity:
            Input space analysis: O(len(argv_edges)) , because i take in a list of tuples and loop through them
            Aux space analysis: O(len(argv_edges)), because i loop through the list of tuples, get each tuple(edge) and append to my new_add_edges
            so my new_add_edges increases linearly to len(argv_edges)
        """
        for edge in argv_edges:
            u, v, c = edge
            # Add to flow network
            current_edge = Edge(u, v, c)
            
            self.flow_network[u].add_edge(current_edge)

            residual_edge = Edge(u, v, c)
            residual_edge.f = c
            residual_backward_edge = Edge(v, u, c)
            residual_edge.reverse_edge = residual_backward_edge
            residual_backward_edge.reverse_edge = residual_edge
            residual_backward_edge.network_edge = current_edge
            self.residual_network[u].add_edge(residual_edge)
            self.residual_network[v].add_edge(residual_backward_edge)


    def reset_graph(self):
        """
        This is the function to reset graph whenever i run bfs for ford fulkerson.
        
        Written by Choong Yu Xin

        Precondition: Graph has vertices 
        Postcondition: All vertices are reset to its original state.(.previous is None, .visited and .discovered is False)

        Input: no Input

        Return: Returns nothing

        Time complexity: 
           Best time analysis: O(V), where V is number of vertices in self.residualnetwork, because you loop through all vertices to reset
            Worst time analysis: O(V), where V is number of vertices in self.residualnetwork, because you loop through all vertices to reset

        Space complexity:
            Input space analysis: O(1) , because there is no input
            Aux space analysis: O(1), because i am reseting vertices only, no extra space required
        """

        for vertex in self.residual_network:
            vertex.previous = None
            vertex.visited = False
            vertex.discovered = False


    def has_augmenting_path(self, source, sink):
        """
        This is the function to find if there is an augmenting path for my residualnetwork.
        
        Written by Choong Yu Xin

        Precondition: Graph has vertices 
        Postcondition: Gives a boolean depending on whether there is a possible path from my source to sink.

        Input: source and sink vertices

        Return: Returns a boolean depending on whether there is a possible path from my source to sink.

        Time complexity: 
           Best time analysis: O(V ), where V is number of vertices in self.residualnetwork, 
            Worst time analysis: O(1), because there are no edges from source, so immedietly return False
            and E is number of all edges in self.residualnetwork, because you traverse all paths to find if there is a possible path from source to sink.

        Space complexity:
            Input space analysis: O(1) , because the input is source and sink id
            Aux space analysis: O(V), where V is number of vertices in self.residualnetwork, because i have queue of maximum V vertices in queue
        """
    
        self.reset_graph()
        
        queue = deque()
        queue.append(source)
        source.discovered = True
        
        while len(queue) > 0:
            u = queue.popleft()
            u.visited = True
            u.discovered = True
            for edge in u.edges:
                if edge.f > 0:
                    v = edge.v
                    v = self.residual_network[v]
                    if not v.visited and edge.f > 0:
                        v.previous = u
                        queue.append(v)
                        v.discovered = True
                        if v.id == sink.id:
                            return True
        return False
    
    def backtracking(self, source, sink):
        """
        This is the function to backtrack to find the path for my traverse from source to sink.
        
        Written by Choong Yu Xin

        Precondition: source and sink is valid vertexes
        Postcondition: Gives the path to reach sink from source

        Input: source and sink vertexes

        Return: Returns the path to reach sink from source

        Time complexity: 
           Best time analysis: O(N), where N is length of path from source to sink 
            Worst time analysis: O(N), where N is length of path from source to sink 

        Space complexity:
            Input space analysis: O(1) , because the input is source and sink id
            Aux space analysis: O(N), where N is length of path from source to sink 
        """
        vertex = sink
        path = []

        while vertex.previous is not None:
            path.append(vertex)
            vertex = vertex.previous 

        path.append(source)
        path.reverse()

        print_path = []

        for vertex in path:
            print_path.append(vertex.id)


        return path


    def fordfulkerson(self, source, sink):
        """
        This is the ford fulkerson function which returns the maximum possible flow in the network flow.
        
        Written by Choong Yu Xin

        Precondition: source and sink is valid vertexes
        Postcondition: Gives the maximum flow from source to sink

        Input: source and sink vertex id

        Return: Returns the maximum possible flow in the network flow

        Time complexity: 
            Best time analysis: O(1), when there is immedietly no paths and max flow is 0 is returned
            Worst time analysis: O(V * E^2), where V is the number of vertices and E is the number of edges
       

        Space complexity:
            Input space analysis: O(1) , because the input is source and sink id
            Aux space analysis: O(V), where V is number of vertices
        """
        start = self.residual_network[source]
        end = self.residual_network[sink]
        
        max_flow = 0
        
     
        while self.has_augmenting_path(start, end):
            path = self.backtracking(start, end) 
            min_flow = float('inf')

            for i in range(len(path) - 1):
                u = path[i].id
                v = path[i + 1].id
                edge = self.residual_network[u].find_edge(v)    
                min_flow = min(min_flow, edge.f)
        
        
            for i in range(len(path) - 1):
                u = path[i].id
                v = path[i + 1].id
                edge = self.residual_network[u].find_edge(v)
                reverse_edge = edge.reverse_edge
                edge.f -= min_flow
                reverse_edge.f += min_flow
                network_edge = edge.network_edge
                if network_edge is None:
                    network_edge = reverse_edge.network_edge
                    network_edge.f += min_flow

                else:
                    network_edge.f -= min_flow

        

            max_flow += min_flow

        return max_flow
            

