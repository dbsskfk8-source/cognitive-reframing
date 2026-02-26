import { openai, GPT_MODEL } from './utils/openai.js';
import fs from 'fs';
import path from 'path';
import stringSimilarity from 'string-similarity';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    const { thought, situation, k = 5 } = req.body;

    if (!thought) {
        return res.status(400).json({ message: 'Thought is required' });
    }

    try {
        // 1. Retrieval
        // Vercel Serverless environment: read local JSON file
        const dataPath = path.resolve(process.cwd(), 'data', 'dataset.json');
        let dataset = [];
        if (fs.existsSync(dataPath)) {
            dataset = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        } else {
            console.warn('dataset.json not found at:', dataPath);
        }

        let similarCases = [];
        if (dataset.length > 0) {
            // Create search space combining thought + situation
            const searchSpace = dataset.map(item => `${item.thought} ${item.situation}`);
            const query = `${thought} ${situation || ''}`;

            // Calculate string similarity instead of Heavy ML Cosine Similarity
            const matches = stringSimilarity.findBestMatch(query, searchSpace);

            // Sort and get top K indices
            const sortedMatches = matches.ratings
                .map((rating, index) => ({ rating: rating.rating, index }))
                .sort((a, b) => b.rating - a.rating)
                .slice(0, k);

            similarCases = sortedMatches.map(match => dataset[match.index]);
        }

        // Shuffle the retrieved cases as done in the original Python logic
        similarCases.sort(() => Math.random() - 0.5);

        // 2. Generation Prompt Setup
        let prompt = "";
        for (const caseObj of similarCases) {
            prompt += `Situation: ${caseObj.situation}\n`;
            prompt += `Distorted Thought: ${caseObj.thought}\n`;
            prompt += `Rational Response: ${caseObj.reframe}\n\n`;
        }

        const testInput = `Situation: ${situation || ''}\nDistorted Thought: ${thought}\nRational Response:`;

        const reframes = [];

        // Generate 3 reframes concurrently
        const promises = Array.from({ length: 3 }).map(() =>
            openai.chat.completions.create({
                model: GPT_MODEL,
                messages: [
                    { role: "system", content: "You are a cognitive therapist helping people reframe negative thoughts." },
                    { role: "user", content: prompt + testInput }
                ],
                max_tokens: 256,
                top_p: 0.6,
                frequency_penalty: 0.0,
                presence_penalty: 0.0
            })
        );

        const responses = await Promise.all(promises);
        responses.forEach(response => {
            reframes.push(response.choices[0].message.content.trim());
        });

        return res.status(200).json({
            reframes,
            similar_cases: similarCases,
            retrieved_k: k
        });

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ message: 'Internal Server Error' });
    }
}
