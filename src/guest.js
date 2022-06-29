/* eslint-disable quotes */
import "./header.css";
import "./guestMain.css";
import "jquery";
import "@chrisoakman/chessboardjs/dist/chessboard-1.0.0.min";
import { Chess } from "chess.js";

let board = null;
const game = new Chess();

function onDragStart(source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false;

  // only pick up pieces for the side to move
  if (
    (game.turn() === "w" && piece.search(/^b/) !== -1) ||
    (game.turn() === "b" && piece.search(/^w/) !== -1)
  ) {
    return false;
  }
  return true;
}

function updateStatus() {
  let status = "";

  let moveColor = "White";
  if (game.turn() === "b") {
    moveColor = "Black";
  }

  // checkmate?
  if (game.in_checkmate()) status = `Game over ${moveColor} is in checkmate.`;

  // draw?
  else if (game.in_draw()) status = "Game over, drawn position";

  // game still on
  else {
    status = `${moveColor} to move`;

    // check?
    if (game.in_check()) {
      status += `, ${moveColor} is in check`;
    }
  }
  const rows = document.getElementById('history').firstElementChild;

  const movesArray = game.pgn(
    { max_width: 2, newline_char: '\n' },
  ).split('\n').map((move) => move.split(' '));

  const row = document.createElement('tr');
  if (rows.lastElementChild) {
    if (movesArray[movesArray.length - 1][0] === rows.lastElementChild.firstElementChild.innerHTML) {
      rows.lastElementChild.remove();
    }
  }
  movesArray[movesArray.length - 1].forEach((move) => {
    const data = document.createElement('td');
    if (movesArray[movesArray.length - 1][0] === move) {
      data.classList.add('count');
    }
    data.innerHTML = move;
    row.appendChild(data);
  });
  rows.append(row);
}

function onDrop(source, target) {
  // see if the move is legal
  const move = game.move({
    from: source,
    to: target,
    promotion: "q", // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return "snapback";

  updateStatus();
  return '';
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd() {
  board.position(game.fen());
}

const config = {
  draggable: true,
  position: "start",
  onDragStart,
  onDrop,
  onSnapEnd,
};
board = Chessboard("board1", config);
console.log(game.pgn());
