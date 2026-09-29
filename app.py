import streamlit as st
import subprocess
import json
from pathlib import Path

st.set_page_config(page_title="AgriBot", page_icon="🌾", layout="wide")

st.title("🌾 AgriBot – Agricultural Robot Simulator")
st.caption("Basic C++ OOP + Stack + Queue project with a Streamlit interface")

# This prototype keeps the simulation in Python for the UI,
# while the supplied C++ folder contains the subject-project core.
if "x" not in st.session_state:
    st.session_state.x = 0
    st.session_state.y = 0
    st.session_state.battery = 100
    st.session_state.status = "READY"
    st.session_state.history = []
    st.session_state.missions = []
    st.session_state.last_result = "Ready for a mission."

FIELD = [
    ["H","H","H","H","H"],
    ["H","H","W","H","H"],
    ["H","H","H","D","H"],
    ["H","H","H","H","H"],
    ["H","W","H","H","H"],
]

def move(dx, dy, name):
    nx = st.session_state.x + dx
    ny = st.session_state.y + dy
    if not (0 <= nx < 5 and 0 <= ny < 5):
        st.session_state.status = "Cannot move outside field."
        st.session_state.last_result = st.session_state.status
        return
    if st.session_state.battery < 2:
        st.session_state.status = "Battery too low."
        st.session_state.last_result = st.session_state.status
        return

    st.session_state.history.append(
        (st.session_state.x, st.session_state.y, st.session_state.battery)
    )
    st.session_state.x, st.session_state.y = nx, ny
    st.session_state.battery -= 2
    st.session_state.status = "MOVING"
    st.session_state.last_result = f"Robot moved {name}."

def inspect():
    if st.session_state.battery > 0:
        st.session_state.battery -= 1
    cell = FIELD[st.session_state.x][st.session_state.y]
    st.session_state.status = "INSPECTING"

    if cell == "H":
        result = "🌱 Crop Status: HEALTHY"
    elif cell == "W":
        result = "🌿 Crop Status: WEED DETECTED"
    else:
        result = "⚠️ Crop Status: POSSIBLE DISEASE"

    st.session_state.last_result = result

def undo():
    if not st.session_state.history:
        st.session_state.last_result = "Nothing to undo."
        return
    x, y, battery = st.session_state.history.pop()
    st.session_state.x, st.session_state.y = x, y
    st.session_state.battery = min(100, battery)
    st.session_state.status = "UNDO COMPLETED"
    st.session_state.last_result = "↩️ Last movement undone."

left, right = st.columns([1.5, 1])

with left:
    st.subheader("🗺️ Virtual Field")

    for i in range(5):
        cols = st.columns(5)
        for j in range(5):
            symbol = "🤖" if (i, j) == (st.session_state.x, st.session_state.y) else {
                "H": "🌱", "W": "🌿", "D": "🔴"
            }[FIELD[i][j]]
            cols[j].markdown(f"<div style='text-align:center;font-size:30px'>{symbol}<br><small>({i},{j})</small></div>", unsafe_allow_html=True)

    st.info(st.session_state.last_result)

    st.subheader("🎮 Robot Controls")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬆️ Up", use_container_width=True):
            move(-1, 0, "up")
    with c2:
        if st.button("🔍 Inspect", use_container_width=True):
            inspect()
    with c3:
        if st.button("↩️ Undo", use_container_width=True):
            undo()

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅️ Left", use_container_width=True):
            move(0, -1, "left")
    with c2:
        if st.button("⬇️ Down", use_container_width=True):
            move(1, 0, "down")
    with c3:
        if st.button("➡️ Right", use_container_width=True):
            move(0, 1, "right")

with right:
    st.subheader("🤖 Robot Status")
    st.metric("Battery", f"{st.session_state.battery}%")
    st.metric("Position", f"({st.session_state.x}, {st.session_state.y})")
    st.write("**Status:**", st.session_state.status)

    st.subheader("📋 Mission Queue")
    mission = st.selectbox(
        "Add a mission",
        ["Inspect", "Move Right", "Move Left", "Move Up", "Move Down", "Spray", "Return"]
    )
    if st.button("➕ Add Mission", use_container_width=True):
        st.session_state.missions.append(mission)

    if st.session_state.missions:
        for i, m in enumerate(st.session_state.missions, 1):
            st.write(f"{i}. {m}")
        if st.button("▶️ Execute Next Mission", use_container_width=True):
            m = st.session_state.missions.pop(0)
            if m == "Inspect":
                inspect()
            elif m == "Move Right":
                move(0, 1, "right")
            elif m == "Move Left":
                move(0, -1, "left")
            elif m == "Move Up":
                move(-1, 0, "up")
            elif m == "Move Down":
                move(1, 0, "down")
            elif m == "Spray":
                st.session_state.last_result = "💧 Spraying simulation completed after farmer approval."
                st.session_state.status = "SPRAYING"
            elif m == "Return":
                st.session_state.last_result = "🏠 Return-to-start mission completed."
                st.session_state.status = "RETURNING"
    else:
        st.caption("No missions in queue.")

    st.subheader("📜 Command History")
    if st.session_state.history:
        st.write(f"{len(st.session_state.history)} movement(s) stored in the undo stack.")
    else:
        st.caption("No movement history yet.")

st.divider()
st.caption("Project concept: the field conditions are simulated. A real camera/AI model can be added later as an extension.")
