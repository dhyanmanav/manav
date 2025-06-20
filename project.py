import streamlit as st
import random

st.set_page_config(page_title="Dot Dodge Game", layout="centered")
st.title("🎮 Dot Dodge - Click to Move")

# Game constants
WIDTH = 10
HEIGHT = 12

# Initialize session state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = WIDTH // 2
    st.session_state.dots = []
    st.session_state.score = 0
    st.session_state.game_over = False

# Game step: move dots, spawn new one, check collision
def game_step():
    # Move red dots down
    for dot in st.session_state.dots:
        dot[1] += 1

    # Spawn new red dot at top
    if random.random() < 0.3:
        st.session_state.dots.append([random.randint(0, WIDTH - 1), 0])

    # Keep only dots on screen
    st.session_state.dots = [dot for dot in st.session_state.dots if dot[1] < HEIGHT]

    # Check collision
    for dot in st.session_state.dots:
        if dot[0] == st.session_state.player_pos and dot[1] == HEIGHT - 1:
            st.session_state.game_over = True
            break

    st.session_state.score += 1

# Draw board
def draw_board():
    board = ""
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if [x, y] in st.session_state.dots:
                row += "🔴"
            elif y == HEIGHT - 1 and x == st.session_state.player_pos:
                row += "🔵"
            else:
                row += "⬛"
        board += row + "\n"
    return board

# Move buttons at bottom
st.markdown(f"```\n{draw_board()}\n```")

# Score display
st.caption(f"Score: {st.session_state.score}")

# Game over message
if st.session_state.game_over:
    st.error(f"💥 Game Over! Final Score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Left", use_container_width=True):
            if st.session_state.player_pos > 0:
                st.session_state.player_pos -= 1
            game_step()
            st.rerun()

    with col2:
        if st.button("➡️ Right", use_container_width=True):
            if st.session_state.player_pos < WIDTH - 1:
                st.session_state.player_pos += 1
            game_step()
            st.rerun()
