# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import load_dataset
from embeddings import EmbeddingIndex
from llm_client import LLMClient
from metrics import AttributeMetrics
from attribute_control import increase_empathy, increase_actionability, increase_specificity

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)

# 전역 객체 (서버 시작 시 1회만 로드)
print("🚀 서버 초기화 중...")
df = load_dataset()
embedding_index = EmbeddingIndex()
embedding_index.build_index(df)
llm_client = LLMClient()
print("✅ 서버 준비 완료!\n")
metrics_calculator = AttributeMetrics()

@app.route('/health', methods=['GET'])
def health():
    """헬스체크"""
    return jsonify({"status": "ok"})

@app.route('/api/classify', methods=['POST'])
def classify_traps():
    """
    사고함정 분류
    
    요청:
    {
        "thought": "나는 실패할 거야",
        "situation": "시험을 망쳤다"
    }
    
    응답:
    {
        "thinking_trap": "Fortune Telling (85%)"
    }
    """
    try:
        data = request.json
        thought = data.get('thought', '')
        situation = data.get('situation', '')
        
        if not thought:
            return jsonify({"error": "thought 필드가 필요합니다"}), 400
        
        print(f"\n📥 분류 요청:")
        print(f"   생각: {thought}")
        print(f"   상황: {situation}")
        
        # LLM 호출
        trap = llm_client.classify_thinking_traps(thought, situation)
        
        return jsonify({
            "thinking_trap": trap
        })
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/reframe', methods=['POST'])
def generate_reframe():
    """
    재구성 생성 (논문의 핵심 알고리즘)
    
    요청:
    {
        "thought": "나는 PhD를 못 끝낼 거야",
        "situation": "프로젝트가 실패했다"
    }
    
    응답:
    {
        "reframe": "이 프로젝트 실패가 PhD 전체 실패를 의미하지 않습니다...",
        "similar_cases": [...],
        "retrieved_k": 5
    }
    """
    try:
        data = request.json
        thought = data.get('thought', '')
        situation = data.get('situation', '')
        k = data.get('k', 5)
        
        if not thought or not situation:
            return jsonify({"error": "thought와 situation 필드가 필요합니다"}), 400
        
        print(f"\n📥 재구성 요청:")
        print(f"   생각: {thought}")
        print(f"   상황: {situation}")
        print(f"   k: {k}")
        
        # 1. Retrieval (논문 알고리즘)
        similar_cases = embedding_index.find_similar(thought, situation, k=k)
        
        
        # 2. Generation (Retrieval-enhanced) - 3개 생성 (논문 방식)
        reframes = []
        for i in range(3):
            reframe = llm_client.generate_reframe(thought, situation, similar_cases)
            reframes.append(reframe)
            
        # 유사 사례도 함께 반환
        similar_list = similar_cases[['situation', 'thought', 'reframe']].to_dict('records')
        
        return jsonify({
            "reframes": reframes,
            "similar_cases": similar_list,
            "retrieved_k": k
        })
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/control', methods=['POST'])
def control_attribute():
    """
    속성 제어
    
    요청:
    {
        "reframe": "...",
        "attribute": "empathy",
        "thought": "...",
        "situation": "..."
    }
    """
    try:
        data = request.json
        reframe = data.get('reframe', '')
        attribute = data.get('attribute', '')
        thought = data.get('thought', '')
        situation = data.get('situation', '')
        
        if not reframe or not attribute:
            return jsonify({"error": "reframe과 attribute 필드가 필요합니다"}), 400
        
        print(f"\n🎛️ 속성 제어 요청: {attribute}")
        
        if attribute == 'empathy':
            controlled = increase_empathy(reframe)
        elif attribute == 'actionability':
            controlled = increase_actionability(reframe)
        elif attribute == 'specificity':
            controlled = increase_specificity(reframe, thought, situation)
        else:
            return jsonify({"error": f"알 수 없는 속성: {attribute}"}), 400
        
        # 변경된 재구성의 속성도 측정
        new_scores = metrics_calculator.measure_all(controlled, thought, situation)
        
        return jsonify({
            "controlled_reframe": controlled,
            "attributes": new_scores
        })
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/measure', methods=['POST'])
def measure_attributes():
    """
    재구성의 속성 측정
    
    요청:
    {
        "reframe": "...",
        "thought": "...",
        "situation": "..."
    }
    """
    try:
        data = request.json
        reframe = data.get('reframe', '')
        thought = data.get('thought', '')
        situation = data.get('situation', '')
        
        if not reframe:
            return jsonify({"error": "reframe 필드가 필요합니다"}), 400
        
        print(f"\n📊 속성 측정 요청")
        
        scores = metrics_calculator.measure_all(reframe, thought, situation)
        
        return jsonify(scores)
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌐 Flask 서버 시작")
    print("📍 URL: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)