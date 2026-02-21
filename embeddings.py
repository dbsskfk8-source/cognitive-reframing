# embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

class EmbeddingIndex:
    """논문의 Retrieval 방식 정확히 재현"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"🔄 Embedding 모델 로드 중: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.df = None
        self.embeddings = None
        print("✅ 모델 로드 완료")
    
    def build_index(self, df, cache_file='embeddings_cache.pkl'):
        """데이터셋 임베딩 (최초 1회만, 이후 캐시 사용)"""
        self.df = df
        
        # 캐시 확인
        if os.path.exists(cache_file):
            print("📦 캐시에서 임베딩 로드 중...")
            with open(cache_file, 'rb') as f:
                self.embeddings = pickle.load(f)
            print(f"✅ 캐시 로드 완료: {len(self.embeddings)}개")
            return
        
        # 새로 생성
        print(f"🔄 {len(df)}개 문장 임베딩 중... (1-2분 소요)")
        
        # 논문 방식: thought + situation 결합
        combined = df['thought'] + ' ' + df['situation']
        self.embeddings = self.model.encode(
            combined.tolist(), 
            show_progress_bar=True,
            batch_size=32
        )
        
        # 캐시 저장
        with open(cache_file, 'wb') as f:
            pickle.dump(self.embeddings, f)
        print(f"✅ 임베딩 완료 및 캐시 저장")
    
    def find_similar(self, thought, situation, k=5):
        """
        논문 알고리즘: Retrieval-based In-context Learning
        k=5가 논문의 최적값
        """
        # Query 임베딩
        query = f"{thought} {situation}"
        query_emb = self.model.encode(query)
        
        # 코사인 유사도 계산
        similarities = np.dot(self.embeddings, query_emb) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        
        # Top-k 추출
        top_k_idx = np.argsort(similarities)[-k:][::-1]
        
        # 논문 원본: shuffle 적용
        from random import shuffle as random_shuffle
        top_k_list = top_k_idx.tolist()
        random_shuffle(top_k_list)
        
        print(f"🔍 Top-{k} 유사 사례 검색 완료 (shuffled)")
        for i, idx in enumerate(top_k_list):
            print(f"  {i+1}. 유사도: {similarities[idx]:.3f}")
        
        return self.df.iloc[top_k_list]

# 테스트
if __name__ == "__main__":
    from data_loader import load_dataset
    
    # 데이터 로드
    df = load_dataset()
    
    # 인덱스 구축
    index = EmbeddingIndex()
    index.build_index(df)
    
    # 검색 테스트
    similar = index.find_similar(
        thought="I'll never finish my PhD",
        situation="My research project failed",
        k=5
    )
    
    print("\n📋 검색 결과:")
    print(similar[['situation', 'thought', 'reframe']])