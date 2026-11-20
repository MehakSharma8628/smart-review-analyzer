
import streamlit as st
from text_analyzer import analyze

# Page configuration
st.set_page_config(
    page_title="Smart Review Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Main heading
st.title("🔍 Smart Review Analyzer")
st.write(
    "Analyze customer reviews using Natural Language Processing "
    "(NLP) and Sentiment Analysis."
)

st.markdown("---")


# Function to format keywords
def format_keywords(keywords):
    formatted = []

    for item in keywords:
        if isinstance(item, (tuple, list)):
            if len(item) >= 2:
                formatted.append(f"{item[0]} ({item[1]})")
            elif len(item) == 1:
                formatted.append(str(item[0]))
        else:
            formatted.append(str(item))

    return formatted


# Review input
st.subheader("Enter Customer Review")

review = st.text_area(
    "Write or paste a customer review below:",
    placeholder="Example: The food was delicious and the staff was very friendly. I really enjoyed my experience!",
    height=180
)

# Analyze button
if st.button("Analyze Review", type="primary"):

    if not review.strip():
        st.warning("Please enter a review before clicking Analyze.")

    else:
        with st.spinner("Analyzing your review..."):

            result = analyze(review)

        st.success("Review analyzed successfully!")

        st.markdown("---")
        st.header("📊 Analysis Results")

        # Sentiment
        st.subheader("😊 Sentiment")
        sentiment = result.get("sentiment", "Not available")
        st.info(str(sentiment))

        # Keywords
        st.subheader("🔑 Extracted Keywords")
        keywords = format_keywords(result.get("keywords", []))

        if keywords:
            st.write(", ".join(keywords))
        else:
            st.write("No keywords found.")

        # Entities
        st.subheader("🏷️ Detected Entities")
        entities = result.get("entities", {})

        if entities:
            st.json(entities)
        else:
            st.write("No entities detected.")

        # Summary
        st.subheader("📝 Review Summary")
        summary = result.get("summary", "No summary available.")
        st.write(summary)

        st.markdown("---")
        st.caption("Smart Review Analyzer | NLP-Based Text Analysis Project")


# Footer
st.markdown("---")
st.caption("Developed using Python, Streamlit and NLP.")
