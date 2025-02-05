import streamlit as st

# Page Title
st.markdown("## 📚 Coaches Corner")
st.write("A free one-month self-paced course to strengthen fundamental basketball knowledge for championship-caliber coaches.")

# Create a structured layout using columns
st.markdown("---")

st.markdown("### 🧾 Course Syllabus", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])  # Creates a sidebar column and main content column
with col1:
    week1 = st.button("🏀 Week 1")
with col2:
    if week1:
        st.markdown("#### Understanding The Sentiments Of Basketball From A Player Perspective")
        st.write(
            "Week 1 is about understanding the impact of your coaching decisions. "
            "This module highlights the depth and power behind every decision you make."
        )

st.markdown("---")  # Separator
with col1:
    week2 = st.button("🏀 Week 2")
with col2:
    if week2:
        st.markdown("#### Coaching A Player Through The Process")
        st.write(
            "Week 2 focuses on the game’s processes. We’ll explore how players transition from A to B, "
            "helping you approach each situation uniquely based on its demands."
        )


with col1:
    week3 = st.button("🏀 Week 3")
with col2:
    if week3:
        st.markdown("#### Systematic Connections From Practice To Game")
        st.write(
            "Week 3 is all about getting results. Learn how to become a result-driven coach by installing, adjusting, "
            "and trusting your system to optimize performance."
        )

with col1:
    week4 = st.button("🏀 Week 4")
with col2:
    if week4:
        st.markdown("#### Adhering To The Expectation of The Game")
        st.write(
            "Week 4 emphasizes decision-making. Basketball teaches responsibility and accountability, and this module ensures "
            "you are prepared for sustainable change in the dynamic game."
        )




