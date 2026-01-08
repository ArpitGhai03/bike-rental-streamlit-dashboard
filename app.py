import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Bike Rental Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            padding: 0rem 0rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['date'] = df['datetime'].dt.date
    
    df['season'] = df['season'].map({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })
    
    df['weather_type'] = df['weather'].map({
        1: 'Clear',
        2: 'Mist',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    })
    
    return df

df = load_data()

# Title and description
st.markdown("# 🚴 Washington D.C. Bike Rental Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📊 Filters")

year_filter = st.sidebar.multiselect(
    "Select Year(s):",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

season_filter = st.sidebar.multiselect(
    "Select Season(s):",
    options=sorted(df['season'].unique()),
    default=sorted(df['season'].unique())
)

# Apply filters
filtered_df = df[(df['year'].isin(year_filter)) & (df['season'].isin(season_filter))]

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📈 Total Rentals",
        value=f"{filtered_df['count'].sum():,}",
        delta=None
    )

with col2:
    st.metric(
        label="👥 Registered Users",
        value=f"{filtered_df['registered'].sum():,}",
        delta=None
    )

with col3:
    st.metric(
        label="🚶 Casual Users",
        value=f"{filtered_df['casual'].sum():,}",
        delta=None
    )

with col4:
    st.metric(
        label="📅 Data Points",
        value=f"{len(filtered_df):,}",
        delta=None
    )

st.markdown("---")

# ============================================
# VISUALIZATION 1: Hourly Rentals Pattern
# ============================================
st.subheader("📊 Mean Hourly Rentals vs Hour of Day")
st.markdown("**Peak commute hours at 8 AM and 5-6 PM reveal strong work-related demand**")

hourly_mean = filtered_df.groupby('hour')['count'].mean()
fig_hourly = go.Figure()
fig_hourly.add_trace(go.Scatter(
    x=hourly_mean.index,
    y=hourly_mean.values,
    mode='lines+markers',
    name='Mean Rentals',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=8),
    fill='tozeroy',
    fillcolor='rgba(31, 119, 180, 0.2)'
))

# Highlight top hours
top_hours = hourly_mean.nlargest(3)
for h, val in top_hours.items():
    fig_hourly.add_annotation(
        x=h, y=val,
        text=f"{int(h)}h<br>{val:.0f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor='#FF6B6B',
        ax=0,
        ay=-40,
        bgcolor='rgba(255, 107, 107, 0.7)',
        bordercolor='#FF6B6B',
        font=dict(color='white', size=10)
    )

fig_hourly.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Mean Rentals",
    height=450,
    template='plotly_white',
    hovermode='x unified'
)
st.plotly_chart(fig_hourly, use_container_width=True)

st.markdown("---")

# ============================================
# VISUALIZATION 2: Hourly Rentals by Day of Week (Line Plot)
# ============================================
st.subheader("📅 Mean Hourly Rentals by Hour - Each Day of Week")
st.markdown("**Weekday vs Weekend patterns: Weekdays show commute peaks; Weekends show flat leisure demand**")

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hour_day = filtered_df.groupby(['day_of_week', 'hour'])['count'].mean().reset_index()

# Color weekdays vs weekends differently
color_map = {
    'Monday': '#1f77b4', 'Tuesday': '#1f77b4', 'Wednesday': '#1f77b4',
    'Thursday': '#1f77b4', 'Friday': '#1f77b4',
    'Saturday': '#ff7f0e', 'Sunday': '#ff7f0e'
}

fig_hourly_dow = go.Figure()
for day in day_order:
    subset = hour_day[hour_day['day_of_week'] == day]
    if not subset.empty:
        fig_hourly_dow.add_trace(go.Scatter(
            x=subset['hour'],
            y=subset['count'],
            mode='lines',
            name=day,
            line=dict(width=2.5, color=color_map[day]),
            opacity=0.8,
            hovertemplate='<b>%{fullData.name}</b>, Hour %{x}<br>Mean Rentals: %{y:.0f}<extra></extra>'
        ))

fig_hourly_dow.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Mean Rentals",
    height=450,
    template='plotly_white',
    hovermode='x unified',
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    xaxis=dict(tickmode='linear', tick0=0, dtick=2)
)
st.plotly_chart(fig_hourly_dow, use_container_width=True)

