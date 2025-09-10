# Iron Lady Chatbot

A simple AI-powered chatbot built for Iron Lady’s AI & Technology internship task.

## 🚀 Tech Stack / Tools Used

### Backend:
- Python 3.10+
- FastAPI – backend framework
- Uvicorn – ASGI server
- Groq API – AI responses
- dotenv – environment variables
- CORS Middleware – allow frontend communication

### Frontend:
- React 18 + Vite
- Tailwind CSS – UI styling

## ⚡ Features
AI-powered chatbot for interactive responses
Answers FAQs about Iron Lady’s programs:
- Programs offered
- Duration
- Mode (online/offline)
- Certificates
- Mentors & coaches

## ▶️ How to Run
### Backend

1. Clone repo & navigate to backend:
   git clone https://github.com/fidafi123/IL_Chatbot.git                                                                                                                                                                                         
   cd IL_chatbot/backend
2. Create a virtual environment and activate:
3. Install dependencies:
   pip install -r requirements.txt
4. Add .env file with your API key:
   GROQ_API_KEY=your_api_key_here
5. Run FastAPI app:
   uvicorn app:app --reload

### Frontend

1. Navigate to frontend folder:
   cd ../Frontend/chatbot
2. Install dependencies:
   npm install
3. Start dev server:
   npm run dev
4. Visit your app at:
   http://localhost:5173
