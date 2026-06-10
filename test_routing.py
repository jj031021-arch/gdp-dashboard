import sys
import os

# Adjust path to import data_store and router
sys.path.append(os.path.dirname(__file__))

from data_store import load_network_graph
from router import find_shortest_path

def test_gangnam_routing():
    print("Testing Gangnam Area Routing...")
    nodes, edges = load_network_graph("Gangnam")
    
    # Target: From platform to a POI on the south street (near Twosome Cafe)
    # The concourse connects to Exit 2 (stairs) and Exit 8 (elevator/ramp) and Exit 12 (elevator)
    start_node = "G_platform"
    end_node = "G_street_south_1"
    
    # 1. Test Standard Route (Stairs allowed)
    path_std, dist_std, dirs_std = find_shortest_path(nodes, edges, start_node, end_node, wheelchair_mode=False)
    
    # 2. Test Wheelchair Accessible Route (Stairs penalized/avoided)
    path_wc, dist_wc, dirs_wc = find_shortest_path(nodes, edges, start_node, end_node, wheelchair_mode=True)
    
    # Verification
    print(f"Standard Path: {' -> '.join(path_std)}")
    print(f"Standard Distance: {dist_std:.1f}m")
    has_stairs_std = any(step["has_stairs"] for step in dirs_std)
    print(f"Standard Path has stairs: {has_stairs_std}")
    
    print(f"Wheelchair Path: {' -> '.join(path_wc)}")
    print(f"Wheelchair Distance: {dist_wc:.1f}m")
    has_stairs_wc = any(step["has_stairs"] for step in dirs_wc)
    print(f"Wheelchair Path has stairs: {has_stairs_wc}")
    
    # Assertions
    assert path_std is not None, "Should find standard path"
    assert path_wc is not None, "Should find wheelchair path"
    assert has_stairs_std == True, "Standard path from platform to South Street should use stairs (Exit 2 is direct/stairs)"
    assert has_stairs_wc == False, "Wheelchair path MUST NOT contain any stair segments!"
    assert dist_wc >= dist_std, "Wheelchair path should be equal or longer due to detour via elevator"
    
    print("[SUCCESS] Gangnam Routing Test Passed!")

def test_seoul_station_routing():
    print("\nTesting Seoul Station Area Routing...")
    nodes, edges = load_network_graph("Seoul Station")
    
    # Target: From platform to Namdaemun Market entry lane
    # Concourse connects to Exit 2 (stairs), Exit 4 (stairs), Exit 9 (elevator)
    start_node = "S_platform"
    end_node = "S_poi_namdaemun_lane"
    
    path_std, dist_std, dirs_std = find_shortest_path(nodes, edges, start_node, end_node, wheelchair_mode=False)
    path_wc, dist_wc, dirs_wc = find_shortest_path(nodes, edges, start_node, end_node, wheelchair_mode=True)
    
    has_stairs_std = any(step["has_stairs"] for step in dirs_std)
    has_stairs_wc = any(step["has_stairs"] for step in dirs_wc)
    
    print(f"Standard Path: {' -> '.join(path_std)}")
    print(f"Standard Distance: {dist_std:.1f}m. Stairs: {has_stairs_std}")
    
    print(f"Wheelchair Path: {' -> '.join(path_wc)}")
    print(f"Wheelchair Distance: {dist_wc:.1f}m. Stairs: {has_stairs_wc}")
    
    assert path_std is not None
    assert path_wc is not None
    assert has_stairs_wc == False, "Wheelchair path must avoid all stairs!"
    
    print("[SUCCESS] Seoul Station Routing Test Passed!")

if __name__ == "__main__":
    try:
        test_gangnam_routing()
        test_seoul_station_routing()
        print("\n[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        sys.exit(1)
