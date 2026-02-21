# data_loader.py
import pandas as pd
import os

def load_dataset():
    """600개 전문가 레이블 데이터 로드"""
    data_path = 'data/reframing_dataset.csv'
    
    if not os.path.exists(data_path):
        print("❌ 데이터 파일이 없습니다!")
        print("👉 data/reframing_dataset.csv 파일을 다운로드하세요")
        return None
    
    df = pd.read_csv(data_path)
    print(f"✅ 데이터 로드 완료: {len(df)}개")
    print(f"📊 컬럼: {list(df.columns)}")
    
    return df

# 테스트
if __name__ == "__main__":
    df = load_dataset()
    if df is not None:
        print("\n📋 샘플 데이터:")
        print(df[['situation', 'thought', 'reframe']].head(3))