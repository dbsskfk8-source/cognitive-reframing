# attribute_control.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def increase_empathy(reframe):
    """공감 수준 높이기 (논문 원본 방식)"""
    
    prompt = f"""Make the following reframed thought more empathic.
Acknowledge feelings and provide emotional support.

Original: {reframe}
More Empathic:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        top_p=0.6
    )
    
    return response.choices[0].message.content.strip()

def increase_actionability(reframe):
    """실행가능성 높이기 (구체적 행동 추가)"""
    
    prompt = f"""Add specific actionable steps to the following reframed thought.

Original: {reframe}
More Actionable:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        top_p=0.6
    )
    
    return response.choices[0].message.content.strip()

def increase_specificity(reframe, thought, situation):
    """구체성 높이기 (상황에 더 맞게)"""
    
    prompt = f"""Make the following reframed thought more specific to the situation.

Situation: {situation}
Thought: {thought}
Reframe: {reframe}

More Specific:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        top_p=0.6
    )
    
    return response.choices[0].message.content.strip()