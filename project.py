import streamlit as st
import random
import time

st.set_page_config(page_title="Dot Dodge Game", layout="centered")
st.title("🎮 Dot Dodge - Avoid the Red Dots!By:Dhyan")

# Initialize game state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 5
    st.session_state.dots = []
    st.session_state.score = 0
    st.session_state.game_over = False

# Game constants
WIDTH = 10
HEIGHT = 12

# Player move
move = st.radio("Move", ["⬅️", "Stay", "➡️"], index=1, horizontal=True)

# Game area
game_area = st.empty()

# Main game loop
if not st.session_state.game_over:
    for step in range(1000):  # Long enough loop
        # Move player
        if move == "⬅️" and st.session_state.player_pos > 0:
            st.session_state.player_pos -= 1
        elif move == "➡️" and st.session_state.player_pos < WIDTH - 1:
            st.session_state.player_pos += 1

        # Spawn red dot
        if random.random() < 0.2:
            st.session_state.dots.append([random.randint(0, WIDTH - 1), 0])

        # Move red dots
        for dot in st.session_state.dots:
            dot[1] += 1

        # Check collision
        for dot in st.session_state.dots:
            if dot[0] == st.session_state.player_pos and dot[1] == HEIGHT - 1:
                st.session_state.game_over = True
                break

        # Filter out dots out of bounds
        st.session_state.dots = [dot for dot in st.session_state.dots if dot[1] < HEIGHT]

        # Draw board
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
        game_area.markdown(f"```\n{board}\n```")
        st.session_state.score += 1
        time.sleep(0.2)
else:
    st.error(f"💥 Game Over! Final Score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for key in ["player_pos", "dots", "score", "game_over"]:
            del st.session_state[key]
        st.rerun()
