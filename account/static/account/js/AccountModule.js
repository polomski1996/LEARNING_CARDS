/**
 * AccountModule - Handles all account-related UI interactions
 * This module manages navigation, dropdowns, messages, and responsive behavior
 */
export class AccountModule {
  constructor() {
    // DOM element references
    this.elements = {
      mobileMenuToggle: null,
      mainNav: null,
      dropdownTriggers: [],
      messageCloseButtons: [],
      messagesList: null,
    }

    // State management
    this.state = {
      isMobileMenuOpen: false,
      activeDropdown: null,
    }

    // Configuration
    this.config = {
      messageAutoCloseDelay: 5000,
      transitionDuration: 250,
      breakpointMobile: 768,
    }
  }

  /**
   * Initialize the module
   * Sets up all event listeners and initial state
   */
  init() {
    this.cacheElements()
    this.attachEventListeners()
    this.setupMessages()
    this.handleResize()
  }

  /**
   * Cache DOM elements for performance
   */
  cacheElements() {
    this.elements.mobileMenuToggle = document.getElementById("mobileMenuToggle")
    this.elements.mainNav = document.getElementById("mainNav")
    this.elements.dropdownTriggers = document.querySelectorAll(".dropdown-trigger")
    this.elements.messageCloseButtons = document.querySelectorAll(".message-close")
    this.elements.messagesList = document.getElementById("messagesList")
  }

  /**
   * Attach all event listeners
   */
  attachEventListeners() {
    // Mobile menu toggle
    if (this.elements.mobileMenuToggle && this.elements.mainNav) {
      this.elements.mobileMenuToggle.addEventListener("click", () => this.toggleMobileMenu())
    }

    // Dropdown menus
    this.elements.dropdownTriggers.forEach((trigger) => {
      trigger.addEventListener("click", (e) => this.handleDropdownClick(e, trigger))
    })

    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => this.handleDocumentClick(e))

    // Message close buttons
    this.elements.messageCloseButtons.forEach((button) => {
      button.addEventListener("click", (e) => this.closeMessage(e.target.closest(".message")))
    })

    // Handle window resize
    window.addEventListener("resize", () => this.handleResize())

    // Handle escape key
    document.addEventListener("keydown", (e) => this.handleEscapeKey(e))
  }

  /**
   * Toggle mobile menu open/closed
   */
  toggleMobileMenu() {
    this.state.isMobileMenuOpen = !this.state.isMobileMenuOpen

    if (this.elements.mobileMenuToggle) {
      this.elements.mobileMenuToggle.classList.toggle("active", this.state.isMobileMenuOpen)
    }

    if (this.elements.mainNav) {
      this.elements.mainNav.classList.toggle("active", this.state.isMobileMenuOpen)
    }

    // Prevent body scroll when menu is open
    document.body.style.overflow = this.state.isMobileMenuOpen ? "hidden" : ""
  }
  
  /**
   * Handle dropdown menu clicks
   */
  handleDropdownClick(event, trigger) {
    event.stopPropagation()

    const dropdownId = trigger.getAttribute("data-dropdown")
    const dropdown = document.getElementById(dropdownId)
    const menuItem = trigger.closest(".menu-item")

    if (!dropdown) return

    const isCurrentlyActive = dropdown.classList.contains("active")

    // Close all dropdowns first
    this.closeAllDropdowns()

    // Toggle current dropdown
    if (!isCurrentlyActive) {
      dropdown.classList.add("active")
      menuItem?.classList.add("active")
      this.state.activeDropdown = dropdown
    } else {
      this.state.activeDropdown = null
    }
  }

  /**
   * Close all open dropdown menus
   */
  closeAllDropdowns() {
    document.querySelectorAll(".dropdown-menu.active").forEach((dropdown) => {
      console.log('dropdown closed');
      dropdown.classList.remove("active");
    })

    document.querySelectorAll(".menu-item.active").forEach((item) => {
      item.classList.remove("active")
    })

    this.state.activeDropdown = null
  }

  /**
   * Handle clicks outside dropdowns to close them
   */
  handleDocumentClick(event) {
    const isDropdownClick = event.target.closest(".dropdown-trigger") || event.target.closest(".dropdown-menu")

    if (!isDropdownClick) {
      this.closeAllDropdowns()
    }
  }

  /**
   * Handle escape key press
   */
  handleEscapeKey(event) {
    if (event.key === "Escape") {
      this.closeAllDropdowns()

      if (this.state.isMobileMenuOpen) {
        this.toggleMobileMenu()
      }
    }
  }

  /**
   * Setup message behavior (auto-close, animations)
   */
  setupMessages() {
    if (!this.elements.messagesList) return

    const messages = this.elements.messagesList.querySelectorAll(".message")

    messages.forEach((message, index) => {
      // Stagger animation
      message.style.animationDelay = `${index * 100}ms`

      // Auto-close after delay
      setTimeout(
        () => {
          this.closeMessage(message)
        },
        this.config.messageAutoCloseDelay + index * 100,
      )
    })
  }

  /**
   * Close a specific message with animation
   */
  closeMessage(messageElement) {
    if (!messageElement) return

    messageElement.style.opacity = "0"
    messageElement.style.transform = "translateX(20px)"
    messageElement.style.transition = `all ${this.config.transitionDuration}ms ease-out`

    setTimeout(() => {
      messageElement.remove()

      // Remove messages container if empty
      if (this.elements.messagesList && this.elements.messagesList.children.length === 0) {
        this.elements.messagesList.closest(".messages-container")?.remove()
      }
    }, this.config.transitionDuration)
  }

  /**
   * Handle window resize events
   */
  handleResize() {
    const isMobile = window.innerWidth <= this.config.breakpointMobile

    // Close mobile menu if resizing to desktop
    if (!isMobile && this.state.isMobileMenuOpen) {
      this.toggleMobileMenu()
    }

    // Reset dropdowns on mobile
    if (isMobile) {
      // On mobile, dropdowns are always visible in the mobile menu
      document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
        dropdown.classList.remove("active")
      })
    }
  }

  /**
   * Destroy the module (cleanup)
   */
  destroy() {
    // Remove all event listeners
    if (this.elements.mobileMenuToggle) {
      this.elements.mobileMenuToggle.removeEventListener("click", this.toggleMobileMenu)
    }

    this.elements.dropdownTriggers.forEach((trigger) => {
      trigger.removeEventListener("click", this.handleDropdownClick)
    })

    document.removeEventListener("click", this.handleDocumentClick)
    document.removeEventListener("keydown", this.handleEscapeKey)
    window.removeEventListener("resize", this.handleResize)

    // Reset body overflow
    document.body.style.overflow = ""
  }
}
