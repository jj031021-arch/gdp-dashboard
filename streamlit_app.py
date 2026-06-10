import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import os
import google.generativeai as genai

from data_store import (
    load_network_graph,
    get_subway_exits,
    get_pois,
    add_crowd_report,
    load_crowd_reports,
    SUBWAY_EXITS,
    get_pois
)
from router import find_shortest_path, find_nearest_node

# Set page config
st.set_page_config(
    page_title="배리어프리 휠체어 맵 | Barrier-Free Wheelchair Map",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API if key is present
gemini_key = os.environ.get("GEMINI_API_KEY")
gemini_active = False

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        gemini_active = True
    except Exception as e:
        pass

# Build local context document for AI Chatbot
def get_database_context():
    context = "Here is the accessibility database for Gangnam and Seoul Station:\n\n"
    context += "=== SUBWAY EXITS WITH ELEVATORS ===\n"
    for area, exits in SUBWAY_EXITS.items():
        context += f"Area: {area}\n"
        for e in exits:
            el_status = "ELEVATOR INSTALLED (Accessible)" if e["has_elevator"] else "STAIRS ONLY (Inaccessible)"
            context += f"- {e['exit']}: {el_status}. Details: {e['details']}\n"
            
    context += "\n=== POINTS OF INTEREST (POIs) AND ACCESS RAMP STATUS ===\n"
    all_pois = get_pois()
    for poi in all_pois:
        context += f"Name: {poi['name']}\n"
        context += f"  Area: {poi['area']}, Category: {poi['category']}\n"
        context += f"  Ramp Installed: {'Yes (Wheelchair entry OK)' if poi['has_ramp'] else 'No (Stairs/Threshold step present)'}\n"
        context += f"  Elevator inside: {'Yes' if poi['has_elevator'] else 'No'}\n"
        context += f"  Accessible Toilet: {'Yes' if poi['accessible_toilet'] else 'No'}\n"
        context += f"  Overall Accessibility Rating: {poi['score']}/5\n"
        context += f"  Description: {poi['description']}\n\n"
    return context

# Fallback parser if Gemini API key is missing
def local_fallback_chat(message):
    message_lower = message.lower()
    
    # 1. Check if user is asking about subway elevator exits
    for area, exits in SUBWAY_EXITS.items():
        if area.lower() in message_lower or ("강남" in message and area == "Gangnam") or ("서울역" in message and area == "Seoul Station"):
            for e in exits:
                # Extract exit number
                exit_num = e["exit"].split()[-1]
                if f"{exit_num}번" in message or f"exit {exit_num}" in message_lower:
                    status = "엘리베이터가 설치되어 있어 휠체어로 이용하기 편리합니다." if e["has_elevator"] else "계단만 있으며 엘리베이터가 없습니다."
                    suggestion = f" 가장 가까운 엘리베이터 설치 출구는 {e['details']}" if not e["has_elevator"] else ""
                    return f"📢 **[{area} {e['exit']}]** 정보입니다.\n\n해당 출구는 **{status}**\n{suggestion}\n\n*(이 답변은 로컬 데이터베이스 조회를 통해 제공되었습니다.)*"
                    
    # 2. Check if user is asking about cafes, restaurants, etc.
    target_category = None
    if "카페" in message or "cafe" in message_lower:
        target_category = "Cafe"
    elif "식당" in message or "맛집" in message_lower or "밥" in message or "restaurant" in message_lower:
        target_category = "Restaurant"
    elif "상점" in message or "가게" in message or "쇼핑" in message or "shop" in message_lower:
        target_category = "Shop"
    elif "관광" in message or "볼거리" in message or "attraction" in message_lower:
        target_category = "Tourist Attraction"
        
    if target_category:
        area_name = "Gangnam"
        area_kor = "강남역"
        if "서울역" in message:
            area_name = "Seoul Station"
            area_kor = "서울역"
            
        matching_pois = [p for p in get_pois(area_name) if p["category"] == target_category]
        if matching_pois:
            reply = f"♿ **{area_kor} 주변의 {target_category} 관련 시설 안내**입니다:\n\n"
            for poi in matching_pois:
                ramp_status = "🟢 경사로 설치 (휠체어 진입 가능)" if poi["has_ramp"] else "🔴 입구 턱/계단 있음 (진입 제한)"
                toilet_status = "장애인 화장실 있음" if poi["accessible_toilet"] else "장애인 화장실 없음"
                reply += f"- **{poi['name']}** (★{poi['score']}/5)\n"
                reply += f"  - {ramp_status} | {toilet_status}\n"
                reply += f"  - *{poi['description']}*\n\n"
            reply += "*(이 답변은 로컬 데이터베이스 조회를 통해 제공되었습니다.)*"
            return reply

    # 3. Default message instructing how to query locally
    return (
        "🤖 **배리어프리 AI 안내 비서입니다.**\n\n"
        "현재 API 키가 등록되지 않아 **로컬 데이터 모드**로 작동 중입니다. 다음과 같이 구체적으로 질문해 주세요:\n"
        "- *예: '강남역 11번 출구 엘리베이터 있나요?'*\n"
        "- *예: '서울역 주변 맛집 추천해줘'*\n"
        "- *예: '강남역 카페 찾아줘'*\n\n"
        "✨ **실시간 생성형 AI 대화**를 이용하시려면 시스템 환경 변수에 `GEMINI_API_KEY`를 설정해 주세요. "
        "토큰이 완전히 소진될 경우 백업 수단으로 **Gemini-CLI**를 추천합니다."
    )

def respond_chat(message):
    if gemini_active:
        try:
            db_context = get_database_context()
            system_prompt = (
                "You are an empathetic, helpful AI travel assistant for wheelchair users and social workers.\n"
                "Answer questions about wheelchair accessibility, transit elevators, ramps, and pathways.\n"
                f"Use the following real-time database context to answer accurately:\n{db_context}\n"
                "If the user asks about a location not in the database, guide them politely.\n"
                "Keep responses in Korean (한국어), friendly, and format with markdown."
            )
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_prompt
            )
            response = model.generate_content(f"User asks: {message}")
            return response.text
        except Exception as e:
            return f"Error contacting Gemini API: {e}. Falling back to local data.\n\n" + local_fallback_chat(message)
    else:
        return local_fallback_chat(message)

