
let tooltip

let hamburgerButton
let hamburgerMenu
let main_content
let header

function tooltip_leave(event) {

    function hide() {
        tooltip.remove()
        tooltip = null
    }

    if (event == null) {
        if (tooltip != null)
            hide()
        return
    }

    const target = event.target.closest('a')
    target.setAttribute('title', target.dataset.originalTitle)
    target.removeAttribute('data-original-title')

    // Remove tooltip on mouseout
    if (tooltip && target && target.dataset.originalTitle) {
        hide()
    }
}


function hamburger_visible(should_show) {
    // also, add a dark effect to the main div
    hamburgerMenu.classList.toggle('-translate-x-full', !should_show)
    main_content.classList.toggle('modal-content-bg', should_show)
    header.classList.toggle('modal-content-bg', should_show)
    tooltip_leave(null)
}

document.addEventListener('DOMContentLoaded', () => {
    hamburgerButton = document.getElementById('hamburgerButton')
    hamburgerMenu = document.getElementById('hamburgerMenu')
    main_content = document.getElementById("mainContent")
    header = document.getElementById("header")

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

    main_content.addEventListener('scroll', highlightActiveNav, { passive: true })

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
        tooltip_leave(event)
    })

    document.addEventListener('mouseover', (event) => {
        const target = event.target.closest('a')

        // Check if the hovered element has a title attribute
        if (target && target.hasAttribute('title')) {
            const titleText = target.getAttribute('title')

            // Create tooltip element
            tooltip = document.createElement('div')
            tooltip.className = 'tooltip'
            tooltip.textContent = titleText

            // Append tooltip to body
            document.body.appendChild(tooltip)

            // Remove the title attribute to prevent default browser tooltips
            target.dataset.originalTitle = titleText
            target.removeAttribute('title')

            // Position the tooltip
            const updateTooltipPosition = (e) => {
                if (tooltip == null)
                    return

                const tooltipWidth = tooltip.offsetWidth
                const tooltipHeight = tooltip.offsetHeight
                const pageX = e.pageX
                const pageY = e.pageY

                tooltip.style.left = `${pageX - tooltipWidth / 2}px`
                tooltip.style.top = `${pageY - tooltipHeight - 10}px`
                tooltip.style.opacity = '1'
            }

            updateTooltipPosition(event)

            // Update position on mousemove
            target.addEventListener('mousemove', updateTooltipPosition)
        }
    })

    document.addEventListener('mouseout', (event) => {
        // tooltip_leave()
    })

})

function highlightActiveNav() {
    const sections = document.querySelectorAll('.title')
    const navLinks = document.querySelectorAll('nav #headings a')
    const main_content = document.querySelector("#mainContent")
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
        navLinks[currentSection].focus()
    }
}