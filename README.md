# 🧠 Cognitive Reframing (인지 재구성 도구)

부정적인 생각을 건강하고 합리적인 관점으로 변화시키는 과정을 돕는 AI 도구입니다. 이 프로젝트는 **ACL 2023 논문 "Cognitive Reframing of Negative Thoughts"**의 핵심 방법론(Retrieval-based In-context Learning)을 현대적인 서버리스 아키텍처로 재현했습니다.

## 🏗️ 시스템 아키텍처

```mermaid
graph TD
    User((사용자)) -->|부정적 생각/상황| Frontend[Vite + React Frontend]
    Frontend -->|API Request| VercelAPI[Vercel Serverless Functions]
    
    subgraph "Backend (Vercel API)"
        VercelAPI --> Classify[/api/classify]
        VercelAPI --> Reframe[/api/reframe]
        VercelAPI --> Measure[/api/measure]
        
        Reframe --> Search[Similarity Search]
        Search --> Dataset[(Dataset JSON)]
    end
    
    Classify --> OpenAI((OpenAI API))
    Reframe --> OpenAI
    Measure --> OpenAI
    
    OpenAI -->|결과 반환| VercelAPI
    VercelAPI -->|JSON 결과| Frontend
```

## 🚀 주요 특징

- **논문 기반 로직**: 600개의 전문가 레이블 데이터를 바탕으로 가장 유사한 치료 사례를 검색(Retrieval)하여 상황에 맞는 최적의 재구성을 제안합니다.
- **서버리스 아키텍처**: Python 백엔드를 제거하고 Vercel Serverless Functions로 통합하여 배포 속도와 반응 속도를 극대화했습니다.
- **AI 기반 분석**: OpenAI GPT-4o-mini 모델을 사용하여 사고함정을 분류하고 정교한 인지 재구성 문장을 생성합니다.
- **7가지 속성 측정 및 제어**: 생성된 문장의 공감도, 구체성, 실행 가능성 등을 실시간으로 측정하고 사용자가 원하는 방향으로 조절할 수 있습니다.

## 🛠️ 기술 스택

- **Frontend**: React (Vite), Axios
- **Backend**: Vercel Serverless Functions (Node.js)
- **AI/ML**: OpenAI API (Chat Completion, Embeddings)
- **Data**: JSON-based Static Vector Search

## 🏁 시작하기

### 1. 환경 변수 설정
Vercel 대시보드 또는 로컬 `.env` 파일에 다음 항목을 추가해야 합니다.
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 설치 및 실행 (로컬)
```bash
# 프론트엔드 폴더로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 📦 배포 방법 (Vercel)

이 프로젝트는 별도의 백엔드 서버 없이 Vercel 한 곳에서 모두 배포됩니다.
1. GitHub 저장소를 Vercel에 연결합니다.
2. Root Directory를 `frontend`로 설정합니다.
3. `OPENAI_API_KEY` 환경 변수를 추가합니다.
4. 배포(Deploy) 버튼을 누르면 끝!

---
*본 프로젝트는 인지 행동 치료(CBT) 기법을 기반으로 제작되었습니다.*
