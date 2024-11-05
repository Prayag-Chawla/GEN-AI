import streamlit as st
from transformers import pipeline

# Load a Hugging Face text generation model
generator = pipeline("text-generation", model="distilgpt2")

# Function to get response from the model
def get_model_response(input_text, no_words, blog_style):
    prompt = (f"Write a {blog_style} blog post on the topic '{input_text}' "
              f"that is insightful and engaging, within {no_words} words. "
              "Ensure the content is original and does not reference any external articles or sources.")
    
    # Generate the response
    response = generator(prompt, max_length=int(no_words) + 50, num_return_sequences=1, temperature=0.7, top_k=50)[0]['generated_text']
    
    # Return the generated text truncated to the desired word count
    generated_content = ' '.join(response.split()[:int(no_words)])

    # Basic filtering to avoid inappropriate references
    filtered_content = " ".join([word for word in generated_content.split() if "GreenMedInfo" not in word and "copyright" not in word])

    return filtered_content

# Streamlit page configuration
st.set_page_config(
    page_title="Generate Blogs",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Blogs 🤖")

# Blog topic input
input_text = st.text_input("Enter the Blog Topic", "")

# Columns for additional fields
col1, col2 = st.columns(2)

# Number of words input
with col1:
    no_words = st.text_input('Number of Words', '100')  # Default to 100 words

# Blog style selection
with col2:
    blog_style = st.selectbox(
        'Writing the blog for',
        ('Researchers', 'Data Scientist', 'Common People'),
        index=0
    )

# Button to generate the blog
submit = st.button("Generate")

# Display the generated blog response
if submit:
    # Check for empty inputs and validate numeric value
    if not input_text:
        st.warning("Please enter a blog topic.")
    elif not no_words.isdigit() or int(no_words) <= 0:
        st.warning("Please enter a valid positive number of words.")
    else:
        response = get_model_response(input_text, int(no_words), blog_style)
        st.markdown(response)  # Properly format the output as markdown
