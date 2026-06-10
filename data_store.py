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
