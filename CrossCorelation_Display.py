import csv 
import plotly.graph_objs as go
import numpy as np
import streamlit as st
import pandas as pd


st.title("🐾Cross Correlation Program Heel and Toe🦿")
st.sidebar.title("👣Given the Value of slider constant➡️")
k_slider = st.sidebar.slider("k_value", min_value=0, max_value=6000, step=50)
st.sidebar.write("K value is a variabel that can shiift the heel signal to n value")
heel = []
toe = []
#Reading dataset 
file_path_heel = "Heel123.txt"
with open(file_path_heel) as file:
    lines = csv.reader(file)
    for row in lines:
        heel.append(float(row[0]))

file_path_toe = "Toe123.txt"
with open(file_path_toe) as file:
    lines = csv.reader(file)
    for row in lines:
        toe.append(float(row[0]))

st.write("Lenght Data of the Original Heel Signal:", len(heel))
st.write("Lenght Data of the Original Toe Signal:", len(toe))
i = np.arange(0, len(toe), 1)
plotly_fig_toe_heel = go.Figure()

plotly_fig_toe_heel.add_trace(go.Scatter(x=i, y=toe, mode='lines', name='Toe Signal', line=dict(color='green')))
plotly_fig_toe_heel.add_trace(go.Scatter(x=i, y=heel, mode='lines', name='Heel Signal', line=dict(color='red')))
# Customize the layout
plotly_fig_toe_heel.update_layout(
    xaxis_title="Sequence [n]",
    yaxis_title="Voltage [mV]",
    title="Toe and Heel Signals",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)
st.subheader("Plot Original Dataset")
st.plotly_chart(plotly_fig_toe_heel)

if st.sidebar.button("Run"):
    new_heel = []
    for i in range (len(heel)):
        new_heel.append(heel[i])

    for i in range(len(heel)):
        if i < k_slider:
            heel[i] = 0
        else:
            heel[i] = new_heel[i-k_slider]
    for i in range(k_slider):
        heel.append(new_heel[len(new_heel)-k_slider+i])
        toe.append(0)
        

    plotly_with_slider = go.Figure()
    plotly_with_slider.add_trace(go.Scatter(x=list(range(len(heel))), y=toe, mode='lines', name='Toe Signal', line=dict(color='green')))
    # Add the shifted heel signal to the plot
    plotly_with_slider.add_trace(go.Scatter(x=list(range(len(heel))), y=heel, mode='lines', name='Heel Signal', line=dict(color='red')))

    # Customize the layout
    plotly_with_slider.update_layout(
        xaxis_title="Sequence [n]",
        yaxis_title="Rxy Value",
        title="Toe and Heel Signals with Heel Shifted",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    st.subheader(f"Plot Shifted Signal with {k_slider} value")
    st.plotly_chart(plotly_with_slider)

    Rxy= []

    for L in range(len(toe)):
        sigmaL = 0.0
        for n in range(len(toe)):
            if n - L >= 0:
                sigmaL += heel[n] * toe[n - L]
        Rxy.append(sigmaL)


    i = np.arange(0, len(toe), 1)
    plotly_fig_auto_correlation = go.Figure()
    # Add the heel signal to the plot
    plotly_fig_auto_correlation.add_trace(go.Scatter(x=i, y=Rxy, mode='lines', name='Heel Signal', line=dict(color='red')))

    # Customize the layout
    plotly_fig_auto_correlation.update_layout(
        xaxis_title="Sequence [n]",
        yaxis_title="Rxy Value",
        title="Toe and Heel Signals",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    # Show the plot
    st.subheader("Plot Auto Correlation Heel and Toe Signal after Shifted")
    st.plotly_chart(plotly_fig_auto_correlation)

    norm = []

    for i in range(len(Rxy)):
        norm.append(Rxy[i] / (len(Rxy)- i))

    i = np.arange(0, len(norm), 1)
    plotly_fig_norm = go.Figure()
    # Add the heel signal to the plot
    plotly_fig_norm.add_trace(go.Scatter(x=i, y=norm, mode='lines', name='Heel Signal', line=dict(color='red')))

    # Customize the layout
    plotly_fig_norm.update_layout(
        xaxis_title="Sequence [n]",
        yaxis_title="Voltage [mV]",
        title="Toe and Heel Signals after Normalized",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    # Show the plot
    st.subheader("Normalized Auto Correction")
    st.plotly_chart(plotly_fig_norm, use_container_width=True)

    # Create a Pandas DataFrame
    st.subheader("Value each Data")

    colom1, colom2, colom3 = st.columns(3)
    df1 = pd.DataFrame(heel, columns=["Heel Value"])
    df2 = pd.DataFrame(toe, columns=["Toe Value"])
    df = pd.DataFrame(norm, columns=["Normalized Value"])

    with colom1:
        st.write("DataFrame of Heel Values")
        st.write(df1)

    with colom2:
        st.write("DataFrame of Toe Values")
        st.write(df2)

    with colom3:
        st.write("DataFrame of Normalized Values")
        st.write(df)




