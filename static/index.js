const menuTrigger = document.querySelector(".menu-trigger")
const mainMenuContainer = document.querySelector(".main-menu-container")

menuTrigger.addEventListener("click", () => {
  mainMenuContainer.classList.toggle("main-menu-opened")
})

const descriptionArray = [
  "Коли радості немає меж",
  "Любов в кожному пікселі",
  "Фото заряджене позитивом",
  "Зловив дзен",
  "Як мало потрібно для щастя",
  "Знали б ви що в мене на умі! ;)",
  "Show must go on",
  "Good vibes only",
  "My inspiration",
  "On my way to paradise",
  "Що це, якщо не любов? Х)",
]

const commentsArray = [
  "Цей кадр нереально крутий! :)",
  "Ти вмієш дивувати! Кожен кадр - поєднання життєлюбності і краси",
  "Спинися мить, прекрасна ти!",
  "Просто супер! Як тобі це вдається?",
  "Це прото шедевр мистецтва",
  "В цьому штучному світі так приємно знайти щось натуральне))",
  "Клас!!!))",
  "Нереально чудово!",
  "А ти вмієш дивувати ;)",
  "Це фото так і проситься в рамочку на стіну",
]

function createPictures(number) {
  const photos = []

  for (let i = 0; i < number; i++) {
    const randomDescriptionIndex = Math.floor(Math.random() * (descriptionArray.length - 1))
    const comments = []

    for (let i = 0; i < Math.floor(Math.random() * 10); i++) {
      const randomCommentsIndex = Math.floor(Math.random() * (commentsArray.length - 1))
      comments.push(commentsArray[randomCommentsIndex])
    }

    const picture = {
      src: `../static/img/photos/${i}.jpg`,
      likes: Math.floor(Math.random() * 200),
      effect: "none",
      description: descriptionArray[randomDescriptionIndex],
      comments: comments,
      commentsNumber: comments.length,
    }
    photos.push(picture)
  }

  return photos
}

function drawPictures(pictures) {
  const pictureTemplate = document.querySelector("#picture-template")
  const pictureExample = pictureTemplate.content.querySelector(".picture-example")
  const pictureContainer = document.querySelector(".pictures-container")

  for (let i = 0; i < pictures.length; i++) {
    let photoCopy = pictureExample.cloneNode(true)
    photoCopy.querySelector(".picture-img").src = pictures[i].src
    photoCopy.querySelector(".picture-img").filter = pictures[i].filter
    photoCopy.querySelector(".picture-comment-span").innerText = pictures[i].commentsNumber
    photoCopy.querySelector(".picture-like-span").innerText = pictures[i].likes
    pictureContainer.append(photoCopy)
  }
}

// const picturesArray = createPictures(25)
// drawPictures(picturesArray)

function showPicture(picture) {
  const openedPictureContainer = document.querySelector(".opened-picture-background")
  openedPictureContainer.classList.remove("hidden")
  document.body.style.overflowY = "hidden"
  const openedPictureImg = document.querySelector(".opened-picture-img")
  openedPictureImg.src = picture.src
  openedPictureImg.style.filter = picture.effect
  openedPictureContainer.querySelector(".description-text").innerText = picture.description
  openedPictureContainer.querySelector(".picture-comments").innerText = picture.commentsNumber
  openedPictureContainer.querySelector(".picture-start").innerText = picture.likes
  const commentTemplate = document.querySelector("#picture-comment").content.querySelector(".comment-block")
  const commentsContainer = document.querySelector(".picture-comments-container")
  for (let i = 0; i < picture.comments.length; i++) {
    const commentCopy = commentTemplate.cloneNode(true)
    commentCopy.querySelector(".comment-text").innerText = picture.comments[i]
    commentsContainer.append(commentCopy)
  }
}

const picturesContainer = document.querySelector(".pictures-container")
picturesContainer.addEventListener("click", function (event) {
  const clickedElement = event.target
  if (clickedElement.classList.contains("picture-img")) {
    for (let i = 0; i < picturesArray.length; i++) {
      if (picturesArray[i].src === clickedElement.getAttribute("src")) {
        showPicture(picturesArray[i])
        break
      }
    }
  }
})

const closeButton = document.querySelector(".close-button")
closeButton.addEventListener("click", function () {
  const openedPictureContainer = document.querySelector(".opened-picture-background")
  openedPictureContainer.classList.add("hidden")
  document.body.style.overflowY = "auto"
})

const inputFile = document.querySelector("#input-file")
inputFile.addEventListener("change", function () {
  const file = inputFile.files[0]

  if (file.type.includes("image")) {
    const reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function () {
      const uploadImage = document.querySelector(".upload-image")
      uploadImage.src = reader.result

      const uploadEffectPreview = document.querySelectorAll(".upload-effect-preview")
      for (let i = 0; i < uploadEffectPreview.length; i++) {
        uploadEffectPreview[i].style.backgroundImage = `url(${reader.result})`
      }

      const uploadImageOverlay = document.querySelector(".upload-image-overlay")
      uploadImageOverlay.classList.remove("hidden")
      document.body.style.overflowY = "hidden"
    }
  } else {
    alert("Виберіть правильний тип файлу")
  }
})

