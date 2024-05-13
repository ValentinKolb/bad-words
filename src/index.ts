import express from 'express';
import {checkProfanity} from "@/lib";

const app = express();
const PORT = 3000;

app.use(express.json());

app.post('/check', (req, res) => {
    try {
        const {text} = req.body
        res.json({
            contains_profanity: checkProfanity(text)
        })
    } catch (e) {
        res.status(400).json({
            error: 'Invalid request'
        })
    }
})

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
})