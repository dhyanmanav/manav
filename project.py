import streamlit as st
import random
import time

st.set_page_config(page_title="Dot Dodge Game", layout="centered")
st.title("🎮 Dot Dodge - Manual Button Mode")

# Constants
WIDTH = 10
HEIGHT = 12

# Init session state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = WIDTH // 2
    st.session_state.dots = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.step_count = 0

# Game logic
def game_step():
    # Move falling red dots
    for dot in st.session_state.dots:
        dot[1] += 1

    # Possibly spawn new red dot
    if random.random() < 0.3:
        st.session_state.dots.append([random.randint(0, WIDTH - 1), 0])

    # Remove dots out of screen
    st.session_state.dots = [dot for dot in st.session_state.dots if dot[1] < HEIGHT]

    # Check for collision
    for dot in st.session_state.dots:
        if dot[0] == st.session_state.player_pos and dot[1] == HEIGHT - 1:
            st.session_state.game_over = True

    st.session_state.step_count += 1
    st.session_state.score += 1

# Handle input buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️ Left", use_container_width=True):
        if st.session_state.player_pos > 0:
            st.session_state.player_pos -= 1
        game_step()

with col2:
    if st.button("⬇️ Stay", use_container_width=True):
        game_step()

with col3:
    if st.button("➡️ Right", use_container_width=True):
        if st.session_state.player_pos < WIDTH - 1:
            st.session_state.player_pos += 1
        game_step()

# Draw game board
def draw_board():
    board = ""
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            char = "⬛"
            if [x, y] in st.session_state.dots:
                char = "🔴"
            elif y == HEIGHT - 1 and x == st.session_state.player_pos:
                char = "🔵"
            row += char
        board += row + "\n"
    return board

# Display board
st.markdown(f"```\n{draw_board()}\n```")

# Game over
if st.session_state.game_over:
    st.error(f"💥 Game Over! Final Score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.caption(f"Score: {st.session_state.score}")
