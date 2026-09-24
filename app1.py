# ==========================================================
# AI Salary Prediction System
# THEME: DARK PURPLE + BLACK + YELLOW + LIGHT GRAY
# Developer: Chaitanya - CS | Data Science | AI & ML
# FIXED: Gauge color + Welcome text cleaned
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="AI Salary Prediction System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "AI Salary Prediction System"
APP_VERSION = "4.0"
DEVELOPER_NAME = "Chaitanya"
DEVELOPER_ROLE = "Computer Science | Data Science | AI & ML Engineer"
LOGO_MAIN = "🤖"
LOGO_SECOND = "📊"
LOGO_COMBO = LOGO_MAIN + LOGO_SECOND
LOGO_ACCENT = "✨"

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "history" not in st.session_state:
    st.session_state.history = []
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

def inject_css():
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
        html, body,.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
            background: #0A0015!important;
        }
      .stApp {
            background: radial-gradient(ellipse at top left, #C0C0C0 0%, #A8A8A8 10%, #1A0B2E 35%, #0A0015 65%, #000000 100%)!important;
            background-attachment: fixed!important;
            color: #F3F1EA; font-family: 'Manrope', sans-serif;
        }
        h1, h2, h3, h4 { font-family: 'Sora', sans-serif; letter-spacing: -0.3px; }
        h1 {
            background: linear-gradient(90deg, #FACC15 0%, #C0C0C0 30%, #A78BFA 60%, #7C3AED 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; font-weight: 800;
            filter: drop-shadow(0 0 18px rgba(192,192,192,0.45));
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A0B2E 0%, #151515 50%, #0F0025 100%)!important;
            border-right: 2px solid #C0C0C088;
        }
        div[data-testid="stExpander"] {
            background: linear-gradient(135deg, #1E1230 0%, #2A2A30 100%)!important;
            border: 1px solid #C0C0C066!important; border-radius: 14px;
        }
      .ai-badge {
            display: inline-flex; align-items: center; gap: 8px; padding: 7px 18px;
            border-radius: 999px;
            background: linear-gradient(90deg, #1A0B2E, #2C2C2C);
            border: 1px solid #C0C0C0AA;
            font-size: 12px; letter-spacing: 1.2px; color: #E8E8E8; margin-bottom: 14px;
            box-shadow: 0 0 12px rgba(192,192,192,0.2);
        }
      .ai-badge.dot { width: 7px; height: 7px; border-radius: 50%; background: #C0C0C0; box-shadow: 0 0 8px #C0C0C0; animation: pulseDot 1.6s infinite; }
        @keyframes pulseDot { 0%,100%{opacity:1} 50%{opacity:0.3} }
      .metric-card {
            background: linear-gradient(135deg, #1A0B2E 0%, #232326 60%, #1A1A1E 100%);
            border: 1px solid #C0C0C040; border-left: 3px solid #C0C0C0;
            border-right: 1px solid #FACC1540;
            border-radius: 18px; padding: 18px 20px; text-align: center;
            transition: transform 0.25s ease, box-shadow 0.25s ease; box-shadow: 0 4px 18px rgba(0,0,0,0.3);
        }
      .metric-card:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 16px 32px rgba(192,192,192,0.25), 0 0 20px rgba(124,58,237,0.2); border-left-color: #FACC15; }
      .metric-value { font-size: 26px; font-weight: 700; background: linear-gradient(90deg, #E8E8E8, #C0C0C0, #FACC15); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 4px 0 2px 0; }
      .metric-label { font-size: 13px; color: #C0C0C0; text-transform: uppercase; letter-spacing: 0.6px; }
      .section-card {
            background: linear-gradient(135deg, #1A0B2E 0%, #1E1E24 50%, #2A1A40 100%);
            border: 1px solid #C0C0C055; border-radius: 20px; padding: 24px 26px; margin-bottom: 22px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(192,192,192,0.1); animation: fadeIn 0.6s ease-in-out;
        }
      .salary-hero {
            background: linear-gradient(135deg, #7C3AED 0%, #2A2A2E 30%, #000000 60%, #C0C0C0 85%, #FACC15 100%);
            background-size: 250% 250%; animation: fadeIn 0.7s ease-in-out, gradientShift 6s ease infinite;
            border-radius: 22px; padding: 34px; text-align: center; color: white;
            border: 2px solid #C0C0C0; box-shadow: 0 14px 50px rgba(124,58,237,0.45), 0 0 80px rgba(192,192,192,0.35);
        }
      .salary-hero h1 { -webkit-text-fill-color: white!important; color: white!important; font-size: 46px; margin: 6px 0; filter: none; background: none!important; }
      .salary-hero p { opacity: 0.95; margin: 0; }
        @keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
      .insight-card { background: linear-gradient(90deg, #1E1230, #25252B); border-left: 4px solid #C0C0C0; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; transition: 0.2s; }
      .insight-card:hover { transform: translateX(6px); border-left-color: #FACC15; box-shadow: 0 4px 12px rgba(192,192,192,0.15); }
      .pill { display: inline-block; padding: 6px 14px; margin: 4px; border-radius: 999px; background: linear-gradient(135deg, #7C3AED33, #C0C0C033, #FACC1522); border: 1px solid #C0C0C088; color: #E8E8E8; font-size: 13px; font-weight: 500; }
      .accent-shimmer {
            background: linear-gradient(90deg, #8A8A8A, #C0C0C0, #E8E8E8, #C0C0C0, #8A8A8A);
            background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 3s linear infinite;
        }
        @keyframes shimmer { to { background-position: 200% center; } }
      .dev-card {
            background: linear-gradient(135deg, #1A0B2E, #2D2D30, #1A1A1E);
            border: 2px solid #C0C0C0; border-radius: 20px; padding: 28px;
            box-shadow: 0 0 30px rgba(192,192,192,0.15);
        }
      .app-footer { text-align: center; padding: 26px 0 10px 0; color: #A8A8A8; font-size: 13px; }
        @keyframes fadeIn { from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:translateY(0)} }
        div.stButton > button { border-radius: 12px; font-weight: 600; border: 1px solid #C0C0C055; background: #1E1E24; color: #F5F5F5; transition: all 0.2s ease; }
        div.stButton > button:hover { transform: translateY(-2px); border-color: #C0C0C0; box-shadow: 0 8px 20px rgba(192,192,192,0.35); }
        div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #7C3AED, #C0C0C0, #FACC15); border: none; color: black!important; font-weight: 800; animation: pulseBtn 2.2s ease-in-out infinite; }
        @keyframes pulseBtn { 0%,100%{box-shadow:0 0 0 0 rgba(192,192,192,0.5),0 8px 30px rgba(124,58,237,0.2)} 50%{box-shadow:0 0 0 10px rgba(192,192,192,0),0 8px 30px rgba(192,192,192,0.35)} }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-testid="stNumberInput"] input { background: #1E1E24!important; border-color: #C0C0C040!important; color: white!important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    st.sidebar.markdown(f"## {LOGO_COMBO} {APP_NAME}")
    st.sidebar.caption(f"v{APP_VERSION}")
    st.sidebar.markdown(f"<span class='accent-shimmer' style='font-weight:700; font-size:14px;'>Purple x Black x Yellow x Neutral Gray</span>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    pages = ["🏠 Home","📊 Dashboard","🤖 Salary Predictor","📈 Analytics","📋 Feature Importance","🤖 About Model","👨💻 About Developer","📞 Contact"]
    st.session_state.page = st.sidebar.radio("Navigate", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑 Clear History"):
        st.session_state.history = []
        st.sidebar.success("History cleared!")
    st.sidebar.markdown("---")
    st.sidebar.info(f"**AI Salary Prediction System**\n\n🤖 Model: XGBoost\n📊 Features: 48\n👨💻 Dev: {DEVELOPER_NAME}\n🎨 Theme: Purple + Black + Yellow")
    st.sidebar.success(f"{LOGO_COMBO} AI Prediction Ready")

@st.cache_resource(show_spinner=False)
def load_artifacts():
    model = joblib.load("salary_prediction_model.pkl")
    return model, joblib.load("job_title_encoder.pkl"), joblib.load("seniority_encoder.pkl"), joblib.load("status_encoder.pkl"), joblib.load("industry_encoder.pkl"), joblib.load("ownership_encoder.pkl")

def metric_card(col, label, value, emoji=""):
    col.markdown(f"""<div class="metric-card"><div style="font-size:22px;">{emoji}</div><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

def salary_stars(prediction):
    if prediction < 70000: return "⭐", "🔴 Entry Level Salary", "error"
    elif prediction < 120000: return "⭐⭐", "🟡 Medium Salary", "warning"
    elif prediction < 180000: return "⭐⭐⭐⭐", "🟢 High Salary", "success"
    else: return "⭐⭐⭐⭐⭐", "🏆 Excellent Salary Range", "success"

def salary_gauge(prediction):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=float(prediction),
        number={"prefix": "$", "valueformat": ",.0f", "font": {"color": "#C0C0C0"}},
        title={"text": "Predicted Annual Salary", "font": {"color": "white"}},
        gauge={
            "axis": {"range": [0, 250000], "tickcolor": "white"},
            "bar": {"color": "#C0C0C0"},
            "bgcolor": "#1A1A1E",
            "steps": [
                {"range": [0, 70000], "color": "#2D1B4E"},
                {"range": [70000, 120000], "color": "#4C1D95"},
                {"range": [120000, 180000], "color": "rgba(124, 58, 237, 0.5)"},
                {"range": [180000, 250000], "color": "rgba(192, 192, 192, 0.5)"}
            ]
        }
    ))
    fig.update_layout(height=320, margin=dict(t=50, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", font={"color":"white"})
    return fig

inject_css()
render_sidebar()

header_l, header_r = st.columns([3, 1])
with header_l:
    st.markdown(f'<div class="ai-badge"><span class="dot"></span> {LOGO_COMBO} AI SALARY INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title(f"{LOGO_MAIN} {APP_NAME}")
    st.caption(f"AI Salary Prediction — Dark Purple x Black x Yellow")
with header_r:
    st.markdown(f"""<div style="text-align:right; padding-top:10px; color:#C0C0C0;"><div style="font-size:13px;">{datetime.now().strftime("%A, %d %B %Y")}<br>{datetime.now().strftime("%I:%M %p")}</div><div style="font-size:13px; font-weight:700;" class="neutral gray-shimmer">{LOGO_COMBO} v{APP_VERSION}</div></div>""", unsafe_allow_html=True)
st.markdown("---")

try:
    model, job_title_encoder, seniority_encoder, status_encoder, industry_encoder, ownership_encoder = load_artifacts()
    model_loaded = True
except Exception as e:
    st.error("❌ Error Loading Model"); st.exception(e); st.stop()

if st.session_state.page == "🏠 Home":
    st.markdown(f"""<div class="section-card"><h3>Welcome to Neutral Gray {APP_NAME} {LOGO_COMBO}</h3><p>This dashboard predicts expected salaries for Data Science, Machine Learning and AI roles using a trained <b>XGBoost</b> model.</p><p>Built by <b style='color:#C0C0C0;'>{DEVELOPER_NAME}</b> - {DEVELOPER_ROLE}</p></div>""", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    metric_card(c1,"Total Features","48","🧩"); metric_card(c2,"Model Used","XGBoost",f"{LOGO_MAIN}"); metric_card(c3,"Prediction Status","Ready" if model_loaded else "Error","✅"); metric_card(c4,"Prediction Status","Ready","📈")
    st.info(f"👉 Go to **🤖 Salary Predictor** to run a salary prediction {LOGO_COMBO}")

elif st.session_state.page == "📊 Dashboard":
    st.header("📊 Model Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    metric_card(c1,"Total Features","48","🧩"); metric_card(c2,"Model Used","XGBoost",f"{LOGO_MAIN}"); metric_card(c3,"Prediction Status","Ready","✅"); metric_card(c4,"Algorithm","Gradient Boosting","📈")
    st.write("")
    c5,c6,c7,c8 = st.columns(4)
    metric_card(c5,"Training Accuracy","N/A","🎯"); metric_card(c6,"R² Score","N/A","📐"); metric_card(c7,"MAE","N/A","📉"); metric_card(c8,"RMSE","N/A","📊")
    st.caption("ℹ Training-time metrics are not stored in the model file.")
    if len(st.session_state.history) > 0:
        st.markdown("### 🕑 Prediction History")
        hist_df = pd.DataFrame(st.session_state.history)
        st.dataframe(hist_df, use_container_width=True)
        st.download_button("⬇ Download History as CSV", data=hist_df.to_csv(index=False).encode("utf-8"), file_name="prediction_history.csv", mime="text/csv")
    else:
        st.info("No predictions yet. Run one from the Salary Predictor page.")

elif st.session_state.page == "🤖 Salary Predictor":
    st.header(f"{LOGO_MAIN} Salary Predictor {LOGO_ACCENT}")
    with st.expander("📝 Basic Job Information", expanded=True):
        b1,b2,b3 = st.columns(3)
        with b1: job_title = st.selectbox("Job Title", job_title_encoder.classes_); seniority = st.selectbox("Seniority Level", seniority_encoder.classes_)
        with b2: status = st.selectbox("Employment Status", status_encoder.classes_); industry = st.selectbox("Industry", industry_encoder.classes_)
        with b3: ownership = st.selectbox("Company Ownership", ownership_encoder.classes_); company_size = st.number_input("Company Size (Employees)", min_value=1, max_value=1000000, value=500)
    with st.expander("💻 Technical Skills", expanded=True):
        s1,s2,s3 = st.columns(3)
        with s1:
            st.markdown("**🧑💻 Programming**"); programming_sel = st.multiselect("Programming skills", ["Python","SQL","Scala","Git"], label_visibility="collapsed")
            st.markdown("**☁ Cloud**"); cloud_sel = st.multiselect("Cloud skills", ["AWS","Azure","Docker"], label_visibility="collapsed")
        with s2:
            st.markdown("**🧠 Machine Learning**"); ml_sel = st.multiselect("ML skills", ["Machine Learning","Scikit-Learn","Statistics"], label_visibility="collapsed")
            st.markdown("**🔮 Deep Learning**"); dl_sel = st.multiselect("DL skills", ["TensorFlow","PyTorch","Deep Learning","NLP","Computer Vision"], label_visibility="collapsed")
        with s3:
            st.markdown("**📊 Visualization**"); viz_sel = st.multiselect("Visualization skills", ["Tableau","Power BI","Excel"], label_visibility="collapsed")
            st.markdown("**🗄 Big Data**"); bigdata_sel = st.multiselect("Big data skills", ["Spark","Hadoop"], label_visibility="collapsed")
        python="Python" in programming_sel; sql="SQL" in programming_sel; scala="Scala" in programming_sel; git="Git" in programming_sel
        aws="AWS" in cloud_sel; azure="Azure" in cloud_sel; docker="Docker" in cloud_sel
        machine_learning="Machine Learning" in ml_sel; scikit_learn="Scikit-Learn" in ml_sel; statistics="Statistics" in ml_sel
        tensorflow="TensorFlow" in dl_sel; pytorch="PyTorch" in dl_sel; deep_learning="Deep Learning" in dl_sel; nlp="NLP" in dl_sel; computer_vision="Computer Vision" in dl_sel
        tableau="Tableau" in viz_sel; power_bi="Power BI" in viz_sel; excel="Excel" in viz_sel
        spark="Spark" in bigdata_sel; hadoop="Hadoop" in bigdata_sel
    with st.expander("🌍 Location & Company Information", expanded=True):
        l1,l2,l3 = st.columns(3)
        with l1: country = st.selectbox("Country", ["USA","Canada","India","United Kingdom","Germany","Switzerland","Australia","Other"])
        with l2: work_mode = st.radio("Work Mode", ["Remote","Hybrid","On-site"])
        with l3: company_category = st.selectbox("Company Category", ["Startup","Small","Medium","Large","Enterprise"])
    with st.expander("🧭 Experience & Posting Details", expanded=True):
        days_since_posted = st.slider("Days Since Job Posted", min_value=1, max_value=365, value=14)

    st.markdown("---")
    job_title_encoded = job_title_encoder.transform([job_title])[0]; seniority_encoded = seniority_encoder.transform([seniority])[0]; status_encoded = status_encoder.transform([status])[0]; industry_encoded = industry_encoder.transform([industry])[0]; ownership_encoded = ownership_encoder.transform([ownership])[0]
    company_category_map = {"Startup":0,"Small":1,"Medium":2,"Large":3,"Enterprise":4}; company_category_encoded = company_category_map[company_category]
    seniority_score_map = {"Unknown":0,"junior":1,"midlevel":2,"senior":3,"lead":4}; seniority_score = seniority_score_map.get(seniority.lower(), 0)
    is_USA = 1 if country=="USA" else 0; is_International = 0 if country=="USA" else 1
    country_map = {"USA":0,"Canada":1,"India":2,"United Kingdom":3,"Germany":4,"Switzerland":5,"Australia":6,"Other":7}; country_encoded = country_map[country]
    is_remote = 1 if work_mode=="Remote" else 0; is_hybrid = 1 if work_mode=="Hybrid" else 0; is_onsite = 1 if work_mode=="On-site" else 0
    posting_category = 3 if days_since_posted<=7 else 2 if days_since_posted<=30 else 1 if days_since_posted<=90 else 0
    number_of_skills = sum([python,sql,spark,aws,azure,docker,git,scala,tableau,power_bi,excel,tensorflow,pytorch,machine_learning,deep_learning,nlp,computer_vision,statistics,scikit_learn,hadoop])
    python_sql=int(python and sql); python_aws=int(python and aws); python_spark=int(python and spark); ml_python=int(machine_learning and python); dl_python=int(deep_learning and python); senior_python=int((seniority_score>=3) and python); enterprise_python=int((company_category=="Enterprise") and python); remote_python=int(is_remote and python)

    input_data = pd.DataFrame({"job_title":[job_title_encoded],"seniority_level":[seniority_encoded],"status":[status_encoded],"headquarter":[0],"industry":[industry_encoded],"ownership":[ownership_encoded],"company_size":[0],"company_size_numeric":[company_size],"number_of_skills":[number_of_skills],"python":[int(python)],"sql":[int(sql)],"spark":[int(spark)],"aws":[int(aws)],"azure":[int(azure)],"docker":[int(docker)],"git":[int(git)],"scala":[int(scala)],"tableau":[int(tableau)],"power_bi":[int(power_bi)],"excel":[int(excel)],"tensorflow":[int(tensorflow)],"pytorch":[int(pytorch)],"machine_learning":[int(machine_learning)],"deep_learning":[int(deep_learning)],"nlp":[int(nlp)],"computer_vision":[int(computer_vision)],"statistics":[int(statistics)],"scikit-learn":[int(scikit_learn)],"hadoop":[int(hadoop)],"company_category":[company_category_encoded],"seniority_score":[seniority_score],"is_remote":[is_remote],"is_hybrid":[is_hybrid],"is_onsite":[is_onsite],"number_of_locations":[1],"days_since_posted":[days_since_posted],"posting_category":[posting_category],"country":[country_encoded],"is_USA":[is_USA],"is_International":[is_International],"python_sql":[python_sql],"python_aws":[python_aws],"python_spark":[python_spark],"ml_python":[ml_python],"dl_python":[dl_python],"senior_python":[senior_python],"enterprise_python":[enterprise_python],"remote_python":[remote_python]})

    all_skills = {"Python":python,"SQL":sql,"Spark":spark,"AWS":aws,"Azure":azure,"Docker":docker,"Git":git,"Scala":scala,"Tableau":tableau,"Power BI":power_bi,"Excel":excel,"TensorFlow":tensorflow,"PyTorch":pytorch,"Machine Learning":machine_learning,"Deep Learning":deep_learning,"NLP":nlp,"Computer Vision":computer_vision,"Statistics":statistics,"Scikit-Learn":scikit_learn,"Hadoop":hadoop}
    selected_skills=[k for k,v in all_skills.items() if v]
    skill_categories = {"Programming":["Python","SQL","Scala","Git"],"Cloud":["AWS","Azure","Docker"],"Machine Learning":["Machine Learning","Scikit-Learn","Statistics"],"Deep Learning":["TensorFlow","PyTorch","Deep Learning","NLP","Computer Vision"],"Visualization":["Tableau","Power BI","Excel"],"Big Data":["Spark","Hadoop"]}
    if selected_skills: st.markdown("**Selected Skills:** "+" ".join(f'<span class="pill">{s}</span>' for s in selected_skills), unsafe_allow_html=True)
    else: st.caption("No skills selected yet.")
    st.markdown("---")
    predict_col, reset_col = st.columns([3,1])
    predict_clicked = predict_col.button(f"{LOGO_MAIN} Predict Salary {LOGO_ACCENT}", use_container_width=True, type="primary")
    reset_clicked = reset_col.button("🔄 Reset Form", use_container_width=True)
    if reset_clicked: st.rerun()
    if predict_clicked:
        progress = st.progress(0, text="Polishing neutral gray features...")
        for pct,label in [(25,"Encoding Neutral Gray..."),(55,"Forging Features..."),(80,"Scoring with XGBoost Neutral Gray..."),(100,"Final Shine...")]:
            time.sleep(0.15); progress.progress(pct, text=label)
        with st.spinner("Computing..."):
            time.sleep(0.2); prediction = model.predict(input_data)[0]
        progress.empty(); st.success("✅ Salary Prediction Completed!")
        stars,level_label,level_kind = salary_stars(prediction)
        st.markdown(f"""<div class="salary-hero"><p>Estimated Neutral Gray Professional Salary</p><h1>${prediction:,.0f}</h1><p>{stars} &nbsp; {level_label} {LOGO_COMBO}</p></div>""", unsafe_allow_html=True)
        if prediction>=180000: st.balloons()
        st.session_state.history.append({"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M"),"job_title":job_title,"seniority":seniority,"industry":industry,"country":country,"company_size":company_size,"num_skills":number_of_skills,"predicted_salary":round(float(prediction),2),"level":level_label})
        st.session_state.last_prediction = {"prediction":float(prediction),"job_title":job_title,"seniority":seniority,"status":status,"industry":industry,"ownership":ownership,"country":country,"work_mode":work_mode,"company_size":company_size,"number_of_skills":number_of_skills,"selected_skills":selected_skills}
        st.plotly_chart(salary_gauge(prediction), use_container_width=True)
        comp_fig = go.Figure(data=[go.Bar(x=["Low Avg","Market Avg","Your Prediction","High Avg"], y=[50000,110000,prediction,200000], marker_color=["#2D1B4E","#4C1D95","#C0C0C0","#FACC15"])])
        comp_fig.update_layout(title="Salary Comparison (AI Salary Prediction)", yaxis_title="USD", height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(comp_fig, use_container_width=True)
        chart_c1, chart_c2 = st.columns(2)
        with chart_c1:
            if selected_skills:
                pie_fig = px.pie(names=selected_skills, values=[1]*len(selected_skills), title="Selected Skills", hole=0.3, color_discrete_sequence=["#C0C0C0","#7C3AED","#FACC15","#A78BFA","#E8E8E8"])
                pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(pie_fig, use_container_width=True)
        with chart_c2:
            if selected_skills:
                bar_fig = px.bar(x=selected_skills, y=[1]*len(selected_skills), title="Selected Technologies", labels={"x":"Skill","y":""}, color=selected_skills, color_discrete_sequence=["#C0C0C0","#7C3AED","#FACC15","#A78BFA"]*7)
                bar_fig.update_yaxes(visible=False); bar_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(bar_fig, use_container_width=True)
        chart_c3, chart_c4 = st.columns(2)
        with chart_c3:
            radar_categories=list(skill_categories.keys()); radar_values=[sum(all_skills[s] for s in skill_categories[cat]) for cat in radar_categories]
            radar_fig=go.Figure(); radar_fig.add_trace(go.Scatterpolar(r=radar_values+[radar_values[0]], theta=radar_categories+[radar_categories[0]], fill="toself", name="Skill Profile", line=dict(color="#C0C0C0"), fillcolor="rgba(192,192,192,0.25)"))
            radar_fig.update_layout(title="Skill Profile (Skill Profile)", height=380, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white")); st.plotly_chart(radar_fig, use_container_width=True)
        with chart_c4:
            donut_fig = px.pie(names=radar_categories, values=[max(v,0.0001) for v in radar_values], title="Skill Categories", hole=0.55, color_discrete_sequence=["#C0C0C0","#7C3AED","#FACC15","#A78BFA","#E8E8E8","#2D1B4E"])
            donut_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
            st.plotly_chart(donut_fig, use_container_width=True)
        st.markdown("### 📋 Prediction Summary")
        sum_c1,sum_c2=st.columns(2)
        with sum_c1: st.write(f"**Job Title:** {job_title}"); st.write(f"**Seniority:** {seniority}"); st.write(f"**Status:** {status}"); st.write(f"**Industry:** {industry}")
        with sum_c2: st.write(f"**Ownership:** {ownership}"); st.write(f"**Country:** {country}"); st.write(f"**Work Mode:** {work_mode}"); st.write(f"**Company Size:** {company_size:,}")
        st.write(f"**Number of Skills:** {number_of_skills}"); st.write(f"**Salary Level:** {level_label}")
        st.markdown("### 🧠 Neutral Gray AI Insights")
        insights=[]
        if python: insights.append(f"{LOGO_MAIN} Python is the strongest salary driver - advanced skill.")
        if machine_learning or deep_learning: insights.append("🤖 ML/DL + AI/ML Stack = Premium Salary.")
        if company_category=="Enterprise": insights.append("🏢 Enterprise + AI Salary Prediction companies pay top 10%.")
        if is_remote: insights.append("🌐 Remote roles carry highest competitive bands.")
        if seniority_score>=3: insights.append("📈 Senior/Lead is major positive factor for AI Salary Prediction.")
        if number_of_skills>=8: insights.append("📊 Broad skill set can support higher predicted pay.")
        if not insights: insights.append("ℹ Add more skills for richer AI insights.")
        for tip in insights: st.markdown(f'<div class="insight-card" style="color:white;">{tip}</div>', unsafe_allow_html=True)
        st.markdown("### ⬇ Export Results")
        exp_c1,exp_c2=st.columns(2)
        summary_df=pd.DataFrame([{"job_title":job_title,"seniority":seniority,"status":status,"industry":industry,"ownership":ownership,"country":country,"work_mode":work_mode,"company_size":company_size,"number_of_skills":number_of_skills,"predicted_salary":round(float(prediction),2),"salary_level":level_label}])
        with exp_c1: st.download_button("⬇ Download Prediction (CSV)", data=summary_df.to_csv(index=False).encode("utf-8"), file_name="salary_prediction.csv", mime="text/csv", use_container_width=True)
        with exp_c2:
            report_text=f"{APP_NAME} SALARY PREDICTION REPORT\nGenerated: {datetime.now()}\nJob: {job_title}\nSeniority: {seniority}\nCountry: {country}\nWork Mode: {work_mode}\nSkills: {', '.join(selected_skills)}\nSalary: ${prediction:,.2f}\nLevel: {level_label}\nTheme: Dark Purple + Black + Yellow {LOGO_COMBO}\nDev: {DEVELOPER_NAME} - {DEVELOPER_ROLE}"
            st.download_button("⬇ Download Report (TXT)", data=report_text.encode("utf-8"), file_name="salary_prediction_report.txt", mime="text/plain", use_container_width=True)

elif st.session_state.page == "📈 Analytics":
    st.header("📈 Salary Analytics")
    if st.session_state.last_prediction is None:
        st.info(f"Run a prediction first on **🤖 Salary Predictor** {LOGO_COMBO}")
    else:
        lp=st.session_state.last_prediction
        size_fig=go.Figure(); size_fig.add_trace(go.Bar(x=["Startup","Small","Medium","Large","Enterprise","Your Input"], y=[50,200,1000,5000,20000,lp["company_size"]], marker_color=["#4C1D95"]*5+["#C0C0C0"]))
        size_fig.update_layout(title="Company Size Reference (Neutral Gray)", yaxis_title="Employees", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(size_fig, use_container_width=True)
        mode_fig=px.pie(names=["Remote","Hybrid","On-site"], values=[1 if lp["work_mode"]=="Remote" else 0.3, 1 if lp["work_mode"]=="Hybrid" else 0.3, 1 if lp["work_mode"]=="On-site" else 0.3], title="Work Mode Emphasis", color_discrete_sequence=["#C0C0C0","#7C3AED","#1A0B2E"])
        st.plotly_chart(mode_fig, use_container_width=True)
    if len(st.session_state.history)>1:
        hist_df=pd.DataFrame(st.session_state.history); trend_fig=px.line(hist_df, x="timestamp", y="predicted_salary", markers=True, title="Predicted Salary Trend - Neutral Gray", line_shape="spline", color_discrete_sequence=["#C0C0C0"])
        trend_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(trend_fig, use_container_width=True)

elif st.session_state.page == "📋 Feature Importance":
    st.header("📋 Feature Importance")
    try:
        importances=model.feature_importances_; feat_names=getattr(model,"feature_names_in_",None)
        if feat_names is None: feat_names=[f"feature_{i}" for i in range(len(importances))]
        imp_df=pd.DataFrame({"feature":feat_names,"importance":importances}).sort_values("importance",ascending=False).head(20)
        fig=px.bar(imp_df.sort_values("importance"), x="importance", y="feature", orientation="h", title="Top 20 Feature Importances - AI Salary Prediction", color="importance", color_continuous_scale=["#1A0B2E","#7C3AED","#C0C0C0","#E8E8E8"])
        fig.update_layout(height=600, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    except AttributeError:
        st.warning("Model does not expose feature_importances_")

elif st.session_state.page == "🤖 About Model":
    st.header("🤖 About the AI Model")
    st.markdown(f"""<div class="section-card"><ul><li><b>Algorithm:</b> XGBoost (Configured)</li><li><b>Theme:</b> Dark Purple #1A0B2E + Black #000000 + Yellow #FACC15 + <b>Neutral Gray #C0C0C0</b></li><li><b>Task:</b> Regression — predicting annual salary (USD)</li><li><b>Features:</b> 48 engineered features</li><li><b>Logo:</b> {LOGO_COMBO} Neutral Gray Crown Professional</li><li><b>Version:</b> {APP_VERSION}</li></ul></div>""", unsafe_allow_html=True)

elif st.session_state.page == "👨💻 About Developer":
    st.header("👨💻 About Developer")
    st.markdown(f"""
    <div class="dev-card">
        <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
            <div style="font-size:72px; background: linear-gradient(135deg, #C0C0C0, #7C3AED); width:110px; height:110px; border-radius:50%; display:flex; align-items:center; justify-content:center; border:3px solid #FACC15; box-shadow: 0 0 20px rgba(192,192,192,0.4);">🤖</div>
            <div>
                <h2 style="margin:0; background:none; -webkit-text-fill-color: white; color:white;">{DEVELOPER_NAME}</h2>
                <p style="margin:4px 0; color:#C0C0C0; font-size:16px; font-weight:600; letter-spacing:0.5px;">{DEVELOPER_ROLE}</p>
                <p style="margin:4px 0; color:#A78BFA;">Founder of TechSalaryPredictor | AI Salary Prediction Architect</p>
            </div>
        </div>
        <hr style="border-color:#C0C0C030; margin:22px 0;">
        <h3 class="neutral gray-shimmer" style="font-size:20px;">Who Am I?</h3>
        <p style="line-height:1.7; color:#E8E8E8; font-size:15px;">
        I am <b style="color:#FACC15;">CHAITANYA</b>, a passionate <b>Computer Science Graduate</b> and a dedicated <b>Data Science, Artificial Intelligence and Machine Learning Engineer</b> from India.
        I build intelligent systems that turn data into wealth and predictions into power. My expertise lies at the intersection of <b>Software Engineering, Data Analytics, and AI</b>.
        </p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:14px; margin-top:18px;">
            <div class="insight-card"><b style="color:#C0C0C0;">🎓 Education</b><br>B.Tech Computer Science<br>Specialization in AI & ML</div>
            <div class="insight-card"><b style="color:#FACC15;">💼 Core Skills</b><br>Python, XGBoost, TensorFlow, PyTorch, Scikit-Learn, Streamlit, SQL, Power BI</div>
            <div class="insight-card"><b style="color:#A78BFA;">🚀 Focus Areas</b><br>Salary Prediction, ML Ops, Deep Learning, NLP, Computer Vision, Generative AI</div>
            <div class="insight-card"><b style="color:#C0C0C0;">🤖 Mission</b><br>To democratize AI salary intelligence with professional design and production-grade ML.</div>
        </div>
        <div style="margin-top:20px;">
            <span class="pill">Computer Science</span><span class="pill">Data Science</span><span class="pill">AI Engineer</span><span class="pill">ML Engineer</span><span class="pill">Python Expert</span><span class="pill">XGBoost</span><span class="pill">Streamlit</span><span class="pill">Technical Skillseveloper</span>
        </div>
        <hr style="border-color:#C0C0C030; margin:22px 0;">
        <p style="color:#A8A8A8;">📍 Project Developer | AI/ML Developer</p>
        <p>🔗 GitHub: github.com/chaitanya6512 | 🔗 LinkedIn: linkedin.com/in/chaitanya-yaragalla-7baa21243 | ✉ Email: yaragallachaitanya@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "📞 Contact":
    st.header("📞 Contact Support")
    st.markdown("""<div class="section-card"><p>Have feedback for AI Salary Prediction System?</p><p>Built with AI/ML by <b>Chaitanya</b></p><p>✉ Email: yaragallachaitanya@gmail.com<br>💬 GitHub Issues: Add your repo link</p></div>""", unsafe_allow_html=True)
    with st.form("contact_form"):
        name=st.text_input("Name"); email=st.text_input("Email"); message=st.text_area("Message"); submitted=st.form_submit_button(f"Send Neutral Gray {LOGO_MAIN}", type="primary")
        if submitted: st.success(f"✅ Thanks {name}! AI Salary Prediction team will reply {LOGO_ACCENT}")

st.markdown("---")
