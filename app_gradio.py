import os
import gradio as gr
from data_store import SUBWAY_EXITS, POIS, get_pois
import google.generativeai as genai

# Try to configure Gemini API
gemini_key = os.environ.get("GEMINI_API_KEY")
gemini_active = False

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        gemini_active = True
    except Exception as e:
        print(f"Failed to configure Gemini API: {e}")

# Build local context document for Gemini API
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

    # 3. Default message instructing how to register API key or query locally
    return (
        "🤖 **배리어프리 AI 안내 비서입니다.**\n\n"
        "현재 API 키가 등록되지 않아 **로컬 데이터 모드**로 작동 중입니다. 다음과 같이 구체적으로 질문해 주세요:\n"
        "- *예: '강남역 11번 출구 엘리베이터 있나요?'*\n"
        "- *예: '서울역 주변 맛집 추천해줘'*\n"
        "- *예: '강남역 카페 찾아줘'*\n\n"
        "✨ **실시간 생성형 AI 대화**를 이용하시려면 시스템 환경 변수에 `GEMINI_API_KEY`를 설정한 후 서버를 재시작해 주세요. "
        "토큰이 완전히 소진될 경우 백업 수단으로 **Gemini-CLI**를 추천합니다."
    )

def respond(message, history):
    if gemini_active:
        try:
            # Setup Generative AI
            db_context = get_database_context()
            system_prompt = (
                "You are an empathetic, helpful AI travel assistant for wheelchair users and social workers.\n"
                "Answer questions about wheelchair accessibility, transit elevators, ramps, and pathways.\n"
                f"Use the following real-time database context to answer accurately:\n{db_context}\n"
                "If the user asks about a location not in the database, guide them politely, suggest checking nearby subway exits, "
                "or explain that they can report it using the Streamlit crowd-sourcing portal.\n"
                "Keep responses in Korean (한국어), friendly, and format with markdown lists or bold markers."
            )
            
            # Combine history for context
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_prompt
            )
            
            # Convert Gradio history to Gemini API format if needed, or just send a direct request with message
            prompt = f"User asks: {message}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error contacting Gemini API: {e}. Falling back to local data.\n\n" + local_fallback_chat(message)
    else:
        return local_fallback_chat(message)

# Define custom Gradio Theme matching the CSS
theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="cyan",
    neutral_hue="slate"
)

# Launch Gradio Block
with gr.Blocks(title="배리어프리 AI 안내 비서") as demo:
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #4F46E5; margin-bottom: 5px;">♿ 배리어프리 AI 안내 비서</h1>
            <p style="color: #6B7280; font-size: 1.1em;">휠체어 이동 시 궁금한 엘리베이터 위치와 매장 접근성 정보를 대화로 실시간 답변받으세요.</p>
        </div>
        """
    )
    
    chatbot = gr.ChatInterface(
        fn=respond,
        examples=[
            ["강남역 2번 출구 엘리베이터 있나요?"],
            ["강남역 주변 휠체어 진입 가능한 카페 추천해줘"],
            ["서울역 9번 출구 엘리베이터 위치"],
            ["서울역 Lotte Outlets 휠체어 탈 수 있나요?"]
        ]
    )
    
    gr.HTML(
        """
        <div style="margin-top: 30px; padding: 15px; background-color: #F3F4F6; border-radius: 8px; font-size: 0.9em; color: #4B5563;">
            💡 <b>이용 팁:</b> 지하철역 이름(강남역/서울역)과 구체적인 출구 번호를 입력하시면 엘리베이터 유무 및 가까운 출구를 즉시 검색해 줍니다. 
            <br/>토큰 만료 시 대체안으로 <b>Gemini-CLI</b> 사용을 적극 권장합니다.
        </div>
        """
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=theme)
