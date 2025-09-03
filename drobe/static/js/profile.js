const sidebar_links = document.querySelector(".sidebar")
const links = sidebar_links.querySelectorAll("#link")
const main_content = document.querySelector(".main--content")
const content = main_content.querySelectorAll(".content-section")

function handleclicks(e) {
    var id = -1
    for (let i = 0; i < links.length; i++) {
        links[i].classList.remove("active")
        content[i].classList.add("hidden")
        if (links[i].classList[0]=== this.classList[0]){
            id = i
        }
    }
    console.log(this.classList[0])
    console.log(`id is ${id}`)
    if (id !== -1) {
        content[id].classList.remove("hidden")
    }
    this.classList.add("active")
}

links.forEach(link => link.addEventListener("click", handleclicks))
