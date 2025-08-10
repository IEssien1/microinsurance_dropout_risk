
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="Insurance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/IEssien1/microinsurance_dropout_risk/refs/heads/main/Insurance_dataset.csv")
    df['Policy_Start_Date'] = pd.to_datetime(df['Policy_Start_Date'], errors='coerce')
    df['Policy_End_Date'] = pd.to_datetime(df['Policy_End_Date'], errors='coerce')
    df['Last_Claim_Date'] = pd.to_datetime(df['Last_Claim_Date'], errors='coerce')
    return df

df = load_data()

# Custom styles
st.markdown("""
    <style>
    .big-font {font-size:18px !important;}
    .title-font {font-size:26px !important; font-weight: 700;}
    .metric-font {font-size:22px !important;}
    </style>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Filters")
region_filter = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())
gender_filter = st.sidebar.multiselect("Select Gender(s):", options=df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[df['Region'].isin(region_filter) & df['Gender'].isin(gender_filter)]

# === Title ===
st.markdown("<h1 style='text-align: center;'> Insurance Data Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# === KPI Metrics ===
st.markdown("## Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    dropout_rate = filtered_df['Dropout_Flag'].mean()
    st.metric("Dropout Rate", f"{dropout_rate:.2%}")

with col2:
    renewal_rate = filtered_df['Renewed'].mean()
    st.metric("Renewal Rate", f"{renewal_rate:.2%}")

with col3:
    avg_income = filtered_df['Monthly_Income'].mean()
    st.metric("Avg. Income", f"₦{avg_income:,.0f}")

with col4:
    avg_wallet = filtered_df['Wallet_Balance'].mean()
    st.metric("Avg. Wallet Balance", f"₦{avg_wallet:,.0f}")

with col5:
    total_claims = filtered_df['Total_Claims'].sum()
    denied_rate = (filtered_df['Denied_Claims'].sum() / total_claims) if total_claims > 0 else 0
    st.metric("Denied Claims Rate", f"{denied_rate:.2%}")

st.markdown("---")

# Charts
st.markdown("## Visual Analytics")

# Chart 1: Age distribution
with st.container():
    st.markdown("### Age Distribution")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['Age'], bins=20, kde=True, color="#4B8BBE", ax=ax1)
    st.pyplot(fig1)

# Chart 2: Monthly Income
with st.container():
    st.markdown("### Monthly Income Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['Monthly_Income'], bins=30, kde=True, color="#306998", ax=ax2)
    st.pyplot(fig2)

# Row: Categorical countplots
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Gender Distribution")
    fig3, ax3 = plt.subplots()
    sns.countplot(data=filtered_df, x='Gender', palette='pastel', ax=ax3)
    st.pyplot(fig3)

with col2:
    st.markdown("### Dropout vs Renewed")
    fig4, ax4 = plt.subplots()
    sns.countplot(data=filtered_df, x='Dropout_Flag', palette='Set2', ax=ax4)
    st.pyplot(fig4)

# Row: Region-based analysis
st.markdown("### Region-wise Analysis")
col1, col2 = st.columns(2)

with col1:
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=filtered_df, x='Region', order=filtered_df['Region'].value_counts().index, ax=ax5)
    ax5.tick_params(axis='x', rotation=45)
    ax5.set_title("Policyholders by Region")
    st.pyplot(fig5)

with col2:
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_df, x='Region', y='Monthly_Income', estimator='mean', ax=ax6)
    ax6.tick_params(axis='x', rotation=45)
    ax6.set_title("Avg. Monthly Income by Region")
    st.pyplot(fig6)

# Correlation Heatmap
# st.markdown("### Correlation Heatmap")
# fig7, ax7 = plt.subplots(figsize=(12, 7))
# sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax7)
# st.pyplot(fig7)

st.markdown("---")
st.markdown("### Raw Data Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)
