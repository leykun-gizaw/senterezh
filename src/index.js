import './header.css';
import './indexMain.css';
import 'jquery';
import '@chrisoakman/chessboardjs/dist/chessboard-1.0.0.min';
import { Chess } from 'chess.js';

let board1 = null;
let board2 = null;
const game = new Chess();

function makeRandomMove1() {
  const possibleMoves = game.moves();

  // exit if the game is over
  if (game.game_over()) return;

  const randomIdx = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIdx]);
  board1.position(game.fen());

  window.setTimeout(makeRandomMove1, 500);
}

const config = {
  draggable: true,
  position: 'start',
};
config.pieceTheme = '/static/img/chesspieces/wikipedia/{piece}.png'

board1 = Chessboard('board1', config);
board2 = Chessboard('board2', config);

window.setTimeout(makeRandomMove1, 500);
