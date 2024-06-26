import base64
import streamlit as st
import plotly.express as px
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
from openai._client import (
    OpenAI,
)  # very important to write openai.client due to version of openai blah blah
from streamlit_carousel import carousel


single_image = dict(
    title="",
    text="",
    interval=None,
    img="",
)


client = OpenAI(api_key=openai_api_key)
genai.configure(api_key=google_gemini_api_key)

generation_config = {
    "temperature": 0.9,  # controls randomness during text generation
    "top_p": 1,  # influences which word are to be selected after current word
    "top_k": 1,  #  forces the model to pick the single most probable word to continue the sequence.
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

st.set_page_config(layout="wide")


# title
st.title("BlogCraft : AI Writing Comapnion")

st.subheader("Create blogs with the help of AI")
with st.sidebar:
    st.title("Input Details")
    st.subheader("Enter details of the blog you wanna generate")

    blog_title = st.text_input("Blog Title")
    keywords = st.text_input("Keywords (comma-separated)")

    # number of words
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=250)
    num_images = st.number_input("Number of images", min_value=1, max_value=5, step=1)

    prompt_parts = [
        f'Generate a comprehensive, engaging blog post relevant to the given title "{blog_title}" and keywords "{keywords}". Make sure to incorporate these keywords into the blog. The blog should be approximately {num_words} '
    ]
    submit_button = st.button("Generate Blog")

if submit_button:
    response = model.generate_content(prompt_parts)
    images = []
    images_gallery = []

    for i in range(num_images):
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Generate an image based on the title : {blog_title}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        new_image = single_image.copy()  # copying dict into new_image
        new_image["title"] = f"Image{i+1}"
        new_image["text"] = f"{blog_title}"
        new_image["img"] = image_response.data[0].url
        images_gallery.append(new_image)

    st.title("Your Blog Images : ")
    carousel(items=images_gallery, width=1)

    st.title("Your Blog Post : ")
    st.write(response.text)
