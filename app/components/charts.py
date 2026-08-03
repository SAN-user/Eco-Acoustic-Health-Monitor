"""
EcoSense AI - Plotly Data Visualization Charts
Includes Forest Health Trend, Species Frequency, and Threat Analysis interactive charts.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from app.styles.theme import ThemeTokens

def render_health_trend_chart(df: pd.DataFrame, dark_mode: bool = False):
    """
    Renders an interactive line chart for Weekly Forest Health trend.
    """
    fig = go.Figure()

    # Health Score line
    fig.add_trace(go.Scatter(
        x=df["Day"],
        y=df["Health Score (%)"],
        mode='lines+markers',
        name='Forest Health Score',
        line=dict(color=ThemeTokens.EMERALD_GREEN, width=3.5, shape='spline'),
        marker=dict(size=8, color=ThemeTokens.FOREST_GREEN, symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(46, 125, 50, 0.08)'
    ))

    # Target baseline line
    fig.add_trace(go.Scatter(
        x=df["Day"],
        y=df["Target Baseline"],
        mode='lines',
        name='Healthy Target (90%)',
        line=dict(color='#F59E0B', width=1.5, dash='dash')
    ))

    text_color = ThemeTokens.DARK_TEXT_PRIMARY if dark_mode else ThemeTokens.LIGHT_TEXT_PRIMARY
    paper_bg = "rgba(0,0,0,0)"

    fig.update_layout(
        title=dict(text="<b>Weekly Forest Health Trend</b>", font=dict(size=15, color=text_color)),
        xaxis=dict(title=None, showgrid=False, font=dict(color=text_color)),
        yaxis=dict(title="Health Score (%)", range=[60, 100], showgrid=True, gridcolor='rgba(100,116,139,0.1)'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
        paper_bgcolor=paper_bg,
        plot_bgcolor=paper_bg,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color=text_color)),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

def render_species_frequency_chart(df: pd.DataFrame, dark_mode: bool = False):
    """
    Renders a bar chart showing detection frequencies of top species.
    """
    text_color = ThemeTokens.DARK_TEXT_PRIMARY if dark_mode else ThemeTokens.LIGHT_TEXT_PRIMARY

    fig = px.bar(
        df,
        x="Detections",
        y="Species",
        orientation='h',
        color="Detections",
        color_continuous_scale=[[0, "#A5D6A7"], [1, "#1E4D2B"]],
        title="<b>Top Species Detections</b>"
    )

    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        xaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)', title="Total Detections"),
        yaxis=dict(title=None, categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

def render_threat_trend_chart(df: pd.DataFrame, dark_mode: bool = False):
    """
    Renders a grouped bar chart for threat detections (Chainsaws, Gunshots, Vehicles).
    """
    text_color = ThemeTokens.DARK_TEXT_PRIMARY if dark_mode else ThemeTokens.LIGHT_TEXT_PRIMARY

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Day"],
        y=df["Chainsaws"],
        name="Chainsaws",
        marker_color="#DC2626"
    ))

    fig.add_trace(go.Bar(
        x=df["Day"],
        y=df["Gunshots"],
        name="Gunshots",
        marker_color="#7C3AED"
    ))

    fig.add_trace(go.Bar(
        x=df["Day"],
        y=df["Vehicles"],
        name="Vehicles",
        marker_color="#F59E0B"
    ))

    fig.update_layout(
        barmode='group',
        title=dict(text="<b>Threat Occurrence Trend</b>", font=dict(size=15, color=text_color)),
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)', title="Alert Count"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)
