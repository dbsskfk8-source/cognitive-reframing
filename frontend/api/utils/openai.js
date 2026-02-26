import OpenAI from 'openai';
import dotenv from 'dotenv';

// Load env vars in local development (Vite), Vercel automatically provides them in prod
dotenv.config();

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const GPT_MODEL = 'gpt-4o-mini';
export const EMBEDDING_MODEL = 'text-embedding-3-small';
