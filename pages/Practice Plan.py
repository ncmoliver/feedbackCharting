import streamlit as st
import pandas as pd

# Initialize session state for practice plan
if 'practice_plan' not in st.session_state:
    st.session_state.practice_plan = []
if 'total_practice_time' not in st.session_state:
    st.session_state.total_practice_time = 60
if 'used_time' not in st.session_state:
    st.session_state.used_time = 0
if 'selected_drill' not in st.session_state:
    st.session_state.selected_drill = None  # Track the selected drill index for editing

# Function to add a drill to the practice plan
def add_drill(name, category, focus, duration, importance):
    if st.session_state.used_time + duration <= st.session_state.total_practice_time:
        st.session_state.practice_plan.append({
            'Drill Name': name,
            'Category': category,
            'Focus': focus,
            'Duration (mins)': duration,
            'Importance': importance
        })
        st.session_state.used_time += duration
    else:
        st.sidebar.warning("Not enough remaining time for this drill!")

# Function to clear the practice plan
def clear_plan():
    st.session_state.practice_plan = []
    st.session_state.used_time = 0
    st.session_state.selected_drill = None  # Reset selection

# Function to delete a drill
def delete_drill(index):
    if 0 <= index < len(st.session_state.practice_plan):
        removed_drill = st.session_state.practice_plan.pop(index)
        st.session_state.used_time -= removed_drill['Duration (mins)']
        st.session_state.selected_drill = None  # Reset selection
        st.rerun()

# Function to update a drill
def update_drill(index, new_name, new_category, new_focus, new_duration, new_importance):
    if 0 <= index < len(st.session_state.practice_plan):
        prev_duration = st.session_state.practice_plan[index]['Duration (mins)']
        st.session_state.practice_plan[index] = {
            'Drill Name': new_name,
            'Category': new_category,
            'Focus': new_focus,
            'Duration (mins)': new_duration,
            'Importance': new_importance
        }
        # Adjust used time
        st.session_state.used_time += new_duration - prev_duration
        st.session_state.selected_drill = None  # Reset selection
        st.rerun()

# Streamlit UI layout
st.title("🏀 Basketball Practice Plan Customizer")
st.sidebar.header("Practice Customization Toolbar")

# Sidebar customization inputs
st.session_state.total_practice_time = st.sidebar.slider("Total Practice Time (minutes)", min_value=30, max_value=180, value=60, step=10)
remaining_time = st.session_state.total_practice_time - st.session_state.used_time

st.sidebar.text(f"⏳ Time Used: {st.session_state.used_time} mins")
st.sidebar.text(f"🕒 Time Remaining: {remaining_time} mins")

# Check if a drill is selected for editing
if st.session_state.selected_drill is not None:
    st.sidebar.subheader("Edit Selected Drill")
    drill = st.session_state.practice_plan[st.session_state.selected_drill]

    edited_name = st.sidebar.text_input("Drill Name", value=drill["Drill Name"], key="edit_name")
    edited_category = st.sidebar.selectbox("Category", ["Offense", "Defense", "Transition", "Shooting", "Conditioning"], index=["Offense", "Defense", "Transition", "Shooting", "Conditioning"].index(drill["Category"]), key="edit_category")
    edited_focus = st.sidebar.text_input("Drill Focus", value=drill["Focus"], key="edit_focus")
    edited_duration = st.sidebar.slider("Duration (minutes)", 5, 60, drill["Duration (mins)"], key="edit_duration")
    edited_importance = st.sidebar.selectbox("Importance", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(drill["Importance"]), key="edit_importance")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("✅ Save Changes"):
            update_drill(st.session_state.selected_drill, edited_name, edited_category, edited_focus, edited_duration, edited_importance)
    with col2:
        if st.sidebar.button("❌ Delete Drill"):
            delete_drill(st.session_state.selected_drill)

else:
    # Default input fields when no drill is selected
    st.sidebar.subheader("Add New Drill")
    category = st.sidebar.selectbox("Select Drill Category", ["Offense", "Defense", "Transition", "Shooting", "Conditioning"])
    focus = st.sidebar.text_input("Drill Focus (e.g., Fast Break, Pick & Roll, Zone Defense)")
    duration = st.sidebar.slider("Drill Duration (minutes)", 5, 60, 15)
    importance = st.sidebar.selectbox("Importance Level", ["High", "Medium", "Low"])

    if st.sidebar.button("➕ Add Drill"):
        if focus:
            add_drill(f"{category} - {focus}", category, focus, duration, importance)
            st.sidebar.success("✅ Drill added to practice plan!")
        else:
            st.sidebar.warning("⚠️ Please enter a drill focus.")

if st.sidebar.button("🗑️ Clear Plan"):
    clear_plan()
    st.sidebar.success("Practice plan cleared!")

# Display practice plan
st.header("📋 Customized Practice Plan")
if st.session_state.practice_plan:
    df = pd.DataFrame(st.session_state.practice_plan)
    for i, row in df.iterrows():
        if st.button(f"📌 {row['Drill Name']}", key=f"toggle_{i}"):
            st.session_state.selected_drill = i if st.session_state.selected_drill != i else None
            st.rerun()
else:
    st.write("🚨 No drills added yet. Use the sidebar to start building your practice plan.")