import streamlit as st
import streamlit.components.v1 as components

st.title("♟️ Drag-and-Drop Chess in Streamlit")

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      #board {
        width: 400px;
        margin: auto;
      }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chess.js@1.0.0/chess.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chessboardjs@1.0.0/dist/chessboard.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/chessboardjs@1.0.0/dist/chessboard.min.css" />
  </head>
  <body>
    <div id="board"></div>
    <p style="text-align:center;"><strong>Status:</strong> <span id="status"></span></p>
    <script>
      var board = null;
      var game = new Chess();

      function onDragStart (source, piece) {
        if (game.game_over() ||
            (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
            (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
          return false;
        }
      }

      function onDrop (source, target) {
        var move = game.move({
          from: source,
          to: target,
          promotion: 'q'
        });

        if (move === null) return 'snapback';
        updateStatus();
      }

      function onSnapEnd () {
        board.position(game.fen());
      }

      function updateStatus () {
        var status = '';
        var moveColor = game.turn() === 'b' ? 'Black' : 'White';

        if (game.in_checkmate()) {
          status = 'Game over, ' + moveColor + ' is in checkmate.';
        } else if (game.in_draw()) {
          status = 'Game over, drawn position.';
        } else {
          status = moveColor + ' to move';
          if (game.in_check()) {
            status += ', ' + moveColor + ' is in check';
          }
        }

        document.getElementById('status').innerText = status;
      }

      board = Chessboard('board', {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
      });

      updateStatus();
    </script>
  </body>
</html>
"""

# Make sure height is sufficient (>= 550)
components.html(html_code, height=600)
