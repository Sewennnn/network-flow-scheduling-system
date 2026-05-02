class Vertex:
    
    def __init__(self,id) -> None:
        """
        This is the init function for my Vertex class.
        
        Written by Choong Yu Xin

        Precondition: id is not None
        Postcondition: After all attributes are initialized, terminate

        Input: the id of the vertex
            
        Return: Nothing to return
            

        Time complexity: 
            Best case analysis: O(1), because i initialise my attributes not according to input size
            Worst case analysis: O(1), because i initialise my attributes not according to input size
        Space complexity: 
            Input space analysis: O(1), because id is integer
            Aux space analysis: O(1), because i initialise my attributes not according to input size
        """
        
        self.id = id
        self.edges= []
        self.discovered = False
        self.visited = False
        self.previous = None



    def add_edge(self, edge):
        """
        This is the function for me to add edges to my vertex.
        
        Written by Choong Yu Xin

        Precondition: edge is not None
        Postcondition: appends edge to my vertex.edges

        Input: edge in form of (u, v, c)
            
        Return: Nothing to return
            

        Time complexity: 
            Best case analysis: O(1), because i append my edge to self.edges
            Worst case analysis: O(1), because i append my edge to self.edges
        Space complexity: 
            Input space analysis: O(1), because my input is an edge in form of (u,v,c)
            Aux space analysis: O(1), because space is not used according to input size
        """
        
        self.edges.append(edge)

    def find_edge(self, v):
        """
        This is the function for me to find a certain edge which links to v.
        
        Written by Choong Yu Xin

        Precondition: v is valid vertex id and is not None
        Postcondition: finds the edge which links this vertex to vertex v

        Input: v which is vertex id
            
        Return: Returns the edge which links this vertex to vertex v

        Time complexity: 
            Best case analysis: O(1), when i find the edge i want imedietly
            Worst case analysis: O(n), where n is length of self.edges, since i loop through self.edges to find the edge i want
        Space complexity: 
            Input space analysis: O(1), because my input is a vertex id
            Aux space analysis: O(1), because  i am looping through self.edges only
        """
        
        for edge in self.edges:
            if edge.v == v:
                return edge
        return None



class Edge:
    
    def __init__(self, u, v, c):
        """
        This is the init function for my Edge class.
        
        Written by Choong Yu Xin

        Precondition: u, v, c is not None
        Postcondition: After all attributes are initialized, terminate

        Input: u,v,c. where u is vertex id, v is another vertex id of next edge, c is capacity of edge
        Example: (2,5,4), i have edge from vertex 2 to vertex 5, with capacity 4
            
        Return: Returns nothing

        Time complexity: 
            Best case analysis: O(1), because i initialise my attributes not according to input size
            Worst case analysis: O(1), because i initialise my attributes not according to input size
        Space complexity: 
            Input space analysis: O(1), where u,v,c are integers
            Aux space analysis: O(1), because i initialise my attributes not according to input size
        """
        
        self.u = u
        self.v = v
        self.c = c
        self.f = 0
        self.forward_edge = None
        self.backward_edge = None
        self.network_edge = None

   
