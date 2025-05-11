const accordionHead = document.querySelectorAll(".accordion-head")

console.log(accordionHead)

accordionHead.forEach((element) => {
  element.addEventListener("click", (event) => {
    const isClassNameExist = event.target.classList.contains("expanded")
    if (isClassNameExist) {
      event.target.classList.remove("expanded")
    } else {
      event.target.classList.add("expanded")
    }
  })
})
