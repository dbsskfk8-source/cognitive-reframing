# llm_client.py
import openai
import os
from dotenv import load_dotenv
from random import shuffle

load_dotenv()

class LLMClient:
    """OpenAI GPT-4o-mini 클라이언트 (논문 원본 방식)"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY가 .env 파일에 없습니다!")
        
        openai.api_key = self.api_key
        self.model = "gpt-4o-mini"
        print(f"✅ OpenAI 클라이언트 초기화: {self.model}")
    
    def classify_thinking_traps(self, thought, situation):
        """사고함정 분류 (Few-shot)"""
        
        prompt = f"""Here are examples of cognitive distortion classification:

Thought: "Everyone will hate me"
Cognitive Distortion: Mind Reading (85%)

Thought: "I will fail again"
Cognitive Distortion: Fortune Telling (90%)

Thought: "I am completely worthless"
Cognitive Distortion: Labeling (80%)

Thought: "If it's not perfect, it's a failure"
Cognitive Distortion: All-or-Nothing Thinking (75%)

Thought: "The worst will happen"
Cognitive Distortion: Catastrophizing (88%)

---

Situation: {situation}
Thought: {thought}
Cognitive Distortion:"""

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in identifying cognitive distortions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                top_p=0.6  # 논문 원본값
            )
            
            result = response.choices[0].message.content.strip()
            print(f"🧠 사고함정 분류: {result}")
            return result
            
        except Exception as e:
            print(f"❌ API 오류: {e}")
            return "Error"
    
    def generate_reframe(self, thought, situation, similar_cases):
        """
        재구성 생성 (논문 원본 방식)
        - 영어 프롬프트
        - top_p=0.6
        - max_tokens=256
        """
        
        # 논문 원본: shuffle 적용
        similar_cases_list = similar_cases.to_dict('records')
        shuffle(similar_cases_list)
        
        # 논문 원본 프롬프트 형식
        prompt = ""
        for case in similar_cases_list:
            prompt += f"Situation: {case['situation']}\n"
            prompt += f"Distorted Thought: {case['thought']}\n"
            prompt += f"Rational Response: {case['reframe']}\n\n"
        
        # 테스트 입력
        test_input = f"Situation: {situation}\nDistorted Thought: {thought}\nRational Response:"

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cognitive therapist helping people reframe negative thoughts."},
                    {"role": "user", "content": prompt + test_input}
                ],
                max_tokens=256,  # 논문 원본값
                top_p=0.6,       # 논문 원본값
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            reframe = response.choices[0].message.content.strip()
            print(f"✨ 재구성 생성 완료")
            return reframe
            
        except Exception as e:
            print(f"❌ API 오류: {e}")
            return "Error"