st.markdown("---")

# ============================================
# VISUALIZATION 3: Monthly Trends by Year
# ============================================
st.subheader("📈 Monthly Trends - 2011 vs 2012 Performance")
st.markdown("**2012 shows 2x growth compared to 2011 with preserved seasonal patterns**")

col1, col2 = st.columns(2)

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for year_val, col in zip([2011, 2012], [col1, col2]):
    year_data = filtered_df[filtered_df['year'] == year_val]
    monthly_mean = year_data.groupby('month')['count'].mean()
    
    color = '#FF6B6B' if year_val == 2011 else '#4ECDC4'
    dark_color = 'darkred' if year_val == 2011 else 'darkblue'
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[month_names[int(m)-1] for m in monthly_mean.index],
        y=monthly_mean.values,
        marker=dict(color=color, line=dict(color='black', width=1)),
        opacity=0.7,
        name='Mean Rentals'
    ))
    fig.add_trace(go.Scatter(
        x=[month_names[int(m)-1] for m in monthly_mean.index],
        y=monthly_mean.values,
        mode='lines+markers',
        line=dict(color=dark_color, width=3),
        marker=dict(size=8),
        name='Trend'
    ))
    
    fig.update_layout(
        title=f"Mean Hourly Rentals by Month - {year_val}",
        xaxis_title="Month",
        yaxis_title="Mean Rentals",
        height=400,
        template='plotly_white',
        showlegend=True
    )
    
    with col:
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# VISUALIZATION 4: Weather Impact with CI
# ============================================
st.subheader("🌧️ Weather Impact on Rentals - Mean with 95% Confidence Intervals")
st.markdown("**Clear weather drives 72% more rentals than rainy conditions**")