# Custom premium styling
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

subway_options = {exit_info["exit"]: exit_info for exit_info in subway_exits}
poi_options = {poi["name"]: poi for poi in pois}

st.sidebar.markdown("#### 📍 경로 탐색")
route_mode = st.sidebar.radio(
    "출발/도착지 지정 방식",
    ["지하철 출구 ➡️ 매장/관광지", "매장/관광지 ➡️ 지하철 출구", "매장/관광지 ➡️ 매장/관광지"],
    index=0
)

start_name = None
end_name = None
start_node_id = None
end_node_id = None

if route_mode == "지하철 출구 ➡️ 매장/관광지":
    start_name = st.sidebar.selectbox("출발 지하철 출구 선택", list(subway_options.keys()))
    end_name = st.sidebar.selectbox("도착 매장/관광지 선택", list(poi_options.keys()))
    exit_num = subway_options[start_name]["exit"].split()[-1]
    prefix = "G" if selected_area == "Gangnam" else "S"
    start_node_id = f"{prefix}_exit_{exit_num}"
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
    
else:
    start_name = st.sidebar.selectbox("출발지 선택", list(poi_options.keys()), index=0)
    end_name = st.sidebar.selectbox("도착지 선택", list(poi_options.keys()), index=min(1, len(poi_options)-1))
    start_poi = poi_options[start_name]
    start_node_id = find_nearest_node(nodes, start_poi["lat"], start_poi["lng"])
    end_poi = poi_options[end_name]
    end_node_id = find_nearest_node(nodes, end_poi["lat"], end_poi["lng"])

wheelchair_friendly = st.sidebar.toggle("♿ 휠체어 안전 경로 찾기 (계단 회피 및 경사도 고려)", value=True)

# Main Application Layout: Tabs (Chat is now natively integrated here!)
tab_map, tab_crowd, tab_stats, tab_chat = st.tabs([
    "🗺️ 인터랙티브 지도 & 길안내", 
    "📢 배리어프리 제보 (크라우드소싱)", 
    "📊 지역별 배리어프리 통계",
    "🤖 AI 안내 비서 (챗봇)"
])

# Calculate routing
path_nodes, total_phys_dist, directions = find_shortest_path(
    nodes, edges, start_node_id, end_node_id, wheelchair_mode=wheelchair_friendly
)