const cancelUpload = document.querySelector("#cancel-upload")
cancelUpload.addEventListener("click", () => {
  const uploadImageOverlay = document.querySelector(".upload-image-overlay")
  uploadImageOverlay.classList.add("hidden")
  document.body.style.overflowY = "auto"
})

/* effects */
const uploadEffectFiledset = document.querySelector(".upload-effect-filedset")

uploadEffectFiledset.addEventListener("click", (event) => {
  const prevActive = document.querySelector(".input-active")
  if (prevActive) {
    prevActive.classList.remove("input-active")
  }
  const label = document.querySelector(`[for="${event.target.id}"]`)
  if (label) {
    label.classList.add("input-active")
  }
  setEffectLevel(event.target.id)
})

/* dnd */
const line = document.querySelector(".effect-level-line")
const pin = document.querySelector(".effect-level-pin")
const effectInputRange = document.querySelector("#effect-input-range")
const effectLevelProgressLine = document.querySelector(".effect-level-progress-line")
const uploadImage = document.querySelector(".upload-image")
const effectLevelTooltip = document.querySelector(".effect-level-tooltip")

const resetFilter = (effect) => {
  pin.style.left = 0
  effectLevelProgressLine.style.width = 0
  effectInputRange.value = 0
  if (effect === "none") {
    uploadImage.style.filter = "none"
  } else {
    uploadImage.style.filter = `${effect}(0)`
  }
}

const setEffectLevel = (effect) => {
  resetFilter(effect)
  pin.addEventListener("mousedown", (event) => {
    event.preventDefault()

    const onMouseMove = (event) => {
      if (effect === "none") {
        resetFilter(effect)
      } else {
        let left = event.clientX - line.getBoundingClientRect().left
        if (left < 0) {
          left = 0
        }
        if (left > line.offsetWidth) {
          left = line.offsetWidth
        }
        const rangePersent = Math.floor((left / line.offsetWidth) * 100)
        effectInputRange.value = rangePersent
        uploadImage.style.filter = `${effect}(${rangePersent}%)`
        effectLevelProgressLine.style.width = left + "px"
        pin.style.left = left + "px"
        effectLevelTooltip.classList.remove("hidden")
        effectLevelTooltip.innerText = `${rangePersent}%`
      }
    }

    const onMouseUp = () => {
      document.removeEventListener("mousemove", onMouseMove)
      document.removeEventListener("mouseup", onMouseUp)
      effectLevelTooltip.classList.add("hidden")
      effectLevelTooltip.innerText = "0%"
    }

    document.addEventListener("mousemove", onMouseMove)
    document.addEventListener("mouseup", onMouseUp)
  })
}

/* Валідація */
function changeSubmitButtonStatus(active) {
  const submitButton = document.querySelector("#submit-upload")
  if (active) {
    submitButton.classList.add("active")
    submitButton.disabled = false
  } else {
    submitButton.classList.remove("active")
    submitButton.disabled = true
  }
}

const formErrorMessage = document.querySelector(".form-error-message")
const uploadFormHachTag = document.querySelector(".upload-form-hach-tag")
uploadFormHachTag.addEventListener("change", () => {
  if (uploadFormHachTag.value.includes("#")) {
    const tagsArray = uploadFormHachTag.value.split("#")

    for (let i = 0; i < tagsArray.length; i++) {
      if (tagsArray[i].includes(" ")) {
        formErrorMessage.innerText = "Тег не повинен містити пробілів"
        changeSubmitButtonStatus(false)
        return
      }
    }

    for (let i = 0; i < tagsArray.length; i++) {
      if (tagsArray[i].length > 20) {
        formErrorMessage.innerText = "Тег не може бути більше 20 символів"
        changeSubmitButtonStatus(false)
        return
      }
    }

    formErrorMessage.innerText = ""
    changeSubmitButtonStatus(true)
  } else if (uploadFormHachTag.value === "") {
    formErrorMessage.innerText = ""
    changeSubmitButtonStatus(true)
  } else {
    formErrorMessage.innerText = "Кожен тег повинен містити символ #"
    changeSubmitButtonStatus(false)
  }
})

function getData() {
  const xhr = new XMLHttpRequest()
  xhr.open("GET", "/api/get/data")
  xhr.send()
  xhr.responseType = "json"
  xhr.onload = function () {
    const data = xhr.response
    console.log(data[0].user)
  }
}

function getAllPhotos() {
  const xhr = new XMLHttpRequest()
  xhr.open("GET", "/api/get/photos/all")
  xhr.send()
  xhr.responseType = "json"
  xhr.onload = function () {
    const data = xhr.response
    drawPictures(data)
  }
}

getData()
getAllPhotos()
