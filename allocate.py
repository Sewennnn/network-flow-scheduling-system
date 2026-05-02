from graph import Vertex, Edge
from collections import deque
from flow_network import FlowNetwork

def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
        This is the allocate function which returns allocation list of officers, or None if the company demand cannot be satisfied.
        In my function, i preprocess everything and convert the information into a network flow graph, then run ford fulkerson to 
        check if the flow meets the demand. Then, i traverse through the network flow to look for the information, then append it into my allocation list.
        
        Written by Choong Yu Xin

        Precondition: preferences, officers_per_org, min and max_shifts is not None
        Postcondition: gives a list of allocation

        Input: A list of preferences of officers(preferences), A list of officers needed per organisation(officers_per_org), the min shifts and max shifts a officer can do.

        Return: Returns the allocation list of officers of a month, or None if the company demand cannot be satisfied.

        Time complexity: 
            Best time analysis: O(M), where M is number of companies, 
            since i can return None early if the officers needed by organisation is greater than officers on hand
            Worst time analysis: O(M * N * N), where M is number of companies, and N is number of officers
       
        Space complexity:
            Input space analysis: O(N+M), where M is number of companies, and N is number of officers
            Aux space analysis: O(N * M), where M is number of companies, and N is number of officers
        """
    
    days = 30
   
    num_officers = len(preferences)
    num_companies = len(officers_per_org)
    num_shifts = 3
    
    shift_list = [0] * (days * num_shifts)

    for org in range(num_companies):
        for day in range(days):
            for shift in range(num_shifts):
                shift_index = day * num_shifts + shift
               
                shift_list[shift_index] += officers_per_org[org][shift]

    for org in range(num_companies):
        for shift in range(num_shifts):
            officers_needed = officers_per_org[org][shift] * 30
            officers_per_org[org][shift] = officers_needed


    x_demand = (-(sum(shift_list))+ (num_officers * min_shifts))
  
    
    if x_demand > 0:
        return None
    
    
    total_vertices = (days * num_shifts * num_officers) + num_officers  + (num_officers * days) + 1 + 1 + 1
    

    source = 0
    sink = total_vertices - 1
    network = FlowNetwork(total_vertices)

    edges = []

    if x_demand != 0:
        edges.append((source, total_vertices -2 , -(x_demand)))

    
    for i in range(num_officers):
        edges.append((source, i + 1, min_shifts))
        
        edges.append((total_vertices-2, i+1, max_shifts - min_shifts))

        for n in range(days):
            edges.append((i + 1, num_officers + n + 1 + i * 30, 1))
            
            for x in range(num_shifts):
                if preferences[i][x] == 1: 
                    edges.append((num_officers + n + 1 + i * days, num_officers + num_officers * days + (n * num_shifts + x + 1) + (i * days * num_shifts), 1))
    
    
    start_index = num_officers + num_officers * days + 1
    
    for i in range(start_index, num_officers + num_officers * days + num_officers * days * num_shifts + 1):
        for day in range(days):
            for shift in range(num_shifts):
                shift_index = day * num_shifts + shift
                
        edges.append((i, sink, shift_list[shift_index]))
  

    network.add_edges(edges)
   

    max_flow = network.fordfulkerson(source, sink)

    
    if max_flow < (sum(shift_list) ):
        return None


    allocation = [
        [
            [
                [0 for _ in range(num_shifts)] 
                for _ in range(days)
            ]
            for _ in range(num_companies)
        ]
        for _ in range(num_officers)
    ]


    officers_range = num_officers

    for officer in range(1, officers_range + 1):
     
        vertex = network.flow_network[officer]
        for edge in vertex.edges:
            if edge.f > 0:
                v = edge.v
                day = (v - (num_officers + 1))% days
                
                vertex = network.flow_network[v]
                for j in vertex.edges:
                    if j.f > 0:
                        v = j.v
                        vertex = network.flow_network[v]
                        
                        dayshift = (v - (num_officers + num_officers * days + 1)) % ( num_shifts ) 
                    
                        for c in range(num_companies):
                            if officers_per_org[c][dayshift] > 0:
                                allocation[officer-1][c][day][dayshift] = 1
                                officers_per_org[c][dayshift] -= 1
                                break


    return allocation

