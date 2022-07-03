/**
 * History table updater.
 * @module history
 */

/**
 * Updates history table with moves
 * @param {GameInstance} game instance
 */
export default function updateHistory(game) {
  const rows = document.getElementById('history')
    .firstElementChild;

  // Create a 2D array of moves
  const movesArr = game.pgn(
    { max_width: 2, newline_char: '\n' },
  ).split('\n').map((move) => move.split(' '));

  // Prepare a table row to put moves in
  const row = document.createElement('tr');

  /*
   * Make sure if first move has been appended the second
   * move is next to it and not on a separate row by removing
   * the first move row and adding the new row.
   */
  if (rows.lastElementChild !== null) {
    /* Check if first column (column that shows moves count) is same
     * as the current pgn's moves count value and decide the fate of
     * that row's existence.
     */
    if (movesArr.at(-1)[0]
      === rows.lastElementChild.firstElementChild.innerHTML
    ) rows.lastElementChild.remove();
  }

  /*
   * Prepare row datas for a particular pgn upon a move
   */
  movesArr.at(-1).forEach((move) => {
    const data = document.createElement('td');
    if (movesArr.at(-1)[0] === move) {
      data.classList.add('count');
    }
    data.innerHTML = move;
    row.appendChild(data);
  });
  rows.append(row);
}
