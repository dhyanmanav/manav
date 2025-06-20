import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import cairosvg

# Title
st.title("♟️ Simple Streamlit Chess App")

# Initialize the board in session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Display the board as an SVG converted to PNG
def chessboard_to_image(board):
    svg = chess.svg.board(board=board)
    png_bytes = cairosvg.svg2png(bytestring=svg)
    return png_bytes

st.image(chessboard_to_image(st.session_state.board))

# Input move
move = st.text_input("Enter your move (e.g., e2e4):")

if st.button("Make Move"):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in st.session_state.board.legal_moves:
            st.session_state.board.push(chess_move)
        else:
            st.error("Illegal move!")
    except:
        st.error("Invalid move format!")

# Reset button
if st.button("Reset Game"):
    st.session_state.board = chess.Board()

# Display game status
if st.session_state.board.is_checkmate():
    st.success("Checkmate!")
elif st.session_state.board.is_stalemate():
    st.info("Stalemate!")
elif st.session_state.board.is_insufficient_material():
    st.info("Draw due to insufficient material!")
elif st.session_state.board.is_check():
    st.warning("Check!")

st.write("FEN:", st.session_state.board.fen())
