import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are FinBot, an expert AI finance assistant. You help users with:
- Stock market concepts (P/E ratio, EPS, market cap, bull/bear market, etc.)
- Personal finance (budgeting, saving, SIP, mutual funds, FD, PPF)
- Indian finance topics (NSE, BSE, SEBI, RBI, GST, ITR)
- Basic accounting (balance sheet, P&L, cash flow, journal entries)
- Investment basics (equity, debt, diversification, risk, return)

Rules:
- Keep answers short and clear (2-4 sentences max)
- Use simple language, avoid heavy jargon unless asked
- If asked about live stock prices, say you don't have real-time data
- Always be helpful and encourage financial literacy
- You can do basic financial calculations if asked
"""

def ask_ai(user_message, chat_history):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat_history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + chat_history,
        max_tokens=300,
        temperature=0.7,
    )
    reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": reply})
    return reply, chat_history