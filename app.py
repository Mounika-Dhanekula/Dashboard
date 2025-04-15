import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
csv_path = "water_dataX.csv"  # Ensure this is the correct CSV file name
df = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Page config and theme
st.set_page_config(page_title="Creative Water Quality Dashboard", layout="wide", page_icon="🌊")
st.markdown(
    """
    <style>
    div.block-container {
        padding: 2rem;
        background: linear-gradient(120deg, #ffefba, #ffffff);
        color: #000;
        border-radius: 10px;
        font-family: 'Helvetica', sans-serif;
    }
    .title-test {
        font-weight: bold;
        color: #0047ab;
        font-size: 2.5rem;
        text-shadow: 1px 1px #a8dadc;
        text-align: center;
    }
    .footer {
        color: #555;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 2rem;
        animation: glow 2s infinite;
    }
    @keyframes glow {
        0% { text-shadow: 0 0 5px #0047ab; }
        50% { text-shadow: 0 0 20px #1d3557; }
        100% { text-shadow: 0 0 5px #0047ab; }
    }
    </style>
    """, unsafe_allow_html=True
)

# Header
image = Image.open("water.jpg")  # Replace with correct image path if needed
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)
with col2:
    st.markdown('<h1 class="title-test"> Water Symphony Dashboard </h1>', unsafe_allow_html=True)

# Interactive storytelling section
st.markdown("###  **Dive into the Data** ")
st.markdown(f"📅 **Last refreshed on:** {datetime.datetime.now().strftime('%d %B %Y')}")
st.markdown("Here's a story of water: every drop has a tale. Let's follow its journey through the data streams of quality and change. ")

# Ensure numeric conversion
for col in ['D.O. (mg/l)', 'PH', 'B.O.D. (mg/l)', 'Temp']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Visualizations and download buttons
st.markdown("### 📊 **Key Metrics Dashboard**")
col3, col4 = st.columns(2)

with col3:
    fig_do = px.bar(df, x="year", y="D.O. (mg/l)", 
                    title="<b> Dissolved Oxygen's Dance Through Time</b>",
                    labels={"D.O. (mg/l)": "Dissolved Oxygen (mg/l)", "year": "Year"},
                    template="plotly_dark", color_discrete_sequence=["#ffcccb"])
    fig_do.update_traces(marker=dict(opacity=0.8))
    st.plotly_chart(fig_do, use_container_width=True)
    expander_do = st.expander("📋 Year-wise Dissolved Oxygen")
    data_do = df[["year", "D.O. (mg/l)"]].groupby("year")["D.O. (mg/l)"].sum()
    expander_do.write(data_do)
    st.download_button("💾 Download D.O. Data", data_do.to_csv().encode('utf-8'), file_name="yearDO.csv", mime="text/csv")

with col4:
    ph_avg = df.groupby("year")["PH"].mean().reset_index()
    fig_ph = px.line(ph_avg, x="year", y="PH",
                     title="<b>🌡️ The Rhythm of pH Levels Over the Years</b>",
                     markers=True, template="plotly_dark", color_discrete_sequence=["#90e0ef"])
    fig_ph.update_traces(line=dict(dash="dashdot"))
    st.plotly_chart(fig_ph, use_container_width=True)
    expander_ph = st.expander("📋 Year-wise pH")
    data_ph = df[["year", "PH"]].groupby("year")["PH"].sum()
    expander_ph.write(data_ph)
    st.download_button("💾 Download pH Data", data_ph.to_csv().encode('utf-8'), file_name="yearPH.csv", mime="text/csv")

# Divider
st.markdown("---")

# Additional metrics with download buttons
st.markdown("### 🌊 **Water Metrics in Focus**")
col5, col6 = st.columns(2)

with col5:
    bod_avg = df.groupby("year")["B.O.D. (mg/l)"].mean().reset_index()
    fig_bod = px.area(bod_avg, x="year", y="B.O.D. (mg/l)",
                      title="<b>Biochemical Oxygen Demand: A Flowing Saga</b>",
                      template="plotly_dark", color_discrete_sequence=["#ffd700"])
    fig_bod.update_traces(fill="tonexty", opacity=0.7)
    st.plotly_chart(fig_bod, use_container_width=True)
    expander_bod = st.expander("📋 Year-wise B.O.D.")
    data_bod = df[["year", "B.O.D. (mg/l)"]].groupby("year")["B.O.D. (mg/l)"].mean()
    expander_bod.write(data_bod)
    st.download_button("💾 Download B.O.D. Data", data=data_bod.to_csv().encode("utf-8"),
                       file_name="yearBOD.csv", mime="text/csv")

with col6:
    temp_avg = df.groupby("year")["Temp"].mean().reset_index()
    fig_temp = px.scatter(temp_avg, x="year", y="Temp",
                          title="<b> Temperature's Crescendo Over Time</b>",
                          template="plotly_dark", color_discrete_sequence=["#ff4d6d"])
    fig_temp.update_traces(marker=dict(size=12))
    st.plotly_chart(fig_temp, use_container_width=True)
    expander_temp = st.expander("📋 Year-wise Temperature")
    data_temp = df[["year", "Temp"]].groupby("year")["Temp"].mean()
    expander_temp.write(data_temp)
    st.download_button("💾 Download Temperature Data", data=data_temp.to_csv().encode("utf-8"),
                       file_name="yearTemp.csv", mime="text/csv")

# Dynamic pie chart
st.markdown("###  **Pie Chart Insights**")
metric = st.selectbox("Choose a metric for distribution analysis:", ['D.O. (mg/l)', 'PH', 'B.O.D. (mg/l)', 'Temp'])
pie_data = df.groupby("year")[metric].sum().reset_index()
fig_pie = px.pie(pie_data, values=metric, names="year", title=f"<b>📊 Distribution of {metric} by Year</b>",
                 color_discrete_sequence=px.colors.sequential.RdBu)
fig_pie.update_traces(textinfo="percent+label", pull=[0.1, 0.05, 0.05, 0])
st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p><b>Designed with creativity  by mounika</b></p>
        <p><i>Turning water data into art since 2025</i></p>
    </div>
    """, unsafe_allow_html=True
)
