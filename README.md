# 🥗 NutritionAI: Localized Learning & Certification Platform

**NutritionAI** is a high-performance educational tool designed to bridge the nutritional knowledge gap for students and examination centers across West Africa. By leveraging Generative AI, the platform transforms complex health data into culturally relevant lessons and provides instant validation through interactive quizzes and automated certification.

## 🚀 Features
* **Localized Content Engine:** Generates lessons using regional food examples (e.g., Jollof, Egusi, Kenkey) to ensure cultural resonance.
* **Hybrid TTS Engine:** A browser-based Text-to-Speech system that provides accessible audio lessons for all learning types.
* **Interactive Quiz System:** A robust, regex-powered assessment tool that validates student knowledge in real-time.
* **Automated Certification:** Generates professional PDF certificates upon successful completion of topics using `fpdf`.
* **Secure Authentication:** Enterprise-grade login and user management powered by **Auth0**.
* **Admin Control:** A dedicated panel for experts to draft, refine, and publish global lessons to thousands of users.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI:** OpenAI-compatible LLMs via Featherless.ai
* **Database:** SQLite (with migration paths to PostgreSQL/Supabase)
* **Auth:** Auth0 (OAuth2)
* **Audio:** Web Speech API (JavaScript Injection)
* **PDF Generation:** FPDF2

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/edunelsonit/NutritionAI.git](https://github.com/edunelsonit/NutritionAI.git)
   cd NutritionAI
2. **Install Dependencies:**
    ```bash
    pip install streamlit openai python-dotenv authlib requests fpdf2

3. **Configure Environment Variables:**
    ```Text
    OPENAI_API_KEY=your_key
    OPENAI_BASE_URL=[https://api.featherless.ai/v1](https://api.featherless.ai/v1)
    OPENAI_MODEL=your_model_choice
    AUTH0_DOMAIN=your_domain
    AUTH0_CLIENT_ID=your_id
    AUTH0_CLIENT_SECRET=your_secret
    AUTH0_CALLBACK_URL=http://localhost:8501
4. **Test Completed Project:**
    ```
    https://nutritionaing.streamlit.app/
5. **Run the Application**
    ```bash
    streamlit run app.py