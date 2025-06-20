import streamlit as st
import chess
import chess.svg

# Title
st.title("♟️ Dhyan CHESS")

# Initialize board in session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Function to render SVG in Streamlit
def render_svg(svg_content):
    """Embed raw SVG content using markdown (safe HTML injection)."""
    st.markdown(f"<div style='text-align:center'>{svg_content}</div>", unsafe_allow_html=True)

# Draw the board
svg_board = chess.svg.board(board=st.session_state.board)
render_svg(svg_board)

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

# Game status
if st.session_state.board.is_checkmate():
    st.success("Checkmate!")
elif st.session_state.board.is_stalemate():
    st.info("Stalemate!")
elif st.session_state.board.is_insufficient_material():
    st.info("Draw due to insufficient material!")
elif st.session_state.board.is_check():
    st.warning("Check!")

st.write("FEN:", st.session_state.board.fen())
