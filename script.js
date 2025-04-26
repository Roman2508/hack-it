const board = document.getElementById("board");
const positions = [
  { left: 5, top: 80 },
  { left: 12, top: 80 },
  { left: 19, top: 80 },
  { left: 26, top: 80 },
  { left: 33, top: 80 },
  { left: 40, top: 80 },
  { left: 40, top: 70 },
  { left: 40, top: 60 },
  { left: 33, top: 60 },
  { left: 26, top: 60 },
  { left: 19, top: 60 },
  { left: 12, top: 60 },
  { left: 5, top: 60 },
  { left: 5, top: 50 },
  { left: 12, top: 50 },
  { left: 19, top: 50 },
  { left: 26, top: 50 },
  { left: 33, top: 50 },
  { left: 40, top: 50 },
  { left: 40, top: 40 },
  { left: 33, top: 40 },
  { left: 26, top: 40 },
  { left: 19, top: 40 },
  { left: 12, top: 40 },
  { left: 5, top: 40 },
  { left: 5, top: 30 },
  { left: 12, top: 30 },
  { left: 19, top: 30 },
  { left: 26, top: 30 },
  { left: 33, top: 30 },
  { left: 40, top: 30 },
  { left: 47, top: 30 },
  { left: 47, top: 20 },
];

let cells = [];

// Створити клітинки за позиціями
positions.forEach((pos, index) => {
  const cell = document.createElement("div");
  cell.classList.add("cell");
  cell.style.left = pos.left + "vw";
  cell.style.top = pos.top + "vh";
  cell.textContent = index + 1;
  board.appendChild(cell);
  cells.push(cell);
});

// Створити фішку
const token = document.createElement("div");
token.classList.add("token");
token.setAttribute("draggable", "true");
cells[0].appendChild(token);

// Налаштування drag & drop
let dragged = null;

token.addEventListener("dragstart", (e) => {
  dragged = token;
  setTimeout(() => {
    token.style.display = "none";
  }, 0);
});

token.addEventListener("dragend", (e) => {
  setTimeout(() => {
    token.style.display = "block";
    dragged = null;
  }, 0);
});

cells.forEach((cell) => {
  cell.addEventListener("dragover", (e) => {
    e.preventDefault();
  });

  cell.addEventListener("drop", (e) => {
    if (dragged) {
      cell.appendChild(dragged);
    }
  });
});
