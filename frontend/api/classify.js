import { openai, GPT_MODEL } from './utils/openai.js';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    const { thought, situation } = req.body;

    if (!thought) {
        return res.status(400).json({ message: 'Thought is required' });
    }

    const prompt = `Here are examples of cognitive distortion classification:

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

Situation: ${situation || ''}
Thought: ${thought}
Cognitive Distortion:`;

    try {
        const response = await openai.chat.completions.create({
            model: GPT_MODEL,
            messages: [
                { role: "system", content: "You are an expert in identifying cognitive distortions." },
                { role: "user", content: prompt }
            ],
            max_tokens: 50,
            top_p: 0.6
        });

        const result = response.choices[0].message.content.trim();
        return res.status(200).json({ thinking_trap: result });
    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ message: 'Internal Server Error' });
    }
}
