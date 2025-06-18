import numpy as np
import networkx as nx
from collections import defaultdict
import time

def create_elevation_graph(elevation_array, max_size=None):
    """
    Create a graph from elevation data where each cell is a node
    and edges connect to 4-neighbors (no diagonal connections, no wrap-around)
    
    Args:
        elevation_array: 2D numpy array of elevation values
        max_size: Optional tuple (max_rows, max_cols) to limit graph size for testing
    
    Returns:
        NetworkX Graph object
    """
    print("Creating graph from elevation data...")
    
    # Get array dimensions
    rows, cols = elevation_array.shape
    
    # Optionally limit size for testing with large arrays
    if max_size:
        rows = min(rows, max_size[0])
        cols = min(cols, max_size[1])
        elevation_array = elevation_array[:rows, :cols]
        print(f"Limited to {rows}x{cols} for testing")
    
    print(f"Processing {rows}x{cols} = {rows*cols:,} nodes")
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes with elevation data
    print("Adding nodes...")
    for i in range(rows):
        for j in range(cols):
            node_id = i * cols + j  # Convert 2D coordinates to 1D node ID
            elevation = elevation_array[i, j]
            G.add_node(node_id, 
                      row=i, 
                      col=j, 
                      elevation=elevation,
                      pos=(j, -i))  # Position for visualization (j=x, -i=y for proper orientation)
    
    # Add edges to 4-connected neighbors
    print("Adding edges...")
    edge_count = 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for i in range(rows):
        for j in range(cols):
            current_node = i * cols + j
            current_elevation = elevation_array[i, j]
            
            # Check each of the 4 neighbors
            for di, dj in directions:
                ni, nj = i + di, j + dj
                
                # Check bounds (no wrap-around)
                if 0 <= ni < rows and 0 <= nj < cols:
                    neighbor_node = ni * cols + nj
                    neighbor_elevation = elevation_array[ni, nj]
                    
                    # Add edge if it doesn't exist (undirected graph)
                    if not G.has_edge(current_node, neighbor_node):
                        # Calculate elevation difference
                        elevation_diff = abs(current_elevation - neighbor_elevation)
                        
                        G.add_edge(current_node, neighbor_node,
                                 weight=elevation_diff,
                                 distance=1)  # Each cell is 1 unit apart
                        edge_count += 1
    
    print(f"Graph created with {G.number_of_nodes():,} nodes and {G.number_of_edges():,} edges")
    return G

def analyze_graph(G):
    """Analyze basic properties of the graph"""
    print("\n=== Graph Analysis ===")
    print(f"Nodes: {G.number_of_nodes():,}")
    print(f"Edges: {G.number_of_edges():,}")
    print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    
    # Get elevation statistics
    elevations = [G.nodes[node]['elevation'] for node in G.nodes()]
    print(f"Elevation range: {min(elevations)} to {max(elevations)} meters")
    
    # Check connectivity
    print(f"Is connected: {nx.is_connected(G)}")
    if not nx.is_connected(G):
        components = list(nx.connected_components(G))
        print(f"Number of connected components: {len(components)}")
        print(f"Largest component size: {len(max(components, key=len))}")

def save_graph_sample(G, sample_size=100):
    """Save a small sample of the graph for visualization"""
    print(f"\nSaving sample of {sample_size} nodes for visualization...")
    
    # Get a random sample of nodes
    sample_nodes = list(G.nodes())[:sample_size]
    subgraph = G.subgraph(sample_nodes)
    
    # Save as GraphML for easy loading in other tools
    nx.write_graphml(subgraph, "elevation_graph_sample.graphml")
    print("Sample saved as: elevation_graph_sample.graphml")

if __name__ == "__main__":
    # Load elevation data
    print("Loading elevation data...")
    elevation = np.load('elevation_data.npy')
    
    # For testing, let's start with a smaller portion
    # Remove this line to process the full array (warning: will be very large!)
    test_size = (100, 100)  # 10,000 nodes, ~20,000 edges
    
    start_time = time.time()
    
    # Create graph
    G = create_elevation_graph(elevation, max_size=test_size)
    
    # Analyze the graph
    analyze_graph(G)
    
    # Save sample for visualization
    save_graph_sample(G, sample_size=min(100, G.number_of_nodes()))
    
    # Save full graph (for small test sizes)
    if G.number_of_nodes() <= 10000:
        print("\nSaving full graph...")
        nx.write_gpickle(G, "elevation_graph.pkl")
        print("Full graph saved as: elevation_graph.pkl")
    
    elapsed = time.time() - start_time
    print(f"\nTotal processing time: {elapsed:.2f} seconds")
    
    print(f"\nGraph object 'G' is ready to use!")
    print("Example usage:")
    print("  - G.nodes[0] to see node 0 attributes")
    print("  - G.edges(data=True) to see edges with weights")
    print("  - nx.shortest_path(G, source, target) for pathfinding")