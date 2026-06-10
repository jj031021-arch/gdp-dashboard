import heapq
from data_store import haversine_distance

def build_adjacency_list(nodes, edges, wheelchair_mode=False):
    """
    Builds an adjacency list representation of the graph.
    Applies weights based on mode.
    """
    adj = {node_id: [] for node_id in nodes}
    
    for u, v, attrs in edges:
        if u not in nodes or v not in nodes:
            continue
            
        # Base physical distance
        lat1, lng1 = nodes[u]["lat"], nodes[u]["lng"]
        lat2, lng2 = nodes[v]["lat"], nodes[v]["lng"]
        dist = haversine_distance(lat1, lng1, lat2, lng2)
        
        # Calculate routing weight
        weight = dist
        has_stairs = attrs.get("has_stairs", False)
        slope = attrs.get("slope", 0)
        has_elevator = attrs.get("has_elevator", False)
        
        if wheelchair_mode:
            # If it has stairs and no elevator, apply a massive penalty (virtually impassable)
            if has_stairs and not has_elevator:
                weight = dist + 10000.0  # Heavy penalty instead of float('inf') to avoid breaking connectivity checks
            
            # Apply penalty for steep slopes
            if slope > 8:
                # Wheelchair ramp limit is usually 1:12 (approx 4.76 degrees). Slope > 8 is very steep.
                weight += dist * (slope * 2.0)
        
        # Since it's a pedestrian graph, it's bidirectional
        adj[u].append((v, weight, dist, attrs))
        adj[v].append((u, weight, dist, attrs))
        
    return adj

def find_shortest_path(nodes, edges, start_node, end_node, wheelchair_mode=False):
    """
    Dijkstra pathfinding algorithm.
    Returns (path_node_ids, total_physical_distance, step_by_step_directions)
    """
    if start_node not in nodes or end_node not in nodes:
        return None, 0.0, []
        
    adj = build_adjacency_list(nodes, edges, wheelchair_mode)
    
    # Priority queue: (current_weight, current_node, path, physical_dist, directions)
    # path is a list of node_ids
    # directions is a list of dicts describing each segment
    queue = [(0.0, start_node, [start_node], 0.0, [])]
    visited = {}
    
    while queue:
        curr_weight, curr_node, path, curr_phys_dist, directions = heapq.heappop(queue)
        
        if curr_node == end_node:
            return path, curr_phys_dist, directions
            
        if curr_node in visited and visited[curr_node] <= curr_weight:
            continue
        visited[curr_node] = curr_weight
        
        for neighbor, edge_weight, edge_dist, attrs in adj[curr_node]:
            new_weight = curr_weight + edge_weight
            
            # Skip if already visited with a better weight
            if neighbor in visited and visited[neighbor] <= new_weight:
                continue
                
            new_path = path + [neighbor]
            new_phys_dist = curr_phys_dist + edge_dist
            
            # Build direction text
            seg_name = attrs.get("name", "Sidewalk segment")
            direction_desc = {
                "from": nodes[curr_node]["name"],
                "to": nodes[neighbor]["name"],
                "action": seg_name,
                "distance": round(edge_dist),
                "has_stairs": attrs.get("has_stairs", False),
                "has_elevator": attrs.get("has_elevator", False),
                "slope": attrs.get("slope", 0)
            }
            new_directions = directions + [direction_desc]
            
            heapq.heappush(queue, (new_weight, neighbor, new_path, new_phys_dist, new_directions))
            
    return None, 0.0, []

def find_nearest_node(nodes, lat, lng):
    """
    Finds the closest node ID in the graph to the given coordinates.
    """
    closest_id = None
    min_dist = float('inf')
    for node_id, coords in nodes.items():
        dist = haversine_distance(lat, lng, coords["lat"], coords["lng"])
        if dist < min_dist:
            min_dist = dist
            closest_id = node_id
    return closest_id
