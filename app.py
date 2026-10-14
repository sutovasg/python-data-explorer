import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Python Data Explorer",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Custom CSS for sleek UI
# ----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #0f172a;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem 2.2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #dbe4f0;
        margin-bottom: 0;
    }

    .section-card {
        background: white;
        border-radius: 18px;
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .mini-card {
        background: white;
        border-radius: 16px;
        padding: 1rem 1rem 0.8rem 1rem;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        border: 1px solid #e5e7eb;
    }

    .insight-box {
        background: #ecfeff;
        border: 1px solid #a5f3fc;
        border-radius: 14px;
        padding: 1rem;
        color: #164e63;
        margin-top: 0.5rem;
    }

    .caption-text {
        color: #64748b;
        font-size: 0.95rem;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
    }

    .stDataFrame, .stPlotlyChart {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sample data
# ----------------------------
sample_data = pd.DataFrame({
    "Month": ["January", "February", "March", "April", "May", "June"],
    "Revenue": [9600, 11400, 10900, 13500, 17200, 21600],
    "Orders": [120, 135, 128, 155, 190, 230],
    "Region": ["North", "North", "South", "South", "West", "West"]
})

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## ⚙️ Data Controls")
    st.markdown(
        "<p class='caption-text'>Upload a CSV file or continue with the sample dataset.</p>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    st.markdown("---")
    st.markdown("### About this tool")
    st.markdown(
        "<p class='caption-text'>A lightweight Python dashboard built with Streamlit, pandas and Plotly to explore data quickly and clearly.</p>",
        unsafe_allow_html=True
    )

# ----------------------------
# Load data
# ----------------------------
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        dataset_label = f"Using uploaded file: {uploaded_file.name}"
        using_sample = False
    except Exception:
        st.error("Unable to read this CSV file. Please upload a valid CSV.")
        st.stop()
else:
    df = sample_data.copy()
    dataset_label = "Using built-in sample dataset"
    using_sample = True

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

# ----------------------------
# Hero section
# ----------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-title">📊 Python Data Explorer</div>
    <p class="hero-subtitle">
        Explore business data, visualise trends, and surface quick insights in a clean, professional dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

colA, colB = st.columns([3, 2])

with colA:
    st.markdown(
        f"<p class='caption-text'><strong>Dataset status:</strong> {dataset_label}</p>",
        unsafe_allow_html=True
    )

with colB:
    if using_sample:
        st.info("Currently showing fictional sample data.")
    else:
        st.success("Upload loaded successfully.")

# ----------------------------
# Metrics
# ----------------------------
numeric_columns = df.select_dtypes(include="number").columns.tolist()
non_numeric_columns = df.select_dtypes(exclude="number").columns.tolist()

row_count = len(df)
column_count = len(df.columns)

metric_1_label = "Rows"
metric_1_value = f"{row_count:,}"

metric_2_label = "Columns"
metric_2_value = f"{column_count:,}"

if numeric_columns:
    primary_metric = numeric_columns[0]
    metric_3_label = f"Total {primary_metric}"
    metric_3_value = f"{df[primary_metric].sum():,.0f}"

    metric_4_label = f"Average {primary_metric}"
    metric_4_value = f"{df[primary_metric].mean():,.2f}"
else:
    metric_3_label = "Numeric Columns"
    metric_3_value = "0"
    metric_4_label = "Status"
    metric_4_value = "No metrics"

m1, m2, m3, m4 = st.columns(4)
m1.metric(metric_1_label, metric_1_value)
m2.metric(metric_2_label, metric_2_value)
m3.metric(metric_3_label, metric_3_value)
m4.metric(metric_4_label, metric_4_value)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------
# Chart controls
# ----------------------------
chart_left, chart_right = st.columns([3, 2])

with chart_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Chart Controls")

    if non_numeric_columns:
        x_axis = st.selectbox("X-axis", options=non_numeric_columns)
    else:
        df = df.reset_index().rename(columns={"index": "Index"})
        x_axis = "Index"

    if numeric_columns:
        y_axis = st.selectbox("Y-axis", options=numeric_columns, index=0)
    else:
        st.warning("No numeric columns available for charting.")
        st.stop()

    chart_type = st.selectbox(
        "Chart type",
        options=["Bar", "Line", "Area"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Main chart
# ----------------------------
with chart_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Performance Overview")

    if chart_type == "Bar":
        fig = px.bar(
            df,
            x=x_axis,
            y=y_axis,
            template="plotly_white",
            color_discrete_sequence=["#14b8a6"]
        )
    elif chart_type == "Line":
        fig = px.line(
            df,
            x=x_axis,
            y=y_axis,
            template="plotly_white",
            markers=True,
            color_discrete_sequence=["#0f172a"]
        )
    else:
        fig = px.area(
            df,
            x=x_axis,
            y=y_axis,
            template="plotly_white",
            color_discrete_sequence=["#38bdf8"]
        )

    fig.update_layout(
        title=f"{y_axis} by {x_axis}",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=20),
        xaxis_title=x_axis,
        yaxis_title=y_axis
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Quick insights
# ----------------------------
insight_col1, insight_col2 = st.columns([2, 2])

with insight_col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Quick Insights")

    highest_value = df[y_axis].max()
    lowest_value = df[y_axis].min()
    average_value = df[y_axis].mean()

    if x_axis in df.columns:
        highest_row = df.loc[df[y_axis].idxmax(), x_axis]
        lowest_row = df.loc[df[y_axis].idxmin(), x_axis]

        st.markdown(f"""
        <div class="insight-box">
            <strong>Top performer:</strong> {highest_row} with {highest_value:,.2f}<br><br>
            <strong>Lowest value:</strong> {lowest_row} with {lowest_value:,.2f}<br><br>
            <strong>Average {y_axis.lower()}:</strong> {average_value:,.2f}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="insight-box">
            <strong>Highest {y_axis}:</strong> {highest_value:,.2f}<br><br>
            <strong>Lowest {y_axis}:</strong> {lowest_value:,.2f}<br><br>
            <strong>Average {y_axis}:</strong> {average_value:,.2f}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with insight_col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Dataset Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Optional numeric distribution
# ----------------------------
if numeric_columns:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Distribution View")

    distribution_metric = st.selectbox(
        "Choose a metric to inspect distribution",
        options=numeric_columns,
        key="distribution_metric"
    )

    hist_fig = px.histogram(
        df,
        x=distribution_metric,
        nbins=10,
        template="plotly_white",
        color_discrete_sequence=["#334155"]
    )

    hist_fig.update_layout(
        title=f"Distribution of {distribution_metric}",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=20)
    )

    st.plotly_chart(hist_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)