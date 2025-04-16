import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the feature names and their corresponding abbreviations
feature_names = {
    'CM': 'How comfortable are you using AI tools for learning or teaching?',
    'TS': 'Do AI tools save time in completing assignments or preparing lessons?',
    'EN': 'Have AI tools increased your engagement with the learning material?',
    'VC': 'Are you challenged to verify the accuracy of AI-generated data?',
    'IC': 'Do you think AI tools reduce critical thinking or creativity?',
    'OR': 'Do you feel over-reliant on AI tools for educational tasks?',
    'PC': 'Privacy concerns:',
    'NI': 'Have you experienced any negative impacts from AI on your learning or teaching process?',
    'EF': 'How effective are AI tools with your personal learning needs?',
    'IN': 'Have AI tools increased your interest in learning new topics?',
}

# Create the Streamlit app
st.title('AI in Education Prediction App')

# Displaying instructions and feature explanation
st.markdown("""
    This app predicts whether AI tools have a **positive** or **negative** impact on your educational experience based on the following criteria.
    Please answer the questions below using the sliders where:
    - **0** = Strongly Disagree
    - **4** = Strongly Agree
""")

# Create a dictionary to hold user inputs
input_data = []

# Get user input for features
for feature_abbr, feature_question in feature_names.items():
    st.write(f"### {feature_question}")
    value = st.slider(
        feature_question,
        0, 4, 2,
        help="Rate from 0 (Strongly Disagree) to 4 (Strongly Agree)"
    )
    input_data.append(value)

# Create a DataFrame for input data
input_df = pd.DataFrame([input_data], columns=feature_names.keys())

# Display a loading spinner during prediction
if st.button('Predict'):
    with st.spinner('Making your prediction...'):
        if len(input_data) == len(feature_names):  # Ensure all inputs are filled
            prediction = model.predict(input_df)[0]
            st.write("### Your responses:")
            for feature_abbr, feature_question in feature_names.items():
                st.write(f"{feature_question}: {input_df[feature_abbr][0]}")
            
            # Display prediction result with color coding
            if prediction == 1:
                st.markdown('<h3 style="color:red;">Prediction: <b>Negative</b></h3>', unsafe_allow_html=True)
                st.write("### Recommendation:")
                st.write("Consider exploring more AI tools or balancing them with other traditional learning methods.")
            else:
                st.markdown('<h3 style="color:green;">Prediction: <b>Positive</b></h3>', unsafe_allow_html=True)
                st.write("### Recommendation:")
                st.write("You seem to benefit greatly from AI tools. Keep exploring new AI tools to enhance your learning.")
        else:
            st.warning("Please fill out all questions before predicting.")

# Add custom CSS for styling
st.markdown("""
    <style>
    .stSlider>div>div>div>input {
        width: 90%;
    }
    h3 {
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)
