import streamlit as st

# --- Game Logic Functions ---

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],   # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],   # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    for combo in win_conditions:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None

# --- Streamlit App ---

st.set_page_config("Tic-Tac-Toe Game 🎮", layout="centered")
st.title("❌🔵 Tic-Tac-Toe (XOX) Game")
st.markdown("Play against a friend — take turns!")

# --- Initialize session state ---
if "board" not in st.session_state:
    reset_game()

board = st.session_state.board
current_player = st.session_state.current_player
winner = st.session_state.winner

# --- Game Board UI ---
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        if board[i] == "":
            if not winner:
                if st.button(" ", key=i, help=f"Cell {i+1}"):
                    board[i] = current_player
                    st.session_state.winner = check_winner(board)
                    if not st.session_state.winner:
                        st.session_state.current_player = "O" if current_player == "X" else "X"
                    st.experimental_rerun()
        else:
            st.markdown(f"### {board[i]}")

# --- Game Status ---
if winner == "Draw":
    st.info("It's a draw! 🤝")
elif winner:
    st.success(f"🎉 Player {winner} wins!")
else:
    st.write(f"Current Player: **{current_player}**")

# --- Reset Button ---
if st.button("🔄 Restart Game"):
    reset_game()
    st.experimental_rerun()
