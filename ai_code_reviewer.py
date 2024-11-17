import streamlit as st
import google.generativeai as ai
import time

# Display the title
st.markdown("<h1 style='text-align: center;color: red;'>AI CODE REVIEWER</h1>", unsafe_allow_html=True)
st.image("c.png")
time.sleep(0.2)
st.markdown("<h3 style='color: red;'>Welcome to the AI-Powered Python Code Reviewer!</h3>", unsafe_allow_html=True)
st.write("Paste your Python code snippet below to identify errors, optimize your code, and receive an improved version with suggested fixes.")

# Configure the AI API key
key = "AIzaSyBRakykP1CZ3O7nr-GE-K8_oMOXSzr9Mnw"
ai.configure(api_key=key)

# System prompt for the model
sys_prompt = (
    """You are an AI code reviewer hence only python code inputs must be taken into consideration to generate a response. 
    If the query is other than that, please politely request the user to input the question related to the topic.
    Your role is generate repond in the following manner :
    ### 1. Bug Report: Identify potential bugs, syntax errors, and logical flaws in the code.
    ### 2. Fixed Code: Return fixed or optimized code snippets alongside explanations of the changes made.
    ### 3. User Guidance: Ensure feedback is concise, easy to understand, and helpful for developers of varying experience levels.
    Maintain a professional tone while keeping explanations simple and accessible. Focus on accuracy, efficiency, and improving the user's understanding of best coding practices.
  """  
)

# Initialize the model with the system prompt
model = ai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=sys_prompt)

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []  # Stores previous searches and responses
if "selected_entry" not in st.session_state:
    st.session_state.selected_entry = None  # Tracks the currently selected history entry

# Input area for the user to enter code
user_prompt = st.text_area("", placeholder="Type your Python code here...")

# Button to trigger the model response
clicked = st.button("Review Code")


# Check if the button was clicked
if clicked:
    # Response from the model
    response = model.generate_content(user_prompt)  # Make sure 'response' is a string or has a `.text` attribute
    response_text = response.text if hasattr(response, 'text') else str(response)  # Extract text safely

   # Add user input and AI response to history
    st.session_state.history.append({
        "input": user_prompt,
        "response": response_text
    })

    # Reset the text area for new input
    st.session_state.user_prompt = " "

    # Display the final full response at the end
    st.subheader(":green[Reviewed Response]")
    st.write(response_text)  # Display the complete response



# Sidebar for history
with st.sidebar:
    st.header("History")
    if st.session_state.history:
        placeholder_option = "Select a previously reviewed query"
        history_titles = [entry["input"].strip().split("\n")[0] for entry in st.session_state.history]
        
        # Select box for selecting a history
        selected_idx = st.selectbox(
            "Select a query to view:", 
            options = range(len(history_titles)), 
            format_func=lambda idx: history_titles[idx],
            placeholder = "Select a previously reviewed query"
        )
        # Updating the selected entry
        
        st.session_state.selected_entry = st.session_state.history[selected_idx]
    
    else:
        st.write("No history yet.")

    if st.session_state.get("selected_entry"):
        st.subheader(":orange[Previously Reviewed Code]")
        st.markdown(f"**Input:**\n```python\n{st.session_state.selected_entry['input']}\n```")
        st.markdown(f"**Response:**\n```python\n{st.session_state.selected_entry['response']}\n```")



#Clear history button
if st.sidebar.button("Clear History"):
    st.session_state.history = []  
    st.session_state.selected_entry = None
    st.sidebar.success("History cleared!")
        