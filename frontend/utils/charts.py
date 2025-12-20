import streamlit as st
import matplotlib.pyplot as plt

def show_probability_chart(prediction: str):
    """
    Simple visualization: show a bar with Low vs High likelihood (dummy percentages).
    """
    labels = ["Low Risk", "High Risk"]
    if prediction == "High Risk":
        vals = [25, 75]
    else:
        vals = [80, 20]

    fig, ax = plt.subplots()
    ax.bar(labels, vals)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Risk Confidence (approx.)")
    st.pyplot(fig)
