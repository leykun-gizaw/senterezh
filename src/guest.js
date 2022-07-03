import './header.css';
import './guestMain.css';
import 'jquery';
import '@chrisoakman/chessboardjs/dist/chessboard-1.0.0.min';
import { Chess } from 'chess.js';
import updateHistory from './history';

let board = null;
export const game = new Chess();

// Setup socketio
export const socket = io();

const pathArray = window.location.pathname.split('/');
const roomAndInterval = pathArray[pathArray.length - 1].split('_');

// Get the room uuid and game interval
const room = roomAndInterval[roomAndInterval.length - 1];
const gameInterval = roomAndInterval[0].replace('%20', ' ');

// Just setting up a socketio connection from the client side
socket.on('connect', () => {
  socket.send('User connected');
});

/*
 * When the server acknowledges the connection setup above,
 * we extract the room uuid sent from /guest endpoint of the server.
 * We then send that through the socket attached to the `join`
 * event. Server will setup a room with that uuid.
 */
socket.on('connected', () => {
  socket.emit('join', { room, gameInterval });
});

/*
 * Log the acknowldegement message sent from the server regarding
 * our request to join a room with a uuid the server sent through
 * the url path
 */
socket.on('room joined', (msg) => {
  if (msg.sid === socket.id) board.orientation(msg.orientation);
});

/*
 * Capture the chatbox and the history area and add an Enter key
 * event listener. Then upon the keypress event, we send a socketio
 * message attached to `communicate` event. The message contains
 * the chatbox value, the socket id of the client, and the room uuid
 * all required by the backend to handle room messaging.
 */
const chatBox = document.getElementById('c_text');
const history = document.getElementById('c_history');
chatBox.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    socket.emit('communicate', { data: chatBox.value, room });
    const me = document.createElement('p');
    me.innerHTML = `me => ${chatBox.value}`;
    history.appendChild(me);
  }
});

/*
 * Listen to returning messages from the connected room and append
 * to the chat history box
 */
socket.on('response', (msg) => {
  if (msg.sid !== socket.id) {
    const opponent = document.createElement('p');
    opponent.innerHTML = `opponent => ${msg.data}`;
    history.appendChild(opponent);
  }
});

function updateStatus() {
  updateHistory(game);
}

/*
 * Listen to returning messages from the connected room and change
 * board position according to server's response.
 */
socket.on('fen response', (msg) => {
  if (msg.sid !== socket.id) {
    console.log(msg);
    board.position(msg.fenString);
  }
});

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd() {
  board.position(board.fen());
  socket.emit('fen exchange', { room, fenString: board.fen() });
}

const config = {
  draggable: true,
  position: 'start',
  onSnapEnd,
};
// Change default location of chesspieces to start with `/static`
config.pieceTheme = '/static/img/chesspieces/wikipedia/{piece}.png';

board = Chessboard('board1', config);

updateStatus();
