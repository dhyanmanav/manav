import streamlit as st
import chess

st.title("♟️ Dhyan Chess")

# Initialize board
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

board = st.session_state.board

# Show board state
st.text_area("Current Board (FEN)", value=board.fen(), height=80)

# Show whose turn it is
turn = "White" if board.turn == chess.WHITE else "Black"
st.write(f"**{turn} to move**")

# Move input
move = st.text_input("Enter your move (e.g., e2e4):")

# Handle move
if st.button("Make Move"):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
        else:
            st.error("Illegal move!")
    except:
        st.error("Invalid move format!")

# Reset game
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
