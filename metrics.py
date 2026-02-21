# metrics.py
import numpy as np
from sentence_transformers import SentenceTransformer
import re

class AttributeMetrics:
    """논문의 7가지 속성 측정"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def measure_specificity(self, reframe, thought, situation):
        """구체성: Reframe이 상황/생각과 얼마나 관련되어 있는가"""
        context = f"{thought} {situation}"
        
        emb_reframe = self.embedding_model.encode(reframe)
        emb_context = self.embedding_model.encode(context)
        
        similarity = np.dot(emb_reframe, emb_context) / (
            np.linalg.norm(emb_reframe) * np.linalg.norm(emb_context)
        )
        
        return float(similarity)
    
    def measure_actionability(self, reframe):
        """실행가능성: 구체적 행동 제안이 있는가"""
        action_patterns = [
            r'\b(can|will|could|should|try|start|practice|focus|work|plan)\b',
            r'\b(하자|해보자|할 수 있다|하겠다|시작하다)\b',
        ]
        
        score = 0
        for pattern in action_patterns:
            matches = re.findall(pattern, reframe, re.IGNORECASE)
            score += len(matches)
        
        return min(score / 3.0, 1.0)
    
    def measure_empathy(self, reframe):
        """공감: 감정 인정 및 지지 표현"""
        empathy_keywords = [
            'understand', 'feel', 'okay', 'normal', 'valid',
            '이해', '괜찮', '힘들', '당연', '자연스러운'
        ]
        
        score = sum(1 for kw in empathy_keywords if kw in reframe.lower())
        return min(score / 3.0, 1.0)
    
    def measure_positivity(self, reframe):
        """긍정성: 긍정적 단어 사용"""
        positive_words = [
            'can', 'will', 'able', 'succeed', 'good', 'better', 'improve',
            '할 수 있', '잘', '개선', '성장', '가능'
        ]
        
        score = sum(1 for word in positive_words if word in reframe.lower())
        return min(score / 4.0, 1.0)
    
    def measure_all(self, reframe, thought, situation):
        """모든 속성 측정"""
        return {
            'specificity': round(self.measure_specificity(reframe, thought, situation), 3),
            'actionability': round(self.measure_actionability(reframe), 3),
            'empathy': round(self.measure_empathy(reframe), 3),
            'positivity': round(self.measure_positivity(reframe), 3),
        }