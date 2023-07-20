

def generate_graph(output_name, module_name, node_ids, edges):

    with open(output_name, "w") as out:
    
        out.write("""
        #include <boost/config.hpp>
        #include <boost/python.hpp>
        #include <iostream>
        #include <fstream>
    
        #include <boost/graph/graph_traits.hpp>
        #include <boost/graph/adjacency_list.hpp>
        #include <boost/graph/dijkstra_shortest_paths.hpp>
        #include <boost/property_map/property_map.hpp>
    
    
        using namespace boost;
    
    
        // create a typedef for the Graph type
        typedef adjacency_list< vecS, vecS, undirectedS, no_property,
        property< edge_weight_t, int > > graph_t;
    
        typedef graph_traits< graph_t >::vertex_descriptor vertex_descriptor;
        typedef std::pair< int, int > Edge;
    
    
        int getIndex(std::vector<std::string>, std::string);
        graph_t buildGraph();
    
    
        """)
    
        
        out.write(f"const int num_nodes = {len(node_ids)};\n\n")
        out.write("enum nodes {\n")
        for node_id in node_ids:
            out.write(f"    {node_id},\n")
                  
        out.write("};\n\n")
    
        out.write('std::string _name[] = {')
        for node_id in node_ids:
            if node_id != node_ids[-1]:
                out.write(f'"{str(node_id)}",')
            else:
                out.write(f'"{str(node_id)}"')
        out.write('};\n')
    
        out.write("std::vector<std::string> name(_name, _name + sizeof(_name)/sizeof(std::string));\n\n")
        
        out.write("Edge edge_array[] = {\n")
        
        for edge in edges:
            if edge != edges[-1]:
                out.write(f"    Edge({edge.start_id}, {edge.end_id}),\n")
            else:
                out.write(f"    Edge({edge.start_id}, {edge.end_id})\n")
    
        out.write("};\n\n")
    
        out.write("float weights[] = {")
        for edge in edges:
            if edge != edges[-1]:
                out.write(f"{edge.distance}, ")
            else:
                out.write(f"{edge.distance}")
        out.write("};\n")
    
        out.write("""
    
    std::string get_route(std::string start, std::string end) {
      graph_t graph = buildGraph();
      
      property_map< graph_t, edge_weight_t >::type weightmap = get(edge_weight, graph);
      std::vector< vertex_descriptor > p(num_vertices(graph));
      std::vector< int > d(num_vertices(graph));
          
      int pos_start = getIndex(name, start);
      int pos_end = getIndex(name, end);
    
      if (pos_start == -1) {
        std::string msg("Invalid id (not found) for start position");
        throw std::invalid_argument(msg);
      } else if (pos_end == -1) {
        std::string msg("Invalid id (not found) for end position");
        throw std::invalid_argument(msg);
      }
      
      vertex_descriptor s = vertex(nodes(pos_start), graph);
      vertex_descriptor e = vertex(nodes(pos_end), graph);
    
      dijkstra_shortest_paths(graph, s,
         predecessor_map(boost::make_iterator_property_map(
                                p.begin(), get(boost::vertex_index, graph)))
                .distance_map(boost::make_iterator_property_map(
                    d.begin(), get(boost::vertex_index, graph))));
          
          //find path from start to end vertex
      std::list<vertex_descriptor> pathVertices;
      
      int distance = d[e];
      while (e != s)
        {
          pathVertices.push_front(e);
          if(name[e] == name[p[e]]) // see https://stackoverflow.com/questions/48367649/boost-dijkstra-shortest-paths-cant-extract-or-find-the-path-path-contains
            break; 
          e = p[e];
        }

    pathVertices.push_front(s); // add starting point to path
    
    
      std::string path;
    
      for (vertex_descriptor n : pathVertices) {
        path += name[n];
        path += " ";
      }
    
      path += ":";
      path += std::to_string(distance);
          
      return path;
    
    }
    
    graph_t buildGraph() {
    
      int num_arcs = sizeof(edge_array) / sizeof(Edge);
      
      graph_t g(edge_array, edge_array + num_arcs, weights, num_nodes);
      
      return g;
    }
    
    int getIndex(std::vector<std::string> v, std::string element)
    {
        auto it = find(v.begin(), v.end(), element);
     
        // If element was found
        if (it != v.end())
        {
         
            // calculating the index
            // of element
            int index = it - v.begin();
    	//std::cout << index << std::endl;
    	return index;
        }
        else {
            // If the element is not
            // present in the vector
    	return -1;
        }
    }
    
    """)
    
        out.write(f"BOOST_PYTHON_MODULE({module_name}) // module name must match the name of the .so compiled")
        out.write("""
        {
        using namespace boost::python;
        def("get_route", get_route);
        }
    
        """)
    
