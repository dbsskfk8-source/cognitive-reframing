# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from data_loader import load_dataset
from embeddings import EmbeddingIndex
from llm_client import LLMClient
from metrics import AttributeMetrics
from attribute_control import increase_empathy, increase_actionability, increase_specificity

# FastAPI 앱 초기화
app = FastAPI(title="Cognitive Reframing API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 객체 (시작 시 1회만 로드)
print("🚀 서버 초기화 중...")
df = load_dataset()
embedding_index = EmbeddingIndex()
embedding_index.build_index(df)
llm_client = LLMClient()
metrics_calculator = AttributeMetrics()
print("✅ 서버 준비 완료!\n")

# Request/Response 모델
class ThoughtInput(BaseModel):
    thought: str
    situation: str = ""

class ReframeInput(BaseModel):
    thought: str
    situation: str
    k: int = 5

class ControlInput(BaseModel):
    reframe: str
    attribute: str
    thought: str = ""
    situation: str = ""

class MeasureInput(BaseModel):
    reframe: str
    thought: str
    situation: str

# 엔드포인트
@app.get("/health")
def health():
    """헬스체크"""
    return {"status": "ok"}

@app.post("/api/classify")
def classify_traps(data: ThoughtInput):
    """사고함정 분류"""
    try:
        print(f"\n📥 분류 요청:")
        print(f"   생각: {data.thought}")
        print(f"   상황: {data.situation}")
        
        trap = llm_client.classify_thinking_traps(data.thought, data.situation)
        
        return {"thinking_trap": trap}
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reframe")
def generate_reframe(data: ReframeInput):
    """재구성 생성 (3개)"""
    try:
        print(f"\n📥 재구성 요청:")
        print(f"   생각: {data.thought}")
        print(f"   상황: {data.situation}")
        print(f"   k: {data.k}")
        
        # 1. Retrieval
        similar_cases = embedding_index.find_similar(data.thought, data.situation, k=data.k)
        
        # 2. Generation (3개)
        reframes = []
        for i in range(3):
            reframe = llm_client.generate_reframe(data.thought, data.situation, similar_cases)
            reframes.append(reframe)
        
        # 유사 사례
        similar_list = similar_cases[['situation', 'thought', 'reframe']].to_dict('records')
        
        return {
            "reframes": reframes,
            "similar_cases": similar_list,
            "retrieved_k": data.k
        }
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/measure")
def measure_attributes(data: MeasureInput):
    """재구성 속성 측정"""
    try:
        print(f"\n📊 속성 측정 요청")
        
        scores = metrics_calculator.measure_all(data.reframe, data.thought, data.situation)
        
        return scores
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/control")
def control_attribute(data: ControlInput):
    """속성 제어"""
    try:
        print(f"\n🎛️ 속성 제어 요청: {data.attribute}")
        
        if data.attribute == 'empathy':
            controlled = increase_empathy(data.reframe)
        elif data.attribute == 'actionability':
            controlled = increase_actionability(data.reframe)
        elif data.attribute == 'specificity':
            controlled = increase_specificity(data.reframe, data.thought, data.situation)
        else:
            raise HTTPException(status_code=400, detail=f"알 수 없는 속성: {data.attribute}")
        
        # 변경된 재구성 속성 측정
        new_scores = metrics_calculator.measure_all(controlled, data.thought, data.situation)
        
        return {
            "controlled_reframe": controlled,
            "attributes": new_scores
        }
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 서버 실행 (개발용)
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    
    print("\n" + "="*50)
    print("🌐 FastAPI 서버 시작")
    print(f"📍 PORT: {port}")
    print("📚 API 문서: /docs")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)