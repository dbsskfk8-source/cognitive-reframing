import { openai, GPT_MODEL } from './utils/openai.js';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    const { reframe, attribute, thought, situation } = req.body;

    if (!reframe || !attribute) {
        return res.status(400).json({ message: 'Reframe and attribute are required' });
    }

    let prompt = "";

    if (attribute === 'empathy') {
        prompt = `Please rewrite the following response to be more empathetic and validating of the person's feelings.
Response: "${reframe}"
More empathetic response:`;
    } else if (attribute === 'actionability') {
        prompt = `Please rewrite the following response to include more specific, actionable steps the person can take.
Response: "${reframe}"
More actionable response:`;
    } else if (attribute === 'specificity') {
        prompt = `Please rewrite the following response to be more specific to this exact situation and thought.
Situation: "${situation || 'N/A'}"
Thought: "${thought || 'N/A'}"
Response: "${reframe}"
More specific response:`;
    } else {
        return res.status(400).json({ message: 'Unknown attribute' });
    }

    try {
        const response = await openai.chat.completions.create({
            model: GPT_MODEL,
            messages: [
                { role: "system", content: "You are a helpful cognitive behavioral therapist." },
                { role: "user", content: prompt }
            ],
            max_tokens: 150,
            temperature: 0.7
        });

        const controlledReframe = response.choices[0].message.content.trim();

        // Since measure is a separate API route, we return just the reframe (frontend handles metrics if needed)
        return res.status(200).json({
            controlled_reframe: controlledReframe
        });

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ message: 'Internal Server Error' });
    }
}
