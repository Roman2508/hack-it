const board = document.getElementById("board")
const positions = [
  { left: 5, top: 85 },
  { left: 12, top: 85 },
  { left: 19, top: 85 },
  { left: 26, top: 85 },
  { left: 33, top: 85 },
  { left: 40, top: 85 },
  { left: 40, top: 75 },
  { left: 40, top: 65 },
  { left: 33, top: 65 },
  { left: 26, top: 65 },
  { left: 19, top: 65 },
  { left: 12, top: 65 },
  { left: 5, top: 65 },
  { left: 5, top: 55 },
  { left: 12, top: 55 },
  { left: 19, top: 55 },
  { left: 26, top: 55 },
  { left: 33, top: 55 },
  { left: 40, top: 55 },
  { left: 40, top: 45 },
  { left: 33, top: 45 },
  { left: 26, top: 45 },
  { left: 19, top: 45 },
  { left: 12, top: 45 },
  { left: 5, top: 45 },
  { left: 5, top: 35 },
  { left: 12, top: 35 },
  { left: 19, top: 35 },
  { left: 26, top: 35 },
  { left: 33, top: 35 },
  { left: 40, top: 35 },
  { left: 47, top: 35 },
  { left: 47, top: 25 },
]

let cells = []

// Створення клітинок
positions.forEach((pos, index) => {
  const cell = document.createElement("div")
  cell.classList.add("cell")
  cell.style.left = pos.left + "vw"
  cell.style.top = pos.top + "vh"
  cell.textContent = index + 1
  board.appendChild(cell)
  cells.push(cell)
})

// Створення фішки
const token = document.createElement("div")
token.classList.add("token")
token.style.position = "absolute"
board.appendChild(token)

// Початкове положення
let currentCell = cells[0]
moveTokenToCell(currentCell)

let isDragging = false

token.addEventListener("mousedown", (e) => {
  isDragging = true
})

document.addEventListener("mousemove", (e) => {
  if (isDragging) {
    token.style.left = e.clientX - token.offsetWidth / 2 + "px"
    token.style.top = e.clientY - token.offsetHeight / 2 + "px"
  }
})

document.addEventListener("mouseup", (e) => {
  if (isDragging) {
    isDragging = false
    snapToClosestCell(e.clientX, e.clientY)
  }
})

// Перемістити фішку в центр клітинки
function moveTokenToCell(cell) {
  const rect = cell.getBoundingClientRect()
  token.style.left = rect.left + rect.width / 2 - token.offsetWidth / 2 + "px"
  token.style.top = rect.top + rect.height / 2 - token.offsetHeight / 2 + "px"
}

// Приліпити фішку до найближчої клітинки
function snapToClosestCell(mouseX, mouseY) {
  let minDistance = Infinity
  let closestCell = null
  cells.forEach((cell) => {
    const rect = cell.getBoundingClientRect()
    const cellCenterX = rect.left + rect.width / 2
    const cellCenterY = rect.top + rect.height / 2
    const dx = mouseX - cellCenterX
    const dy = mouseY - cellCenterY
    const distance = Math.sqrt(dx * dx + dy * dy)
    if (distance < minDistance) {
      minDistance = distance
      closestCell = cell
    }
  })
  if (closestCell) {
    moveTokenToCell(closestCell)
    currentCell = closestCell
  }
}
