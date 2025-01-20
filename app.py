import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes_model import BlackScholes

BACKGROUND_COLOR = "#0E1117"

st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.metric-call {
    background-color: #00D100;
    color: black;
}

.metric-put {
    background-color: #FF2E2E;
    color: black;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: bold;
    text-align: center;
}

.metric-label {
    font-size: 1.2rem;
    margin-bottom: 5px;
    text-align: center;
}

.greek-container {
    background-color: #2E2E2E;
    padding: 10px;
    border-radius: 5px;
    margin: 5px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.title("📊 Black-Scholes Calculator")
    st.write("Created by Nicolas Pons")
    
    tab1, tab2 = st.tabs(["Parameters", "Analysis Settings"])
    
    with tab1:
        current_price = st.number_input("Current Asset Price ($)", 
                                      value=100.0, 
                                      min_value=0.01)
        strike = st.number_input("Strike Price ($)", 
                               value=100.0, 
                               min_value=0.01)
        time_to_maturity = st.number_input("Time to Maturity (Years)", 
                                         value=1.0, 
                                         min_value=0.01)
        volatility = st.slider("Volatility (σ)", 
                             min_value=0.01, 
                             max_value=1.0, 
                             value=0.2)
        interest_rate = st.slider("Risk-Free Rate", 
                                min_value=0.0, 
                                max_value=0.20, 
                                value=0.05)
    
    with tab2:
        spot_min = st.number_input('Min Spot Price', 
                                 min_value=0.01, 
                                 value=current_price*0.8)
        spot_max = st.number_input('Max Spot Price', 
                                 min_value=0.01, 
                                 value=current_price*1.2)
        vol_min = st.slider('Min Volatility', 
                          min_value=0.01, 
                          max_value=1.0, 
                          value=volatility*0.5)
        vol_max = st.slider('Max Volatility', 
                          min_value=0.01, 
                          max_value=1.0, 
                          value=volatility*1.5)
        
        spot_points = st.slider('Number of Spot Price Points', 
                              min_value=5, 
                              max_value=20, 
                              value=10)
        vol_points = st.slider('Number of Volatility Points', 
                             min_value=5, 
                             max_value=20, 
                             value=10)

spot_range = np.linspace(spot_min, spot_max, spot_points)
vol_range = np.linspace(vol_min, vol_max, vol_points)

# Main Page
st.title("Black-Scholes Option Calculator")

# Initialize model and calculate prices
bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()

# Display option prices
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Option Price</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Option Price</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Greeks Display
st.subheader("Option Greeks")
call_greeks, put_greeks = bs_model.calculate_greeks()

col1, col2, col3, col4, col5 = st.columns(5)
greek_names = ["Delta", "Gamma", "Theta", "Vega", "Rho"]
greek_values = [
    call_greeks.delta,
    call_greeks.gamma,
    call_greeks.theta,
    call_greeks.vega,
    call_greeks.rho
]

for col, name, value in zip([col1, col2, col3, col4, col5], greek_names, greek_values):
    with col:
        st.markdown(f"""
            <div class="greek-container">
                <div style="font-size: 1.2rem;">{name}</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{value:.4f}</div>
            </div>
        """, unsafe_allow_html=True)

# Price Sensitivity Analysis
st.subheader("Price Sensitivity Analysis")

def create_heatmap(prices, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(prices, 
                xticklabels=np.round(spot_range, 2),
                yticklabels=np.round(vol_range, 2),
                annot=True, 
                fmt=".2f",
                cmap="RdYlGn",
                ax=ax)
    fig.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)
    # Customize text color for better readability
    ax.tick_params(colors='white')  # White ticks
    ax.xaxis.label.set_color('white')  # X-axis label
    ax.yaxis.label.set_color('white')  # Y-axis label
    ax.title.set_color('white')  # Title color
    ax.set_title(title)
    ax.set_xlabel('Spot Price')
    ax.set_ylabel('Volatility')
    return fig

# Calculate prices for heatmap
call_prices = np.zeros((len(vol_range), len(spot_range)))
put_prices = np.zeros((len(vol_range), len(spot_range)))

for i, vol in enumerate(vol_range):
    for j, spot in enumerate(spot_range):
        bs_temp = BlackScholes(time_to_maturity, strike, spot, vol, interest_rate)
        c, p = bs_temp.calculate_prices()
        call_prices[i, j] = c
        put_prices[i, j] = p

col1, col2 = st.columns(2)
with col1:
    st.pyplot(create_heatmap(call_prices, 'Call Option Prices'))
with col2:
    st.pyplot(create_heatmap(put_prices, 'Put Option Prices'))

# PnL Analysis
st.subheader("Profit/Loss Analysis")
purchase_price = st.number_input("Option Purchase Price ($)", 
                               value=min(call_price, put_price),
                               min_value=0.0)

call_pnl, put_pnl = bs_model.calculate_pnl(spot_range, purchase_price)

fig = go.Figure()
fig.add_trace(go.Scatter(x=spot_range, y=call_pnl, name="Call PnL",
                        line=dict(color="#00D100")))
fig.add_trace(go.Scatter(x=spot_range, y=put_pnl, name="Put PnL",
                        line=dict(color="#FF2E2E")))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.update_layout(title="Option PnL Analysis",
                 xaxis_title="Spot Price ($)",
                 yaxis_title="PnL ($)",
                 height=500)

st.plotly_chart(fig, use_container_width=True)

# Download results
if st.button("Download Analysis Results"):
    results = pd.DataFrame({
        'Spot Price': spot_range,
        'Call PnL': call_pnl,
        'Put PnL': put_pnl,
        'Call Price': call_prices[-1],  # Using last volatility row
        'Put Price': put_prices[-1]
    })
    
    st.download_button(
        "Download CSV",
        results.to_csv(index=False),
        "black_scholes_analysis.csv",
        "text/csv"
    )
