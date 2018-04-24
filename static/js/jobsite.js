$(document).ready(function() {
    
    // bulma menu toggle
    var nav_burger = $('.navbar-burger')
    var nav_menu = $('.navbar-menu')
    nav_burger.click(function() {
        nav_burger.toggleClass('is-active')
        nav_menu.toggleClass('is-active')
    })
    
})