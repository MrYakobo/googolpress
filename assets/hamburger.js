
let hamburgerButton
let hamburgerMenu
let mainContentWrapper
let mainContent
let overlay
let header

function hamburger_visible(should_show) {
    // also, add a dark effect to the main div
    hamburgerMenu.classList.toggle('-translate-x-full', !should_show)
    overlay.classList.toggle('hidden', !should_show)
}

document.addEventListener('DOMContentLoaded', () => {
    hamburgerButton = document.getElementById('hamburgerButton')
    hamburgerMenu = document.getElementById('hamburgerMenu')
    mainContentWrapper = document.getElementById("mainContentWrapper")
    mainContent = document.getElementById("mainContent")
    header = document.getElementById("header")
    overlay = document.getElementById("overlay")

    let startX = 0

    document.addEventListener("touchstart", (event) => {
        startX = event.touches[0].clientX
    })

    document.addEventListener("touchmove", (event) => {
        const endX = event.touches[0].clientX
        let movement_threshold = 100
        if (startX - endX > movement_threshold) { // Detect a left swipe
            hamburger_visible(false)
        }
    })

    mainContentWrapper.addEventListener('scroll', highlightActiveNav, { passive: true })

    document.addEventListener('click', event => {
        if (event.target == hamburgerButton) {
            // const isMenuOpen = !hamburgerMenu.classList.contains('-translate-x-full')
            // const should_show = !isMenuOpen
            hamburger_visible(true)
            return
        }

        if (hamburgerMenu.contains(event.target)) {
            // if we click inside the hamburgermenu, no action is taken
            return
        }

        hamburger_visible(false)
    })
})

function highlightActiveNav() {
    const sections = document.querySelectorAll('.title')
    const navLinks = document.querySelectorAll('nav #headings a')
    const main_content = document.querySelector("#mainContentWrapper")
    const curr_scroll = main_content.scrollTop

    // if the heading is within 100 pixels, set it as active
    const margin = 100

    let currentSection = null

    for (let i = sections.length - 1; i >= 0; i--) {
        const top = sections[i].offsetTop
        if (top <= curr_scroll + margin) {
            currentSection = i
            break
        }
    }

    // Remove the 'active' class from all nav items
    navLinks.forEach(link => {
        link.classList.remove('active')
    })

    // focus on body, so no link is focused
    document.body.focus()

    // Add the 'active' class to the corresponding nav item
    if (currentSection !== null) {
        navLinks[currentSection].classList.add('active')
        // focus the correct link
        navLinks[currentSection].scrollIntoView({ behavior: "smooth" })
    }
}