import json
import os
import math
# File path for crowd-sourced reports
REPORTS_FILE = os.path.join(os.path.dirname(__file__), "crowd_reports.json")
# 1. Subway Exits Accessibility Database
SUBWAY_EXITS = {
    "Gangnam": [
        {"exit": "Exit 1", "lat": 37.4983, "lng": 127.0284, "has_elevator": True, "details": "Elevator located outside Exit 1 (next to tax office entrance)."},
        {"exit": "Exit 2", "lat": 37.4975, "lng": 127.0282, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 1 (80m) or Exit 12 (120m)."},
        {"exit": "Exit 3", "lat": 37.4971, "lng": 127.0283, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 1 (140m)."},
        {"exit": "Exit 4", "lat": 37.4965, "lng": 127.0281, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 1 (220m)."},
        {"exit": "Exit 5", "lat": 37.4962, "lng": 127.0270, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 8 (180m)."},
        {"exit": "Exit 6", "lat": 37.4967, "lng": 127.0264, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 8 (120m)."},
        {"exit": "Exit 7", "lat": 37.4972, "lng": 127.0262, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 8 (70m)."},
        {"exit": "Exit 8", "lat": 37.4978, "lng": 127.0264, "has_elevator": True, "details": "Elevator located inside the building block at Exit 8 (connected to Kyobo Tower path)."},
        {"exit": "Exit 9", "lat": 37.4984, "lng": 127.0262, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 8 (80m) or Exit 12 (210m)."},
        {"exit": "Exit 10", "lat": 37.4988, "lng": 127.0269, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 12 (160m)."},
        {"exit": "Exit 11", "lat": 37.4990, "lng": 127.0278, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 12 (90m)."},
        {"exit": "Exit 12", "lat": 37.4987, "lng": 127.0285, "has_elevator": True, "details": "Elevator located behind Exit 12, near Asem Tower direction."}
    ],
    "Seoul Station": [
        {"exit": "Exit 1", "lat": 37.5538, "lng": 126.9696, "has_elevator": True, "details": "Elevator located next to the main entrance of Lotte Outlets."},
        {"exit": "Exit 2", "lat": 37.5545, "lng": 126.9688, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 1 (90m)."},
        {"exit": "Exit 3", "lat": 37.5558, "lng": 126.9715, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 9 (140m)."},
        {"exit": "Exit 4", "lat": 37.5562, "lng": 126.9722, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 9 (160m)."},
        {"exit": "Exit 9", "lat": 37.5548, "lng": 126.9718, "has_elevator": True, "details": "Elevator connected directly to Seoul Square building basement lobby."},
        {"exit": "Exit 10", "lat": 37.5535, "lng": 126.9726, "has_elevator": False, "details": "Stairs only. Nearest elevator is Exit 9 (180m)."},
        {"exit": "Exit 14", "lat": 37.5520, "lng": 126.9715, "has_elevator": True, "details": "Elevator located near the taxi stand at Exit 14."}
    ]
}
# 2. Points of Interest (POIs) Accessibility Database
POIS = [
    # Gangnam Area
    {
        "id": "poi_g1",
        "area": "Gangnam",
        "name": "Kakao Friends Gangnam Flagship Store",
        "category": "Shop",
        "lat": 37.4985,
        "lng": 127.0272,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 5,
        "description": "Double automatic doors, flat threshold entrance. Spaced layout inside, wheelchair friendly elevator to upper floors."
    },
    {
        "id": "poi_g2",
        "area": "Gangnam",
        "name": "Shake Shack Gangnam",
        "category": "Restaurant",
        "lat": 37.5023,
        "lng": 127.0255,
        "has_ramp": True,
        "has_elevator": False,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 4.5,
        "description": "Accessible ramp on the right side of the main entrance. Wide sliding doors and tables suitable for wheelchairs."
    },
    {
        "id": "poi_g3",
        "area": "Gangnam",
        "name": "Gangnam Traditional K-BBQ",
        "category": "Restaurant",
        "lat": 37.4995,
        "lng": 127.0290,
        "has_ramp": False,
        "has_elevator": False,
        "accessible_toilet": False,
        "entrance_width_ok": False,
        "score": 1.5,
        "description": "3 large concrete steps at the entry door. Tight layout inside, heavy smoke hood poles make wheelchair passage difficult."
    },
    {
        "id": "poi_g4",
        "area": "Gangnam",
        "name": "Starbucks Gangnam R",
        "category": "Cafe",
        "lat": 37.4978,
        "lng": 127.0286,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 4.8,
        "description": "Stepless street entrance. Dedicated elevator inside for basement and upper floor seating. Well-maintained accessible toilet."
    },
    {
        "id": "poi_g5",
        "area": "Gangnam",
        "name": "A Twosome Place Gangnam",
        "category": "Cafe",
        "lat": 37.4963,
        "lng": 127.0280,
        "has_ramp": False,
        "has_elevator": False,
        "accessible_toilet": False,
        "entrance_width_ok": True,
        "score": 2.0,
        "description": "Has a 15cm high threshold step at the entrance. Inside is spacious, but entrance remains inaccessible without assistance."
    },
    {
        "id": "poi_g6",
        "area": "Gangnam",
        "name": "Olive Young Gangnam Town",
        "category": "Shop",
        "lat": 37.5015,
        "lng": 127.0259,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": False,
        "entrance_width_ok": True,
        "score": 4.2,
        "description": "Very wide sliding automatic doors. Smooth floors and wide aisles. Elevator available to access 2nd and 3rd floors."
    },
    {
        "id": "poi_g7",
        "area": "Gangnam",
        "name": "Gangnam Square (Plaza)",
        "category": "Tourist Attraction",
        "lat": 37.4979,
        "lng": 127.0276,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 5.0,
        "description": "Open plaza near Exit 11 & 12. Flat pavement, outdoor seating zones, completely barrier-free area."
    },
    
    # Seoul Station Area
    {
        "id": "poi_s1",
        "area": "Seoul Station",
        "name": "Lotte Outlets Seoul Station",
        "category": "Shop",
        "lat": 37.5539,
        "lng": 126.9693,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 5.0,
        "description": "Fully accessible department store. Direct elevator connections to parking lot and Seoul Station platform lobby."
    },
    {
        "id": "poi_s2",
        "area": "Seoul Station",
        "name": "Culture Station Seoul 284",
        "category": "Tourist Attraction",
        "lat": 37.5553,
        "lng": 126.9710,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 4.5,
        "description": "Historical building. Main front entrance has stairs, but a wheelchair ramp is located at the right-side entrance."
    },
    {
        "id": "poi_s3",
        "area": "Seoul Station",
        "name": "Seoul Station Plaza",
        "category": "Tourist Attraction",
        "lat": 37.5546,
        "lng": 126.9708,
        "has_ramp": True,
        "has_elevator": True,
        "accessible_toilet": True,
        "entrance_width_ok": True,
        "score": 5.0,
        "description": "Spacious flat asphalt plaza. Fully accessible, integrates pathways to subway elevator entrances."
    },
    {
        "id": "poi_s4",
        "area": "Seoul Station",
        "name": "Namdaemun Market Accessible Lane",
        "category": "Tourist Attraction",
        "lat": 37.5592,
        "lng": 126.9765,
        "has_ramp": True,
        "has_elevator": False,
        "accessible_toilet": False,
        "entrance_width_ok": True,
        "score": 3.0,
        "description": "Main road of the market has flat pavement but is highly crowded. Side alleys contain steep stairs and steps."
    },
    {
        "id": "poi_s5",
        "area": "Seoul Station",
        "name": "Old Station Tavern",
        "category": "Restaurant",
        "lat": 37.5528,
        "lng": 126.9720,
        "has_ramp": False,
        "has_elevator": False,
        "accessible_toilet": False,
        "entrance_width_ok": False,
        "score": 1.2,
        "description": "Traditional pub with high steps at entrance. Narrow aisles packed with heavy wooden tables. Inaccessible."
    }
]
# 3. Routing Graph Data
# Nodes around Gangnam Station
GANGNAM_NODES = {
    "G_platform": {"lat": 37.4979, "lng": 127.0276, "name": "Gangnam Subway Platform (B2)"},
    "G_concourse": {"lat": 37.4979, "lng": 127.0276, "name": "Gangnam Ticket Concourse (B1)"},
    
    # Exits
    "G_exit_1": {"lat": 37.4983, "lng": 127.0284, "name": "Gangnam Exit 1 (Elevator)"},
    "G_exit_2": {"lat": 37.4975, "lng": 127.0282, "name": "Gangnam Exit 2 (Stairs)"},
    "G_exit_8": {"lat": 37.4978, "lng": 127.0264, "name": "Gangnam Exit 8 (Elevator)"},
    "G_exit_11": {"lat": 37.4990, "lng": 127.0278, "name": "Gangnam Exit 11 (Stairs)"},
    "G_exit_12": {"lat": 37.4987, "lng": 127.0285, "name": "Gangnam Exit 12 (Elevator)"},
    
    # Street Sidewalks (North-East-South-West Intersections)
    "G_sidewalk_ne": {"lat": 37.4982, "lng": 127.0280, "name": "Northeast Sidewalk Intersection"},
    "G_sidewalk_se": {"lat": 37.4976, "lng": 127.0279, "name": "Southeast Sidewalk Intersection"},
    "G_sidewalk_sw": {"lat": 37.4976, "lng": 127.0271, "name": "Southwest Sidewalk Intersection"},
    "G_sidewalk_nw": {"lat": 37.4982, "lng": 127.0270, "name": "Northwest Sidewalk Intersection"},
    
    # Street nodes
    "G_street_north_1": {"lat": 37.4998, "lng": 127.0272, "name": "Gangnam-daero North Side"},
    "G_street_south_1": {"lat": 37.4960, "lng": 127.0279, "name": "Gangnam-daero South Side"},
    "G_street_east_1": {"lat": 37.4980, "lng": 127.0298, "name": "Teheran-ro East Side"},
    "G_street_west_1": {"lat": 37.4978, "lng": 127.0250, "name": "Teheran-ro West Side"},
    
    # Crossings (North-South, East-West)
    "G_crosswalk_north": {"lat": 37.4982, "lng": 127.0275, "name": "North Crosswalk (Gangnam-daero)"},
    "G_crosswalk_south": {"lat": 37.4976, "lng": 127.0275, "name": "South Crosswalk (Gangnam-daero)"},
    "G_crosswalk_east": {"lat": 37.4979, "lng": 127.0280, "name": "East Crosswalk (Teheran-ro)"},
    "G_crosswalk_west": {"lat": 37.4979, "lng": 127.0271, "name": "West Crosswalk (Teheran-ro)"},
    
    # POI specific node connectors
    "G_poi_kakao": {"lat": 37.4985, "lng": 127.0272, "name": "Kakao Friends Entrance"},
    "G_poi_bbq": {"lat": 37.4995, "lng": 127.0290, "name": "Gangnam BBQ Entrance (Steep Steps)"},
    "G_poi_starbucks": {"lat": 37.4978, "lng": 127.0286, "name": "Starbucks Entrance"},
    "G_poi_twosome": {"lat": 37.4963, "lng": 127.0280, "name": "A Twosome Place Entrance (Step)"}
}
GANGNAM_EDGES = [
    # Underground platform to ticket concourse
    ("G_platform", "G_concourse", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Platform to Concourse Elevator"}),
    
    # Concourse to Exits (Subway stairs vs elevators)
    ("G_concourse", "G_exit_1", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground Passage to Exit 1 Elevator"}),
    ("G_concourse", "G_exit_2", {"has_stairs": True, "has_elevator": False, "slope": 15, "name": "Underground Stairs to Exit 2"}),
    ("G_concourse", "G_exit_8", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground Passage to Exit 8 Elevator"}),
    ("G_concourse", "G_exit_11", {"has_stairs": True, "has_elevator": False, "slope": 15, "name": "Underground Stairs to Exit 11"}),
    ("G_concourse", "G_exit_12", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground Passage to Exit 12 Elevator"}),
    
    # Exits to Sidewalks
    ("G_exit_1", "G_sidewalk_ne", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 1 to Sidewalk"}),
    ("G_exit_2", "G_sidewalk_se", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 2 to Sidewalk"}),
    ("G_exit_8", "G_sidewalk_sw", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 8 to Sidewalk"}),
    ("G_exit_11", "G_sidewalk_ne", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 11 to Sidewalk"}),
    ("G_exit_12", "G_sidewalk_ne", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 12 to Sidewalk"}),
    
    # Sidewalk to Crosswalks (Flat ramped crossings)
    ("G_sidewalk_nw", "G_crosswalk_north", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "NW Sidewalk to North Crosswalk"}),
    ("G_sidewalk_ne", "G_crosswalk_north", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "NE Sidewalk to North Crosswalk"}),
    
    ("G_sidewalk_sw", "G_crosswalk_south", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "SW Sidewalk to South Crosswalk"}),
    ("G_sidewalk_se", "G_crosswalk_south", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "SE Sidewalk to South Crosswalk"}),
    
    ("G_sidewalk_ne", "G_crosswalk_east", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "NE Sidewalk to East Crosswalk"}),
    ("G_sidewalk_se", "G_crosswalk_east", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "SE Sidewalk to East Crosswalk"}),
    
    ("G_sidewalk_nw", "G_crosswalk_west", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "NW Sidewalk to West Crosswalk"}),
    ("G_sidewalk_sw", "G_crosswalk_west", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "SW Sidewalk to West Crosswalk"}),
    
    # Sidewalk Intersections to Main Streets
    ("G_sidewalk_nw", "G_poi_kakao", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Sidewalk to Kakao Store"}),
    ("G_sidewalk_nw", "G_street_north_1", {"has_stairs": False, "has_elevator": False, "slope": 2, "name": "Sidewalk Northbound"}),
    ("G_street_north_1", "G_poi_kakao", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Street North to Kakao Store"}),
    
    ("G_sidewalk_ne", "G_street_east_1", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Sidewalk Eastbound"}),
    ("G_street_east_1", "G_poi_starbucks", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Street East to Starbucks"}),
    ("G_street_east_1", "G_poi_bbq", {"has_stairs": True, "has_elevator": False, "slope": 12, "name": "Sidewalk to BBQ Entrance (Stairs)"}),
    
    ("G_sidewalk_se", "G_street_south_1", {"has_stairs": False, "has_elevator": False, "slope": 2, "name": "Sidewalk Southbound"}),
    ("G_street_south_1", "G_poi_twosome", {"has_stairs": True, "has_elevator": False, "slope": 8, "name": "Sidewalk to Twosome Cafe (Threshold Step)"}),
    
    ("G_sidewalk_sw", "G_street_west_1", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Sidewalk Westbound"}),
    
    # Subway underground stairs between exits (Stairs Only, No Wheelchair!)
    ("G_concourse", "G_sidewalk_se", {"has_stairs": True, "has_elevator": False, "slope": 15, "name": "Direct Subway Concourse to SE Street Stairs"})
]
# Seoul Station Nodes and Edges
SEOUL_NODES = {
    "S_platform": {"lat": 37.5547, "lng": 126.9707, "name": "Seoul Station Subway Platform (B3)"},
    "S_concourse": {"lat": 37.5547, "lng": 126.9707, "name": "Seoul Station Concourse (B1)"},
    
    # Exits
    "S_exit_1": {"lat": 37.5538, "lng": 126.9696, "name": "Seoul Station Exit 1 (Elevator)"},
    "S_exit_2": {"lat": 37.5545, "lng": 126.9688, "name": "Seoul Station Exit 2 (Stairs)"},
    "S_exit_4": {"lat": 37.5562, "lng": 126.9722, "name": "Seoul Station Exit 4 (Stairs)"},
    "S_exit_9": {"lat": 37.5548, "lng": 126.9718, "name": "Seoul Station Exit 9 (Elevator)"},
    "S_exit_14": {"lat": 37.5520, "lng": 126.9715, "name": "Seoul Station Exit 14 (Elevator)"},
    
    # Plaza and Outer Areas
    "S_plaza_center": {"lat": 37.5546, "lng": 126.9708, "name": "Seoul Station Plaza Central"},
    "S_plaza_north": {"lat": 37.5554, "lng": 126.9709, "name": "Seoul Station Plaza North"},
    "S_plaza_south": {"lat": 37.5532, "lng": 126.9702, "name": "Seoul Station Plaza South"},
    
    # POI connectors
    "S_poi_lotte": {"lat": 37.5539, "lng": 126.9693, "name": "Lotte Outlets Entrance"},
    "S_poi_culture284": {"lat": 37.5553, "lng": 126.9710, "name": "Culture Station 284 Entrance"},
    "S_poi_namdaemun_lane": {"lat": 37.5592, "lng": 126.9765, "name": "Namdaemun Market Entry Lane"},
    "S_poi_tavern": {"lat": 37.5528, "lng": 126.9720, "name": "Old Tavern Entrance (Steps)"},
    
    # Crosswalks
    "S_crosswalk_east": {"lat": 37.5547, "lng": 126.9715, "name": "Plaza to Seoul Square Crosswalk"}
}
SEOUL_EDGES = [
    # Underground to ticket concourse
    ("S_platform", "S_concourse", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Platform to Concourse Elevator"}),
    
    # Concourse to Exits
    ("S_concourse", "S_exit_1", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground to Exit 1 Elevator"}),
    ("S_concourse", "S_exit_2", {"has_stairs": True, "has_elevator": False, "slope": 15, "name": "Underground Stairs to Exit 2"}),
    ("S_concourse", "S_exit_4", {"has_stairs": True, "has_elevator": False, "slope": 15, "name": "Underground Stairs to Exit 4"}),
    ("S_concourse", "S_exit_9", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground to Exit 9 Elevator"}),
    ("S_concourse", "S_exit_14", {"has_stairs": False, "has_elevator": True, "slope": 0, "name": "Underground to Exit 14 Elevator"}),
    
    # Exits to Plaza/Plaza connections
    ("S_exit_1", "S_poi_lotte", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 1 to Lotte Outlets"}),
    ("S_exit_1", "S_plaza_center", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Exit 1 to Central Plaza"}),
    ("S_exit_2", "S_plaza_center", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 2 to Central Plaza"}),
    
    ("S_plaza_center", "S_plaza_north", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Plaza Transit North"}),
    ("S_plaza_center", "S_plaza_south", {"has_stairs": False, "has_elevator": False, "slope": 1, "name": "Plaza Transit South"}),
    
    ("S_plaza_north", "S_poi_culture284", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Plaza to Culture Station Side Ramp"}),
    ("S_plaza_north", "S_exit_9", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Plaza North to Exit 9"}),
    
    ("S_plaza_south", "S_exit_14", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Plaza South to Exit 14"}),
    ("S_plaza_south", "S_poi_tavern", {"has_stairs": True, "has_elevator": False, "slope": 10, "name": "Plaza South to Tavern (Steps)"}),
    
    # Crosswalks to Eastern commercial zone
    ("S_exit_9", "S_crosswalk_east", {"has_stairs": False, "has_elevator": False, "slope": 0, "name": "Exit 9 to Crosswalk"}),
    ("S_crosswalk_east", "S_poi_namdaemun_lane", {"has_stairs": False, "has_elevator": False, "slope": 3, "name": "Crosswalk to Namdaemun lane"}),
    
    # Subway stairs connecting platform to street levels directly (Inaccessible)
    ("S_concourse", "S_plaza_north", {"has_stairs": True, "has_elevator": False, "slope": 20, "name": "Direct Subway Concourse to Plaza North Stairs"})
]
def load_network_graph(area):
    """
    Returns (nodes, edges) for a given area ('Gangnam' or 'Seoul Station').
    """
    if area == "Gangnam":
        return GANGNAM_NODES, GANGNAM_EDGES
    elif area == "Seoul Station":
        return SEOUL_NODES, SEOUL_EDGES
    return {}, []
def get_subway_exits(area):
    """
    Returns subway exits list for given area.
    """
    return SUBWAY_EXITS.get(area, [])
def get_pois(area=None):
    """
    Returns list of POIs, optionally filtered by area.
    Integrates any dynamically reported user reports that are ramp-approved.
    """
    reports = load_crowd_reports()
    
    # Merge reports into POIs
    dynamic_pois = []
    for i, report in enumerate(reports):
        # Convert report to POI format
        dynamic_pois.append({
            "id": f"report_{i}",
            "area": report["area"],
            "name": f"[User Report] {report['name']}",
            "category": report["category"],
            "lat": report["lat"],
            "lng": report["lng"],
            "has_ramp": report["has_ramp"],
            "has_elevator": report.get("has_elevator", False),
            "accessible_toilet": report.get("accessible_toilet", False),
            "entrance_width_ok": True,
            "score": 4.0 if report["has_ramp"] else 2.0,
            "description": f"Verified by User: {report['description']}"
        })
        
    all_pois = POIS + dynamic_pois
    if area:
        return [poi for poi in all_pois if poi["area"] == area]
    return all_pois
# 4. Crowd-Sourcing File Operations
def load_crowd_reports():
    """
    Loads user reported accessible zones.
    """
    if not os.path.exists(REPORTS_FILE):
        return []
    try:
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
def add_crowd_report(area, name, category, lat, lng, has_ramp, has_elevator, accessible_toilet, description):
    """
    Saves a user reported accessible location.
    """
    reports = load_crowd_reports()
    new_report = {
        "area": area,
        "name": name,
        "category": category,
        "lat": float(lat),
        "lng": float(lng),
        "has_ramp": bool(has_ramp),
        "has_elevator": bool(has_elevator),
        "accessible_toilet": bool(accessible_toilet),
        "description": description
    }
    reports.append(new_report)
    try:
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False
# Utility function to calculate geographical distance between two lat/lng pairs (in meters)
def haversine_distance(lat1, lng1, lat2, lng2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
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
    
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import os
from data_store import (
    load_network_graph,
    get_subway_exits,
    get_pois,
    add_crowd_report,
    load_crowd_reports
)
from router import find_shortest_path, find_nearest_node
# Set page config
st.set_page_config(
    page_title="배리어프리 휠체어 맵 | Barrier-Free Wheelchair Map",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom premium styling using Outfit font & glassmorphic cards
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(229, 231, 235, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    
    .dark-mode .card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(55, 65, 81, 0.5);
    }
    
    .kpi-title {
        font-size: 0.875rem;
        text-transform: uppercase;
        color: #9CA3AF;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    
    .kpi-val {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111827;
        margin-top: 0.25rem;
    }
    
    .route-header {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .step-card {
        border-left: 4px solid #10B981;
        padding-left: 10px;
        margin-bottom: 8px;
        background: #F0FDF4;
        border-radius: 0 8px 8px 0;
        padding-top: 6px;
        padding-bottom: 6px;
    }
    
    .step-card-stairs {
        border-left: 4px solid #EF4444;
        padding-left: 10px;
        margin-bottom: 8px;
        background: #FEF2F2;
        border-radius: 0 8px 8px 0;
        padding-top: 6px;
        padding-bottom: 6px;
    }
    
    .rating-badge {
        background: #EEF2F6;
        color: #1E293B;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)
# 1. Main Header
st.markdown('<div class="main-header">♿ 배리어프리 휠체어 길안내 지도</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">사회적 약자와 휠체어 이용자를 위한 지하철 엘리베이터 출구 안내 및 보행 최적 경로 추천 서비스</div>', unsafe_allow_html=True)
# 2. Sidebar Settings
st.sidebar.markdown("### 🗺️ 지역 및 목적지 설정")
selected_area = st.sidebar.selectbox("대상 지역 선택", ["Gangnam", "Seoul Station"], index=0)
# Load data based on area
nodes, edges = load_network_graph(selected_area)
subway_exits = get_subway_exits(selected_area)
pois = get_pois(selected_area)
# Extract subway exits for dropdown
subway_options = {exit_info["exit"]: exit_info for exit_info in subway_exits}
poi_options = {poi["name"]: poi for poi in pois}
# Routing selections
st.sidebar.markdown("#### 📍 경로 탐색")
route_mode = st.sidebar.radio(
    "출발/도착지 지정 방식",
    ["지하철 출구 ➡️ 매장/관광지", "매장/관광지 ➡️ 지하철 출구", "매장/관광지 ➡️ 매장/관광지"],
    index=0
)
# Populate start/end options
start_name = None
end_name = None
start_node_id = None
end_node_id = None
if route_mode == "지하철 출구 ➡️ 매장/관광지":
    start_name = st.sidebar.selectbox("출발 지하철 출구 선택", list(subway_options.keys()))
    end_name = st.sidebar.selectbox("도착 매장/관광지 선택", list(poi_options.keys()))
    
    # Map back to graph nodes
    # Subways are named G_exit_X or S_exit_X in graph
    exit_num = subway_options[start_name]["exit"].split()[-1]
    prefix = "G" if selected_area == "Gangnam" else "S"
    start_node_id = f"{prefix}_exit_{exit_num}"
    
    # POI coords mapped to nearest node in graph
    poi_coords = poi_options[end_name]
    end_node_id = find_nearest_node(nodes, poi_coords["lat"], poi_coords["lng"])
    
elif route_mode == "매장/관광지 ➡️ 지하철 출구":
    start_name = st.sidebar.selectbox("출발 매장/관광지 선택", list(poi_options.keys()))
    end_name = st.sidebar.selectbox("도착 지하철 출구 선택", list(subway_options.keys()))
    
    poi_coords = poi_options[start_name]
    start_node_id = find_nearest_node(nodes, poi_coords["lat"], poi_coords["lng"])
    
    exit_num = subway_options[end_name]["exit"].split()[-1]
    prefix = "G" if selected_area == "Gangnam" else "S"
    end_node_id = f"{prefix}_exit_{exit_num}"
    
else:  # Between POIs
    start_name = st.sidebar.selectbox("출발지 선택", list(poi_options.keys()), index=0)
    end_name = st.sidebar.selectbox("도착지 선택", list(poi_options.keys()), index=min(1, len(poi_options)-1))
    
    start_poi = poi_options[start_name]
    start_node_id = find_nearest_node(nodes, start_poi["lat"], start_poi["lng"])
    
    end_poi = poi_options[end_name]
    end_node_id = find_nearest_node(nodes, end_poi["lat"], end_poi["lng"])
# Routing constraints
wheelchair_friendly = st.sidebar.toggle("♿ 휠체어 안전 경로 찾기 (계단 회피 및 경사도 고려)", value=True)
# Main Application Layout: Tabs
tab_map, tab_crowd, tab_stats = st.tabs(["🗺️ 인터랙티브 지도 & 길안내", "📢 배리어프리 제보 (크라우드소싱)", "📊 지역별 배리어프리 통계"])
# Calculate routing
path_nodes, total_phys_dist, directions = find_shortest_path(
    nodes, edges, start_node_id, end_node_id, wheelchair_mode=wheelchair_friendly
)
# ================= TAB 1: INTERACTIVE MAP & ROUTING =================
with tab_map:
    # 3. KPI Header Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_exits = len(subway_exits)
    elevator_exits_count = sum(1 for e in subway_exits if e["has_elevator"])
    el_ratio = round((elevator_exits_count / total_exits) * 100) if total_exits > 0 else 0
    accessible_pois_count = sum(1 for p in pois if p["score"] >= 4.0)
    
    with kpi1:
        st.markdown(f"""
            <div class="card">
                <div class="kpi-title">총 지하철 출구 수</div>
                <div class="kpi-val">{total_exits}개 출구</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
            <div class="card">
                <div class="kpi-title">엘리베이터 설치 출구</div>
                <div class="kpi-val" style="color: #10B981;">{elevator_exits_count}개소 ({el_ratio}%)</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class="card">
                <div class="kpi-title">휠체어 접근 가능 시설</div>
                <div class="kpi-val" style="color: #3B82F6;">{accessible_pois_count}개소</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
            <div class="card">
                <div class="kpi-title">활성화된 분석 구역</div>
                <div class="kpi-val" style="color: #8B5CF6;">{selected_area}</div>
            </div>
        """, unsafe_allow_html=True)
    col_map_view, col_dir_view = st.columns([7, 3])
    with col_map_view:
        # Determine center coords
        if selected_area == "Gangnam":
            center_lat, center_lng = 37.4979, 127.0276
            zoom_start = 16
        else:
            center_lat, center_lng = 37.5547, 126.9707
            zoom_start = 16
            
        # Create Folium Map
        m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_start, control_scale=True)
        
        # Add subway exit markers
        for exit_info in subway_exits:
            icon_color = "green" if exit_info["has_elevator"] else "red"
            icon_symbol = "info-sign" if exit_info["has_elevator"] else "exclamation-sign"
            
            popup_html = f"""
                <div style='font-family: sans-serif; font-size:12px; width:200px;'>
                    <b>{exit_info['exit']}</b><br/>
                    <b>엘리베이터:</b> {'설치됨 (이용 가능)' if exit_info['has_elevator'] else '미설치 (계단만 있음)'}<br/>
                    <small style='color: gray;'>{exit_info['details']}</small>
                </div>
            """
            
            folium.Marker(
                location=[exit_info["lat"], exit_info["lng"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{exit_info['exit']} (엘리베이터: {'O' if exit_info['has_elevator'] else 'X'})",
                icon=folium.Icon(color=icon_color, icon=icon_symbol)
            ).add_to(m)
            
        # Add POI markers
        for poi in pois:
            # Color code based on accessibility score
            if poi["score"] >= 4.0:
                color = "blue"
            elif poi["score"] >= 2.5:
                color = "orange"
            else:
                color = "lightred"
                
            popup_html = f"""
                <div style='font-family: sans-serif; font-size:12px; width:220px;'>
                    <b>{poi['name']}</b> ({poi['category']})<br/>
                    <b>경사로 설치:</b> {'설치됨 (진입가능)' if poi['has_ramp'] else '계단/턱 있음 (불가)'}<br/>
                    <b>장애인 화장실:</b> {'있음' if poi['accessible_toilet'] else '없음'}<br/>
                    <b>접근성 평점:</b> {'★' * int(poi['score'])}{'☆' * (5 - int(poi['score']))} ({poi['score']}/5)<br/>
                    <hr style='margin: 5px 0;'/>
                    <small style='color: gray;'>{poi['description']}</small>
                </div>
            """
            
            folium.Marker(
                location=[poi["lat"], poi["lng"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{poi['name']} ({poi['category']})",
                icon=folium.Icon(color=color, icon="shopping-cart" if poi["category"]=="Shop" else "cutlery" if poi["category"]=="Restaurant" else "eye-open")
            ).add_to(m)
            
        # Draw computed route on map
        if path_nodes:
            # Build list of lat/lng pairs
            path_coords = [[nodes[node_id]["lat"], nodes[node_id]["lng"]] for node_id in path_nodes]
            
            # Line style based on wheelchair friendly
            line_color = "#10B981" if wheelchair_friendly else "#EF4444"
            line_weight = 7 if wheelchair_friendly else 4
            dash_style = None if wheelchair_friendly else "10, 10"
            
            folium.PolyLine(
                locations=path_coords,
                color=line_color,
                weight=line_weight,
                opacity=0.8,
                dash_array=dash_style,
                tooltip="추천 경로"
            ).add_to(m)
            
            # Mark Start and End explicitly
            folium.CircleMarker(
                location=path_coords[0],
                radius=10,
                color="#4F46E5",
                fill=True,
                fill_color="#4F46E5",
                popup="출발지"
            ).add_to(m)
            
            folium.CircleMarker(
                location=path_coords[-1],
                radius=10,
                color="#D97706",
                fill=True,
                fill_color="#D97706",
                popup="도착지"
            ).add_to(m)
            
        # Render map in streamlit
        st_data = st_folium(m, width=800, height=600, returned_objects=[])
    with col_dir_view:
        st.markdown(f'<div class="route-header">🚶 길안내: {start_name} ➡️ {end_name}</div>', unsafe_allow_html=True)
        
        # Check if route includes any stair segments
        has_stairs_on_route = any(d["has_stairs"] for d in directions) if directions else False
        
        if wheelchair_friendly:
            st.success("♿ 휠체어 안전 경로를 계산했습니다. 계단을 완벽히 회피합니다.")
        else:
            if has_stairs_on_route:
                st.error("⚠️ 경고: 경로에 휠체어로 이동 불가능한 계단/턱 구간이 포함되어 있습니다.")
            else:
                st.info("ℹ️ 일반 최단 경로를 탐색했습니다. (현재 경로에는 다행히 계단이 포함되지 않음)")
                
        if directions:
            st.metric("총 보행 거리", f"{round(total_phys_dist)}m")
            
            st.write("---")
            st.write("**상세 이동 경로:**")
            
            for i, step in enumerate(directions):
                is_stair = step["has_stairs"]
                card_class = "step-card-stairs" if is_stair else "step-card"
                stair_warning = " 🛑 **[계단/턱 주의!]**" if is_stair else ""
                icon = "🚨" if is_stair else "➡️"
                
                st.markdown(f"""
                    <div class="{card_class}">
                        <b>{i+1}. {step['from']}</b> 에서 <b>{step['to']}</b> (으)로 이동<br/>
                        <span style='font-size: 0.9rem; color: #555;'>구간: {step['action']} ({step['distance']}m)</span>{stair_warning}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("출발지와 도착지 간의 경로를 찾을 수 없습니다. 그래프가 분리되어 있거나 잘못된 노드입니다.")
# ================= TAB 2: CROWD-SOURCING REPORTS =================
with tab_crowd:
    st.markdown("### 📢 장애인 편의시설 제보 서비스")
    st.write("휠체어 사용자가 길을 걷다 발견한 경사로, 장애인 화장실, 엘리베이터 여부를 제보하여 사회적 지도를 함께 완성해주세요.")
    
    col_form, col_reports = st.columns([5, 5])
    
    with col_form:
        st.write("**신규 편의시설 제보하기**")
        with st.form("crowd_report_form", clear_on_submit=True):
            report_area = st.selectbox("지역 선택", ["Gangnam", "Seoul Station"])
            venue_name = st.text_input("매장/장소 이름", placeholder="예: 무장애 삼겹살 강남점")
            category = st.selectbox("업종/종류", ["Restaurant", "Cafe", "Shop", "Tourist Attraction"])
            
            # Simple simulation coordinate helpers
            st.write("위치 좌표 지정 (테스트를 위해 자동 지정 가능)")
            lat_default = 37.4980 if report_area == "Gangnam" else 37.5540
            lng_default = 127.0270 if report_area == "Gangnam" else 126.9700
            
            lat = st.number_input("위도 (Latitude)", value=lat_default, format="%.6f")
            lng = st.number_input("경도 (Longitude)", value=lng_default, format="%.6f")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                has_ramp = st.checkbox("♿ 입구 경사로 설치됨", value=True)
            with c2:
                has_elevator = st.checkbox("🛗 내부 엘리베이터 있음", value=False)
            with c3:
                accessible_toilet = st.checkbox("🚽 장애인 전용 화장실 있음", value=False)
                
            description = st.text_area("상세 상태 제보", placeholder="입구에 턱이 없으나 내부에 테이블 간격이 다소 좁습니다.")
            
            submitted = st.form_submit_form_button = st.form_submit_button("제보 제출하기")
            
            if submitted:
                if not venue_name.strip():
                    st.warning("매장/장소 이름을 입력해주세요.")
                else:
                    success = add_crowd_report(
                        report_area, venue_name, category, lat, lng,
                        has_ramp, has_elevator, accessible_toilet, description
                    )
                    if success:
                        st.success("제보해 주셔서 감사합니다! 즉시 지도에 반영되었습니다.")
                        st.rerun()
                    else:
                        st.error("제보 저장에 실패했습니다.")
    with col_reports:
        st.write("**최근 제보 현황**")
        reports = load_crowd_reports()
        if not reports:
            st.info("아직 사용자 제보가 없습니다. 첫 제보의 주인공이 되어주세요!")
        else:
            # Create a dataframe for display
            df_reports = pd.DataFrame(reports)
            st.dataframe(
                df_reports[["name", "category", "has_ramp", "has_elevator", "description"]],
                column_config={
                    "name": "장소명",
                    "category": "분류",
                    "has_ramp": "경사로 유무",
                    "has_elevator": "엘리베이터",
                    "description": "설명"
                },
                hide_index=True,
                use_container_width=True
            )
# ================= TAB 3: STATISTICS & ANALYTICS =================
with tab_stats:
    st.markdown("### 📊 배리어프리 편의성 분석 대시보드")
    st.write("각 구역별 편의시설 분포 및 접근성 점수를 시각적으로 제공하여 개선이 필요한 구역을 분석합니다.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    # Calculate stats
    all_pois = get_pois() # includes user reports
    df_pois = pd.DataFrame(all_pois)
    
    with col_chart1:
        st.write("**1. 매장 분류별 장애인 경사로(Ramp) 설치 비율**")
        if not df_pois.empty:
            ramp_stats = df_pois.groupby("category")["has_ramp"].mean().reset_index()
            ramp_stats["has_ramp"] = ramp_stats["has_ramp"] * 100
            
            chart1 = alt.Chart(ramp_stats).mark_bar(color='#10B981').encode(
                x=alt.X('category:N', title='업종 분류'),
                y=alt.Y('has_ramp:Q', title='경사로 설치율 (%)', scale=alt.Scale(domain=[0, 100])),
                tooltip=['category', 'has_ramp']
            ).properties(height=300)
            
            st.altair_chart(chart1, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")
            
    with col_chart2:
        st.write("**2. 편의시설 카테고리별 평균 접근성 점수 (5점 만점)**")
        if not df_pois.empty:
            score_stats = df_pois.groupby("category")["score"].mean().reset_index()
            
            chart2 = alt.Chart(score_stats).mark_bar(color='#3B82F6').encode(
                x=alt.X('category:N', title='업종 분류'),
                y=alt.Y('score:Q', title='평균 평점 (점)', scale=alt.Scale(domain=[0, 5])),
                tooltip=['category', 'score']
            ).properties(height=300)
            
            st.altair_chart(chart2, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")
            
    st.write("---")
    st.write("**3. 정밀 데이터 분석 테이블 (Gangnam & Seoul Station)**")
    st.dataframe(
        df_pois[["area", "name", "category", "has_ramp", "has_elevator", "accessible_toilet", "score"]],
        column_config={
            "area": "지역",
            "name": "장소명",
            "category": "카테고리",
            "has_ramp": "경사로 여부",
            "has_elevator": "엘리베이터",
            "accessible_toilet": "장애인 화장실",
            "score": "배리어프리 점수"
        },
        hide_index=True,
        use_container_width=True
    )