weather_stats = []
weather_labels_map = {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Rain', 4: 'Moderate Rain'}

for weather_val in sorted(filtered_df['weather'].unique()):
    weather_subset = filtered_df[filtered_df['weather'] == weather_val]['count']
    mean_val = weather_subset.mean()
    std_val = weather_subset.std()
    n = len(weather_subset)
    ci = 1.96 * std_val / np.sqrt(n)
    weather_stats.append({
        'weather': weather_labels_map.get(weather_val, f'Weather {weather_val}'),
        'mean': mean_val,
        'ci_lower': mean_val - ci,
        'ci_upper': mean_val + ci
    })

weather_df = pd.DataFrame(weather_stats).sort_values('mean', ascending=False)
colors_weather = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

fig_weather = go.Figure()
fig_weather.add_trace(go.Bar(
    x=weather_df['weather'],
    y=weather_df['mean'],
    error_y=dict(
        type='data',
        symmetric=False,
        array=weather_df['ci_upper'] - weather_df['mean'],
        arrayminus=weather_df['mean'] - weather_df['ci_lower'],
        color='black',
        thickness=2,
        width=6
    ),
    marker=dict(color=colors_weather, line=dict(color='black', width=1.5)),
    text=[f"{val:.0f}" for val in weather_df['mean']],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Mean: %{y:.0f}<br>95% CI: [%{customdata[0]:.0f}, %{customdata[1]:.0f}]<extra></extra>',
    customdata=np.column_stack((weather_df['ci_lower'], weather_df['ci_upper']))
))

fig_weather.update_layout(
    xaxis_title="Weather Category",
    yaxis_title="Mean Rentals",
    height=450,
    template='plotly_white',
    showlegend=False
)
st.plotly_chart(fig_weather, use_container_width=True)

st.markdown("---")

# ============================================
# VISUALIZATION 5: Working vs Non-Working Days by Period
# ============================================
st.subheader("💼 Demand Pattern: Working vs Non-Working Days by Period")
st.markdown("**Evening peak amplified on working days; weekends show flat midday leisure demand**")

bins = [-0.01, 6, 12, 18, 24]
labels = ['Night (12 AM-6 AM)', 'Morning (6 AM-12 PM)', 'Afternoon (12 PM-6 PM)', 'Evening (6 PM-12 AM)']
filtered_df['day_period'] = pd.cut(filtered_df['hour'], bins=bins, labels=labels, right=False)

period_stats = filtered_df.groupby(['day_period', 'workingday'])['count'].agg(['mean', 'std', 'count']).reset_index()
period_stats['sem'] = period_stats['std'] / np.sqrt(period_stats['count'])
period_stats['ci95'] = 1.96 * period_stats['sem']

fig_period = go.Figure()

for wd, label, color in [(1, 'Working Days', '#1f77b4'), (0, 'Non-Working Days', '#ff7f0e')]:
    data = period_stats[period_stats['workingday'] == wd]
    fig_period.add_trace(go.Bar(
        x=data['day_period'].astype(str),
        y=data['mean'],
        error_y=dict(
            type='data',
            array=data['ci95'],
            color='black',
            thickness=2,
            width=6
        ),
        name=label,
        marker=dict(color=color, line=dict(color='black', width=1)),
        text=[f"{val:.0f}" for val in data['mean']],
        textposition='outside'
    ))

fig_period.update_layout(
    xaxis_title="Time Period",
    yaxis_title="Mean Rentals",
    height=450,
    template='plotly_white',
    barmode='group',
    hovermode='x unified'
)
st.plotly_chart(fig_period, use_container_width=True)

st.markdown("---")

# ============================================
# VISUALIZATION 6: Seasonal Monthly Patterns
# ============================================
st.subheader("🌡️ Seasonal Trends - Monthly Performance Across Seasons")
st.markdown("**Summer peaks at 242 rentals; Spring ramps up gradually; Winter shows steepest decline**")

season_order = ['Spring', 'Summer', 'Fall', 'Winter']
colors_seasons = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

fig_seasons = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Spring (Jan-Mar)', 'Summer (Apr-Jun)', 'Fall (Jul-Sep)', 'Winter (Oct-Dec)'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

month_names_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
season_months = {
    'Spring': [1, 2, 3],
    'Summer': [4, 5, 6],
    'Fall': [7, 8, 9],
    'Winter': [10, 11, 12]
}

row_col = [(1, 1), (1, 2), (2, 1), (2, 2)]

for season, (r, c), color in zip(season_order, row_col, colors_seasons):
    months = season_months[season]
    season_data = filtered_df[filtered_df['month'].isin(months)]
    monthly_mean = season_data.groupby('month')['count'].mean()
    
    month_labels = [month_names_short[int(m)-1] for m in monthly_mean.index]
    
    fig_seasons.add_trace(
        go.Bar(x=month_labels, y=monthly_mean.values, marker=dict(color=color, line=dict(color='black', width=1)),
               name=season, showlegend=False),
        row=r, col=c
    )
    fig_seasons.add_trace(
        go.Scatter(x=month_labels, y=monthly_mean.values, mode='lines+markers',
                   line=dict(color='darkred' if season != 'Winter' else 'darkblue', width=2.5),
                   marker=dict(size=8), showlegend=False),
        row=r, col=c
    )
    
    fig_seasons.update_xaxes(title_text="Month", row=r, col=c)
    fig_seasons.update_yaxes(title_text="Mean Rentals", row=r, col=c)

fig_seasons.update_layout(height=600, title_text="Monthly Mean Hourly Rentals by Season", template='plotly_white')
st.plotly_chart(fig_seasons, use_container_width=True)

st.markdown("---")

# ============================================
# FINAL VISUALIZATION: Correlation Heatmap (Numerical Variables Only)
# ============================================
st.subheader("📊 Correlation Analysis - Numerical Variables")
st.markdown("**Correlation matrix shows relationships between all numerical variables in the dataset**")

# Select only numerical columns (same as EDA: df.select_dtypes(include='number'))
num_data = filtered_df.select_dtypes(include='number')
correlation_matrix = num_data.corr()

fig_corr_heatmap = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    zmin=-1,
    zmax=1,
    colorbar=dict(title='Correlation'),
    text=np.round(correlation_matrix.values, 2),
    texttemplate='%{text}',
    textfont={"size": 10},
    hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
))

fig_corr_heatmap.update_layout(
    height=550,
    template='plotly_white',
    xaxis={'side': 'bottom'}
)
st.plotly_chart(fig_corr_heatmap, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>🚴 Washington D.C. Bike Rental Analysis Dashboard | Data: 2011-2012</p>
    </div>
""", unsafe_allow_html=True)