# ================= TAB 1: INTERACTIVE MAP & ROUTING =================
with tab_map:
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    total_exits = len(subway_exits)
    elevator_exits_count = sum(1 for e in subway_exits if e["has_elevator"])
    el_ratio = round((elevator_exits_count / total_exits) * 100) if total_exits > 0 else 0
    accessible_pois_count = sum(1 for p in pois if p["score"] >= 4.0)
    
    with kpi1:
        st.markdown(f'<div class="card"><div class="kpi-title">총 지하철 출구 수</div><div class="kpi-val">{total_exits}개 출구</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="card"><div class="kpi-title">엘리베이터 설치 출구</div><div class="kpi-val" style="color: #10B981;">{elevator_exits_count}개소 ({el_ratio}%)</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="card"><div class="kpi-title">휠체어 접근 가능 시설</div><div class="kpi-val" style="color: #3B82F6;">{accessible_pois_count}개소</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="card"><div class="kpi-title">활성화된 분석 구역</div><div class="kpi-val" style="color: #8B5CF6;">{selected_area}</div></div>', unsafe_allow_html=True)

    col_map_view, col_dir_view = st.columns([7, 3])

    with col_map_view:
        center_lat, center_lng = (37.4979, 127.0276) if selected_area == "Gangnam" else (37.5547, 126.9707)
        zoom_start = 16
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_start, control_scale=True)
        
        for exit_info in subway_exits:
            icon_color = "green" if exit_info["has_elevator"] else "red"
            icon_symbol = "info-sign" if exit_info["has_elevator"] else "exclamation-sign"
            
            popup_html = f"""
                <div style='font-family: sans-serif; font-size:12px; width:200px;'>
                    <b>{exit_info['exit']}</b><br/>
                    <b>엘리베이터:</b> {'설치됨' if exit_info['has_elevator'] else '미설치'}<br/>
                    <small style='color: gray;'>{exit_info['details']}</small>
                </div>
            """
            folium.Marker(
                location=[exit_info["lat"], exit_info["lng"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{exit_info['exit']} (엘리베이터: {'O' if exit_info['has_elevator'] else 'X'})",
                icon=folium.Icon(color=icon_color, icon=icon_symbol)
            ).add_to(m)
            
        for poi in pois:
            color = "blue" if poi["score"] >= 4.0 else "orange" if poi["score"] >= 2.5 else "lightred"
            popup_html = f"""
                <div style='font-family: sans-serif; font-size:12px; width:220px;'>
                    <b>{poi['name']}</b> ({poi['category']})<br/>
                    <b>경사로:</b> {'설치됨' if poi['has_ramp'] else '미설치'}<br/>
                    <b>평점:</b> {poi['score']}/5<br/>
                    <small style='color: gray;'>{poi['description']}</small>
                </div>
            """
            folium.Marker(
                location=[poi["lat"], poi["lng"]],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=poi["name"],
                icon=folium.Icon(color=color, icon="shopping-cart" if poi["category"]=="Shop" else "cutlery" if poi["category"]=="Restaurant" else "eye-open")
            ).add_to(m)
            
        if path_nodes:
            path_coords = [[nodes[node_id]["lat"], nodes[node_id]["lng"]] for node_id in path_nodes]
            line_color = "#10B981" if wheelchair_friendly else "#EF4444"
            line_weight = 7 if wheelchair_friendly else 4
            dash_style = None if wheelchair_friendly else "10, 10"
            
            folium.PolyLine(locations=path_coords, color=line_color, weight=line_weight, opacity=0.8, dash_array=dash_style).add_to(m)
            folium.CircleMarker(location=path_coords[0], radius=8, color="#4F46E5", fill=True, fill_color="#4F46E5").add_to(m)
            folium.CircleMarker(location=path_coords[-1], radius=8, color="#D97706", fill=True, fill_color="#D97706").add_to(m)
            
        st_folium(m, width=800, height=550, returned_objects=[])

    with col_dir_view:
        st.markdown(f'<div class="route-header">🚶 길안내: {start_name} ➡️ {end_name}</div>', unsafe_allow_html=True)
        has_stairs_on_route = any(d["has_stairs"] for d in directions) if directions else False
        
        if wheelchair_friendly:
            st.success("♿ 휠체어 안전 경로 (계단 우회 완료)")
        else:
            if has_stairs_on_route:
                st.error("⚠️ 경고: 경로에 계단/턱이 있습니다.")
                
        if directions:
            st.metric("총 보행 거리", f"{round(total_phys_dist)}m")
            st.write("---")
            for i, step in enumerate(directions):
                card_class = "step-card-stairs" if step["has_stairs"] else "step-card"
                stair_warning = " 🛑 **[계단 주의]**" if step["has_stairs"] else ""
                st.markdown(f'<div class="{card_class}"><b>{i+1}. {step["from"]}</b> ➡️ <b>{step["to"]}</b><br/><small>{step["action"]} ({step["distance"]}m)</small>{stair_warning}</div>', unsafe_allow_html=True)
        else:
            st.info("경로를 찾을 수 없습니다.")

# ================= TAB 2: CROWD-SOURCING REPORTS =================
with tab_crowd:
    st.markdown("### 📢 장애인 편의시설 제보")
    st.write("휠체어 사용자가 발견한 경사로, 엘리베이터 여부를 제보하여 배리어프리 지도를 채워주세요.")
    
    col_form, col_reports = st.columns([5, 5])
    
    with col_form:
        with st.form("crowd_report_form", clear_on_submit=True):
            report_area = st.selectbox("지역 선택", ["Gangnam", "Seoul Station"])
            venue_name = st.text_input("장소 이름", placeholder="예: 무장애 카페 강남역점")
            category = st.selectbox("업종", ["Restaurant", "Cafe", "Shop", "Tourist Attraction"])
            
            lat_default = 37.4980 if report_area == "Gangnam" else 37.5540
            lng_default = 127.0270 if report_area == "Gangnam" else 126.9700
            
            lat = st.number_input("위도 (Latitude)", value=lat_default, format="%.6f")
            lng = st.number_input("경도 (Longitude)", value=lng_default, format="%.6f")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                has_ramp = st.checkbox("♿ 입구 경사로 있음", value=True)
            with c2:
                has_elevator = st.checkbox("🛗 내부 엘리베이터 있음", value=False)
            with c3:
                accessible_toilet = st.checkbox("🚽 장애인 화장실 있음", value=False)
                
            description = st.text_area("상세 상태", placeholder="진입 턱이 없으며 출입문이 자동문입니다.")
            submitted = st.form_submit_button("제보 제출하기")
            
            if submitted:
                if not venue_name.strip():
                    st.warning("장소 이름을 입력해주세요.")
                else:
                    success = add_crowd_report(report_area, venue_name, category, lat, lng, has_ramp, has_elevator, accessible_toilet, description)
                    if success:
                        st.success("제보해 주셔서 감사합니다! 즉시 반영되었습니다.")
                        st.rerun()

    with col_reports:
        st.write("**최근 제보 현황**")
        reports = load_crowd_reports()
        if not reports:
            st.info("등록된 제보가 없습니다.")
        else:
            df_reports = pd.DataFrame(reports)
            st.dataframe(
                df_reports[["name", "category", "has_ramp", "has_elevator", "description"]],
                column_config={"name": "장소명", "category": "분류", "has_ramp": "경사로", "has_elevator": "엘리베이터", "description": "설명"},
                hide_index=True,
                width="stretch"
            )

# ================= TAB 3: STATISTICS =================
with tab_stats:
    st.markdown("### 📊 배리어프리 분석 대시보드")
    all_pois = get_pois()
    df_pois = pd.DataFrame(all_pois)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("**1. 분류별 장애인 경사로(Ramp) 설치 비율 (%)**")
        if not df_pois.empty:
            ramp_stats = df_pois.groupby("category")["has_ramp"].mean().reset_index()
            ramp_stats["has_ramp"] = ramp_stats["has_ramp"] * 100
            chart1 = alt.Chart(ramp_stats).mark_bar(color='#10B981').encode(
                x=alt.X('category:N', title='분류'),
                y=alt.Y('has_ramp:Q', title='설치 비율 (%)', scale=alt.Scale(domain=[0, 100])),
                tooltip=['category', 'has_ramp']
            ).properties(height=280)
            st.altair_chart(chart1, use_container_width=True)
            
    with col_chart2:
        st.write("**2. 분류별 평균 배리어프리 접근성 점수**")
        if not df_pois.empty:
            score_stats = df_pois.groupby("category")["score"].mean().reset_index()
            chart2 = alt.Chart(score_stats).mark_bar(color='#3B82F6').encode(
                x=alt.X('category:N', title='분류'),
                y=alt.Y('score:Q', title='평균 점수', scale=alt.Scale(domain=[0, 5])),
                tooltip=['category', 'score']
            ).properties(height=280)
            st.altair_chart(chart2, use_container_width=True)
            
    st.write("---")
    st.dataframe(
        df_pois[["area", "name", "category", "has_ramp", "has_elevator", "accessible_toilet", "score"]],
        column_config={"area": "지역", "name": "장소명", "category": "분류", "has_ramp": "경사로", "has_elevator": "엘리베이터", "accessible_toilet": "화장실", "score": "접근성 점수"},
        hide_index=True,
        width="stretch"
    )

# ================= TAB 4: NATIVE AI CHATBOT (NO PORT ERRORS!) =================
with tab_chat:
    st.markdown("### 🤖 배리어프리 AI 안내 비서")
    st.write("휠체어 이동 시 궁금한 엘리베이터 위치와 매장 접근성 정보를 대화로 실시간 답변받으세요.")
    
    # Store chat history in streamlit session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "안녕하세요! 배리어프리 AI 안내 비서입니다. 강남역이나 서울역의 출구 엘리베이터 위치, 혹은 주변 매장의 경사로 설치 여부에 대해 질문해 주세요! \n\n*예: '강남역 2번 출구 엘리베이터 있나요?' or '서울역 주변 맛집 추천해줘'*"}
        ]
        
    # Render chat window in a container
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Chat Input
    if user_query := st.chat_input("질문을 이곳에 입력해 주세요..."):
        # Add user question to history and show it
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_query)
                
        # Generate chatbot response
        bot_response = respond_chat(user_query)
        
        # Add bot answer to history and show it
        st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(bot_response)
        
        # Force rerun to update scroll position
        st.rerun()
