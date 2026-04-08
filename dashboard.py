import streamlit as st
import pandas as pd

# Page Config for that "Ultra Wide" Monitor look
st.set_page_config(layout="wide", page_title="Gold Hunter AI")

# --- CUSTOM NEON CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050517; }
    [data-testid="stVerticalBlock"] { 
        background-color: #0b0b28; 
        border: 1px solid #1f1f4e; 
        border-radius: 10px; 
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 199, 255, 0.1);
    }
    h1, h2, h3 { color: #00c7ff !important; text-shadow: 0 0 10px #00c7ff; }
    .stMetric { background: #151d3a; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_index=True)

# --- LAYOUT ---
# We create two main columns: Left (Small) and Right (Large)
col_left, col_right = st.columns([1, 3])

with col_left:
    st.image("https://img.icons8.com/fluency/144/rocket.png") # Rocket icon
    st.title("BOT ACTIVE")
    st.success("RUNNING")
    
    st.metric(label="Total Profit (24h)", value="+4.2%", delta="0.5%")
    st.metric(label="Active Trades", value="3")
    
    # Glow Buttons
    if st.button("▶️ START BOT"):
        st.write("Bot Started")
    if st.button("⏹️ STOP BOT"):
        st.write("Bot Stopped")
    
    st.subheader("Market Analysis")
    st.line_chart([10, 15, 12, 18, 20]) # Mini chart

with col_right:
    # Top Main Chart
    st.subheader("XAUUSD / GOLD - M15 Chart")
    chart_data = pd.DataFrame({'Price': [2030, 2035, 2032, 2038, 2040]})
    st.area_chart(chart_data)
    
    # Middle Tables
    t1, t2 = st.columns(2)
    with t1:
        st.write("### Open Trades")
        st.table(pd.DataFrame({'Symbol': ['XAUUSD'], 'Type': ['Buy'], 'Profit': ['+ $45.00']}))
    with t2:
        st.write("### Past Trades")
        st.table(pd.DataFrame({'Symbol': ['XAUUSD'], 'Type': ['Sell'], 'Profit': ['- $10.00']}))

    # Bottom Settings/Balance
    b1, b2 = st.columns(2)
    with b1:
        st.write("### Portfolio Balance")
        st.info("Balance: $34,306,297")
    with b2:
        st.write("### Settings")
        st.toggle("Auto-Trading")
        st.toggle("Notifications")
      
