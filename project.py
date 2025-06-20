import streamlit as st
import chess
import chess.svg

# Title
st.title("♟️ Simple Streamlit Chess App (No cairosvg)")

# Initialize the board in session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Display the board as SVG directly
def render_svg(svg_content):
    """Renders the given SVG string in Streamlit."""
    st.image(svg_content.encode("utf-8"), format="svg")

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
