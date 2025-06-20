import streamlit as st
import chess
import chess.svg
from PIL import Image
from io import BytesIO
import base64

# Title
st.title("♟️ Dhyan Chess")

# Initialize board in session
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

board = st.session_state.board

# Helper to convert SVG to PNG using Pillow (via base64 trick)
def render_board_svg(board):
    svg = chess.svg.board(board=board)
    # Convert SVG to base64 for img tag (Streamlit workaround)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    st.markdown(html, unsafe_allow_html=True)

# Display board
render_board_svg(board)

# Show game status
if board.is_checkmate():
    st.success("Checkmate!")
elif board.is_stalemate():
    st.info("Stalemate!")
elif board.is_insufficient_material():
    st.info("Draw due to insufficient material!")
elif board.is_check():
    st.warning("Check!")

# Show FEN and turn
st.text_area("Current Board (FEN)", value=board.fen(), height=80)
turn = "White" if board.turn == chess.WHITE else "Black"
st.markdown(f"**{turn} to move**")

# Move input
move = st.text_input("Enter your move (e.g., e2e4):")
if st.button("Make Move"):
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
            st.experimental_rerun()  # ✅ Force rerun to refresh board
        else:
            st.error("Illegal move!")
    except:
        st.error("Invalid move format!")

# Reset game
if st.button("Reset Game"):
    st.session_state.board = chess.Board()
    st.rerun()
