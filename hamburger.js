function hamburger_visible(hamburgerMenu, main_content, should_show) {
    // also, add a dark effect to the main div
    hamburgerMenu.classList.toggle('-translate-x-full', !should_show)
    main_content.classList.toggle('opacity-50', should_show)
}

document.addEventListener('DOMContentLoaded', () => {
    const hamburgerButton = document.getElementById('hamburgerButton')
    const hamburgerMenu = document.getElementById('hamburgerMenu')
    const main_content = document.getElementById("mainContent")

    document.addEventListener('click', event => {
        if (event.target == hamburgerButton) {
            // const isMenuOpen = !hamburgerMenu.classList.contains('-translate-x-full')
            // const should_show = !isMenuOpen
            hamburger_visible(hamburgerMenu, main_content, true)
            return
        }

        if (hamburgerMenu.contains(event.target)) {
            // if we click inside the hamburgermenu, no action is taken
            return
        }

        hamburger_visible(hamburgerMenu, main_content, false)
    })
})