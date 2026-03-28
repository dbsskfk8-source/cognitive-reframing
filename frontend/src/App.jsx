import { useState } from 'react';
import axios from 'axios';

function App() {
  const [step, setStep] = useState(1);
  const [thought, setThought] = useState('');
  const [situation, setSituation] = useState('');
  const [thinkingTrap, setThinkingTrap] = useState('');
  const [reframes, setReframes] = useState([]);
  const [selectedReframe, setSelectedReframe] = useState('');
  const [similarCases, setSimilarCases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');



  const API_BASE = '/api';

  const handleInputNext = () => {
    if (!thought.trim()) {
      setError('생각을 입력해주세요');
      return;
    }
    if (!situation.trim()) {
      setError('상황을 입력해주세요');
      return;
    }
    setError('');
    setStep(2);
    classifyThinkingTrap();
  };

  const classifyThinkingTrap = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/classify`, {
        thought,
        situation
      });
      setThinkingTrap(response.data.thinking_trap);
      setStep(3);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError('분류 중 오류가 발생했습니다: ' + msg);
    } finally {
      setLoading(false);
    }
  };

  const generateReframe = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/reframe`, {
        thought,
        situation
      });

      setReframes(response.data.reframes);  // 3개 저장
      setSimilarCases(response.data.similar_cases || []);
      setStep(4);
    } catch (err) {
      setError('재구성 생성 중 오류: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(1);
    setThought('');
    setSituation('');
    setThinkingTrap('');
    setSelectedReframe('');
    setSimilarCases([]);
    setError('');
  };

  const handleControl = async (attribute) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/control`, {
        reframe: selectedReframe,
        attribute,
        thought,
        situation
      });

      setSelectedReframe(response.data.controlled_reframe);

      // reframes 배열도 업데이트
      const newReframes = [...reframes];
      const idx = newReframes.indexOf(selectedReframe);
      if (idx !== -1) {
        newReframes[idx] = response.data.controlled_reframe;
        setReframes(newReframes);
      }
    } catch (err) {
      setError('속성 제어 중 오류: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: '800px',
      margin: '50px auto',
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ textAlign: 'center', color: '#2563eb' }}>
        🧠 인지 재구성 도구
      </h1>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
        부정적인 생각을 건강한 관점으로 바꿔보세요
      </p>

      {error && (
        <div style={{
          padding: '15px',
          marginBottom: '20px',
          backgroundColor: '#fee2e2',
          border: '1px solid #ef4444',
          borderRadius: '8px',
          color: '#dc2626'
        }}>
          ⚠️ {error}
        </div>
      )}

      {step === 1 && (
        <div>
          <h2>1️⃣ 어떤 생각 때문에 힘드신가요?</h2>

          <label style={{ display: 'block', marginTop: '20px', fontWeight: 'bold' }}>
            부정적인 생각:
          </label>
          <textarea
            value={thought}
            onChange={(e) => setThought(e.target.value)}
            placeholder="예: 나는 절대 성공하지 못할 거야"
            style={{
              width: '100%',
              minHeight: '100px',
              padding: '12px',
              fontSize: '16px',
              border: '2px solid #e5e7eb',
              borderRadius: '8px',
              marginTop: '8px'
            }}
          />

          <label style={{ display: 'block', marginTop: '20px', fontWeight: 'bold' }}>
            어떤 상황이었나요?
          </label>
          <textarea
            value={situation}
            onChange={(e) => setSituation(e.target.value)}
            placeholder="예: 프로젝트 발표가 잘 안됐다"
            style={{
              width: '100%',
              minHeight: '100px',
              padding: '12px',
              fontSize: '16px',
              border: '2px solid #e5e7eb',
              borderRadius: '8px',
              marginTop: '8px'
            }}
          />

          <button
            onClick={handleInputNext}
            style={{
              marginTop: '20px',
              padding: '12px 30px',
              fontSize: '16px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            다음 단계 →
          </button>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '20px' }}>🔍</div>
          <h2>사고함정 분석 중...</h2>
          <p style={{ color: '#666' }}>AI가 당신의 생각 패턴을 분석하고 있습니다</p>
        </div>
      )}

      {step === 3 && (
        <div>
          <h2>2️⃣ 사고함정 분석 결과</h2>

          <div style={{
            padding: '20px',
            backgroundColor: '#fef3c7',
            border: '2px solid #f59e0b',
            borderRadius: '8px',
            marginTop: '20px'
          }}>
            <h3 style={{ marginTop: 0 }}>감지된 사고함정:</h3>
            <p style={{ fontSize: '20px', fontWeight: 'bold', color: '#d97706' }}>
              {thinkingTrap}
            </p>
          </div>

          <div style={{
            marginTop: '20px',
            padding: '15px',
            backgroundColor: '#f3f4f6',
            borderRadius: '8px'
          }}>
            <p><strong>당신의 생각:</strong> "{thought}"</p>
            <p><strong>상황:</strong> "{situation}"</p>
          </div>

          <button
            onClick={generateReframe}
            disabled={loading}
            style={{
              marginTop: '20px',
              padding: '12px 30px',
              fontSize: '16px',
              backgroundColor: loading ? '#9ca3af' : '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {loading ? '재구성 생성 중...' : '재구성 생성 →'}
          </button>
        </div>
      )}

      {step === 4 && (
        <div>
          <h2>3️⃣ 재구성 제안</h2>
          <p style={{ color: '#666' }}>가장 마음에 드는 재구성을 선택해주세요</p>

          <div style={{ marginTop: '20px' }}>
            {reframes.map((reframe, idx) => (
              <div
                key={idx}
                onClick={() => setSelectedReframe(reframe)}
                style={{
                  padding: '20px',
                  marginBottom: '15px',
                  backgroundColor: selectedReframe === reframe ? '#d1fae5' : '#f9fafb',
                  border: selectedReframe === reframe ? '3px solid #10b981' : '2px solid #e5e7eb',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{
                    fontSize: '20px',
                    fontWeight: 'bold',
                    color: selectedReframe === reframe ? '#047857' : '#6b7280',
                    marginRight: '10px'
                  }}>
                    {selectedReframe === reframe ? '✅' : `${idx + 1}.`}
                  </span>
                </div>
                <div style={{
                  maxHeight: '150px',
                  overflowY: 'auto',
                  padding: '12px',
                  backgroundColor: 'white',
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb',
                  wordBreak: 'break-word'
                }}>
                  <p style={{
                    fontSize: '16px',
                    lineHeight: '1.6',
                    color: '#374151',
                    margin: 0
                  }}>
                    {reframe}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {selectedReframe && (
            <div style={{ marginTop: '30px' }}>
              <h3>🎛️ 선택한 재구성 조절하기</h3>
              <p style={{ color: '#666', fontSize: '14px', marginBottom: '15px' }}>
                속성을 조절하여 더 나은 재구성을 만들어보세요
              </p>

              <div style={{
                display: 'flex',
                gap: '10px',
                flexWrap: 'wrap'
              }}>
                <button
                  onClick={() => handleControl('empathy')}
                  disabled={loading}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: loading ? '#9ca3af' : '#8b5cf6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: loading ? 'not-allowed' : 'pointer'
                  }}
                >
                  💜 더 공감적으로
                </button>

                <button
                  onClick={() => handleControl('actionability')}
                  disabled={loading}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: loading ? '#9ca3af' : '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: loading ? 'not-allowed' : 'pointer'
                  }}
                >
                  ⚡ 더 실행 가능하게
                </button>

                <button
                  onClick={() => handleControl('specificity')}
                  disabled={loading}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: loading ? '#9ca3af' : '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: loading ? 'not-allowed' : 'pointer'
                  }}
                >
                  🎯 더 구체적으로
                </button>
              </div>
            </div>
          )}

          <div style={{ marginTop: '30px', textAlign: 'center' }}>
            <button
              onClick={reset}
              style={{
                padding: '12px 30px',
                fontSize: '16px',
                backgroundColor: '#6b7280',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer'
              }}
            >
              🔄 다시 시작
            </button>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;