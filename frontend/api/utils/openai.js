import OpenAI from 'openai';

// Vercel 환경에서는 process.env가 바로 제공되므로 dotenv.config()를 생략하거나 조건부로 실행
// 로컬 개발 시에만 dotenv가 필요할 수 있음
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

if (!process.env.OPENAI_API_KEY) {
  console.warn('⚠️ WARNING: OPENAI_API_KEY is not defined in environment variables.');
}

export const GPT_MODEL = 'gpt-4o-mini';
export const EMBEDDING_MODEL = 'text-embedding-3-small';
