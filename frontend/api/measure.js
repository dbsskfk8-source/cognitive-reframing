import { openai, EMBEDDING_MODEL } from './utils/openai.js';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    const { reframe, thought, situation } = req.body;

    if (!reframe || !thought) {
        return res.status(400).json({ message: 'Reframe and thought are required' });
    }

    try {
        // 1. Specificity (Cosine Similarity via OpenAI embeddings)
        let specificity = 0;
        try {
            const context = `${thought} ${situation || ''}`;
            const response = await openai.embeddings.create({
                model: EMBEDDING_MODEL,
                input: [reframe, context]
            });

            const embReframe = response.data[0].embedding;
            const embContext = response.data[1].embedding;

            // Calculate dot product (cosine similarity since OpenAI embeddings are normalized)
            specificity = embReframe.reduce((sum, val, i) => sum + val * embContext[i], 0);
        } catch (embError) {
            console.error('Embedding error for specificity:', embError);
            specificity = 0.5; // fallback
        }

        // 2. Actionability
        const actionPatterns = ['can', 'will', 'could', 'should', 'try', 'start', 'practice', 'focus', 'work', 'plan', '하자', '해보자', '할 수 있다', '하겠다', '시작하다'];
        let actionScore = actionPatterns.filter(p => new RegExp(p, 'i').test(reframe)).length;
        const actionability = Math.min(actionScore / 3.0, 1.0);

        // 3. Empathy
        const empathyKeywords = ['understand', 'feel', 'okay', 'normal', 'valid', '이해', '괜찮', '힘들', '당연', '자연스러운'];
        let empathyScore = empathyKeywords.filter(k => reframe.toLowerCase().includes(k)).length;
        const empathy = Math.min(empathyScore / 3.0, 1.0);

        // 4. Positivity
        const positiveWords = ['can', 'will', 'able', 'succeed', 'good', 'better', 'improve', '할 수 있', '잘', '개선', '성장', '가능'];
        let posScore = positiveWords.filter(w => reframe.toLowerCase().includes(w)).length;
        const positivity = Math.min(posScore / 4.0, 1.0);

        return res.status(200).json({
            specificity: Number(specificity.toFixed(3)),
            actionability: Number(actionability.toFixed(3)),
            empathy: Number(empathy.toFixed(3)),
            positivity: Number(positivity.toFixed(3))
        });

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ message: 'Internal Server Error' });
    }
}
