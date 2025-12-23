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

def show_readmission_risk_chart(risk: str, probability: float):
    """
    Visualization for readmission risk with probability gauge.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Risk level bar chart
    colors = ['green' if risk == 'Low' else 'red', 'red' if risk == 'High' else 'green']
    ax1.bar(['Low Risk', 'High Risk'], [100-probability*100, probability*100], color=colors)
    ax1.set_ylabel('Probability (%)')
    ax1.set_title('Readmission Risk Level')
    ax1.set_ylim(0, 100)
    
    # Probability gauge
    ax2.pie([probability, 1-probability], labels=[f'Risk: {probability:.1%}', f'Safe: {1-probability:.1%}'], 
            colors=['red', 'green'], startangle=90)
    ax2.set_title('Risk Probability')
    
    st.pyplot(fig)