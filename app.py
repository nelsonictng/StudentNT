import streamlit as st
import re
from fpdf import FPDF
from database import init_db
from auth_lib import login, handle_callback
from ai_engine import generate_learning_stream
from services import register_user_if_not_exists, save_user_topic, get_user_topics_list
from models import is_admin, save_topic

init_db()
st.set_page_config(page_title="Nutrition Learning Platform", layout="wide")

handle_callback()

if "user" not in st.session_state:
    login()
    st.stop()

user = st.session_state["user"]
register_user_if_not_exists(user)

# --- PDF Certificate Generator ---
def create_pdf_certificate(user_name, topic_name):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_line_width(2)
    pdf.rect(10, 10, 277, 190)
    
    pdf.set_font('Arial', 'B', 34)
    pdf.cell(0, 50, 'Certificate of Completion', ln=True, align='C')
    pdf.set_font('Arial', '', 18)
    pdf.cell(0, 15, 'This award is presented to', ln=True, align='C')
    pdf.set_font('Arial', 'B', 28)
    pdf.cell(0, 25, user_name, ln=True, align='C')
    pdf.set_font('Arial', '', 18)
    pdf.cell(0, 15, f'for mastering the topic of {topic_name}', ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- Interactive Quiz Engine ---
def render_quiz(content, topic_name, topic_id):
    q_blocks = re.findall(r"Q: (.*?)\nA\) (.*?)\nB\) (.*?)\nC\) (.*?)\nD\) (.*?)\nAnswer: ([A-D])", content, re.S)
    
    if q_blocks:
        st.divider()
        st.subheader("📝 Quiz & Assessment")
        
        score_key = f"score_{topic_id}"
        if score_key not in st.session_state:
            st.session_state[score_key] = {}

        for i, (q, a, b, c, d, ans) in enumerate(q_blocks):
            st.write(f"**Q{i+1}: {q}**")
            options = [f"A) {a}", f"B) {b}", f"C) {c}", f"D) {d}"]
            u_choice = st.radio("Select answer:", options, key=f"r_{topic_id}_{i}")
            
            if st.button(f"Submit Answer {i+1}", key=f"b_{topic_id}_{i}"):
                if u_choice.startswith(ans):
                    st.success("Correct!")
                    st.session_state[score_key][i] = True
                else:
                    st.error(f"Incorrect. Correct answer: {ans}")
                    st.session_state[score_key][i] = False

        final_score = sum(st.session_state[score_key].values())
        total = len(q_blocks)
        st.metric("Total Score", f"{final_score} / {total}")
        
        if final_score == total:
            st.balloons()
            cert = create_pdf_certificate(user['name'], topic_name)
            st.download_button("🎓 Download Certificate", cert, f"{topic_name}_cert.pdf", "application/pdf")

# --- Sidebar Navigation ---
user_is_admin = is_admin(user["email"])
nav_items = ["Generate", "My Topics"]
if user_is_admin: nav_items.append("Admin Panel")
menu = st.sidebar.selectbox("Navigation", nav_items)

if menu == "Generate":
    st.title("🌱 New Lesson")
    c1, c2 = st.columns(2)
    country = c1.text_input("Country")
    topic = c2.text_input("Nutrition Topic")

    if st.button("Generate Lesson"):
        if country and topic:
            full_text = ""
            p = st.empty() # Create a placeholder
            
            # The fix in ai_engine.py now prevents the crash here
            for chunk in generate_learning_stream(country, topic):
                full_text += chunk
                p.markdown(full_text) # Update placeholder with streamed text
                
            save_user_topic(user, country, topic, full_text)
            render_quiz(full_text, topic, "new")

elif menu == "My Topics":
    st.title("📚 Your Library")
    for idx, t in enumerate(get_user_topics_list(user)):
        with st.expander(f"{'🌟' if t[3] else '📖'} {t[0]} ({t[2]})"):
            st.markdown(t[1])
            if "Answer:" in t[1]:
                render_quiz(t[1], t[0], f"old_{idx}")

elif menu == "Admin Panel":
    st.title("🛡️ Admin Dashboard")
    with st.form("admin_lesson"):
        target = st.text_input("Country/Global")
        title = st.text_input("Title")
        body = st.text_area("Lesson Content", height=250)
        if st.form_submit_button("Publish Global Lesson"):
            save_topic("admin-system", target, title, body, is_global=1)
            st.success("Published!")