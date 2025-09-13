// Sidebar Navigation JavaScript
const body = document.querySelector("body");
const sidebar = document.querySelector(".sidebar");
const sidebarBtn = document.querySelector("#sidebar_btn");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");
const darkLight = document.querySelector("#darkLight");

// Only proceed if sidebar exists (dashboard pages only)
if (!sidebar) {
  console.log("Sidebar not found, skipping sidebar initialization");
} else {
  // Sidebar toggle functionality - handle both top navbar and sidebar button
  function toggleSidebar() {
    if (window.innerWidth > 768) {
      // Desktop: toggle compressed state
      sidebar.classList.toggle("compressed");
    } else {
      // Mobile: toggle open/close
      sidebar.classList.toggle("open");
    }
  }

  // Top navbar hamburger menu toggle
  if (sidebarOpen) {
    sidebarOpen.addEventListener("click", (e) => {
      e.preventDefault();
      toggleSidebar();
    });
  }

  // Sidebar button toggle (inside sidebar)
  if (sidebarBtn) {
    sidebarBtn.addEventListener("click", (e) => {
      e.preventDefault();
      toggleSidebar();
    });
  }

  // Close sidebar on mobile when clicking outside
  document.addEventListener("click", (e) => {
    if (window.innerWidth <= 768) {
      if (!sidebar.contains(e.target) && !sidebarOpen.contains(e.target)) {
        sidebar.classList.remove("open");
      }
    }
  });

  // Dark/Light theme toggle
  if (darkLight) {
    darkLight.addEventListener("click", () => {
      body.classList.toggle("dark");
      if (body.classList.contains("dark")) {
        darkLight.classList.replace("bx-sun", "bx-moon");
      } else {
        darkLight.classList.replace("bx-moon", "bx-sun");
      }
    });
  }

  // Submenu functionality
  function initSubmenuHandlers() {
    const submenuItems = document.querySelectorAll(".submenu_item");
    submenuItems.forEach((item, index) => {
      // Remove existing event listeners
      item.removeEventListener("click", handleSubmenuClick);
      // Add new event listener
      item.addEventListener("click", handleSubmenuClick);
    });
  }

  function handleSubmenuClick(e) {
    e.preventDefault();
    const parentLi = this.closest('li');
    
    if (sidebar.classList.contains("compressed")) {
      // In compressed mode, expand sidebar and show submenu
      sidebar.classList.remove("compressed");
      
      // Small delay to ensure sidebar expansion animation completes
      setTimeout(() => {
        parentLi.classList.add("showMenu");
        
        // Close other submenus
        const submenuItems = document.querySelectorAll(".submenu_item");
        submenuItems.forEach((item) => {
          if (item !== this) {
            item.closest('li').classList.remove("showMenu");
          }
        });
      }, 300); // Wait for sidebar expansion animation
    } else {
      // In expanded mode, toggle the submenu
      parentLi.classList.toggle("showMenu");
      
      // Close other submenus
      const submenuItems = document.querySelectorAll(".submenu_item");
      submenuItems.forEach((item) => {
        if (item !== this) {
          item.closest('li').classList.remove("showMenu");
        }
      });
    }
  }

  // Initialize submenu handlers
  initSubmenuHandlers();

  // Hover functionality for compressed sidebar - only on desktop
  sidebar.addEventListener("mouseenter", () => {
    if (window.innerWidth > 768 && sidebar.classList.contains("compressed")) {
      // Show tooltips or expand temporarily on hover
      const menuItems = document.querySelectorAll(".nav_list li a");
      menuItems.forEach(item => {
        const linkName = item.querySelector(".link_name");
        if (linkName) {
          item.setAttribute("title", linkName.textContent);
        }
      });
    }
  });

  sidebar.addEventListener("mouseleave", () => {
    if (window.innerWidth > 768 && sidebar.classList.contains("compressed")) {
      // Remove tooltips when leaving
      const menuItems = document.querySelectorAll(".nav_list li a");
      menuItems.forEach(item => {
        item.removeAttribute("title");
      });
    }
  });

  // Responsive behavior - keep expanded on desktop by default
  function handleResize() {
    if (window.innerWidth <= 768) {
      // Mobile behavior
      sidebar.classList.remove("compressed");
      sidebar.classList.remove("open");
    } else {
      // Desktop behavior - keep expanded by default
      sidebar.classList.remove("open");
      // Don't automatically compress on desktop
    }
  }

  // Initialize responsive behavior
  handleResize();

  // Listen for window resize
  window.addEventListener("resize", handleResize);

  // Active menu item highlighting
  function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll(".nav_list li a");
    
    menuItems.forEach(item => {
      const href = item.getAttribute("href");
      if (href && (currentPath === href || currentPath === href.replace(/\/$/, '') || currentPath === href + '/')) {
        item.classList.add("active");
        // Also activate parent menu if it's a submenu
        const parentLi = item.closest("li");
        if (parentLi) {
          parentLi.classList.add("active");
        }
      } else {
        item.classList.remove("active");
      }
    });
  }

  // Set active menu item on page load
  document.addEventListener("DOMContentLoaded", setActiveMenuItem);

  // Search functionality
  const searchInput = document.querySelector(".search_bar input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase();
      const menuItems = document.querySelectorAll(".nav_list li a");
      
      menuItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        const listItem = item.closest("li");
        
        if (text.includes(searchTerm)) {
          listItem.style.display = "block";
        } else {
          listItem.style.display = "none";
        }
      });
    });
  }

  // Keyboard shortcuts
  document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + B to toggle sidebar - only on desktop
    if ((e.ctrlKey || e.metaKey) && e.key === "b" && window.innerWidth > 768) {
      e.preventDefault();
      toggleSidebar();
    }
    
    // Escape to close mobile sidebar
    if (e.key === "Escape" && window.innerWidth <= 768) {
      sidebar.classList.remove("open");
    }
  });

  // Smooth scrolling for sidebar
  const sidebarNav = document.querySelector(".nav_list");
  if (sidebarNav) {
    sidebarNav.style.scrollBehavior = "smooth";
  }

  // Initialize tooltips for compressed sidebar - only on desktop
  function initTooltips() {
    if (window.innerWidth > 768 && sidebar.classList.contains("compressed")) {
      const menuItems = document.querySelectorAll(".nav_list li a");
      menuItems.forEach(item => {
        const linkName = item.querySelector(".link_name");
        if (linkName) {
          item.setAttribute("title", linkName.textContent);
        }
      });
    }
  }

  // Initialize tooltips on page load
  document.addEventListener("DOMContentLoaded", initTooltips);

  // Update tooltips when sidebar state changes
  const observer = new MutationObserver(() => {
    initTooltips();
  });

  observer.observe(sidebar, {
    attributes: true,
    attributeFilter: ["class"]
  });

  // Export functions for use in other scripts
  window.Sidebar = {
    toggle: toggleSidebar,
    expand: () => {
      if (window.innerWidth > 768) {
        sidebar.classList.remove("compressed");
      } else {
        sidebar.classList.remove("open");
      }
    },
    compress: () => {
      if (window.innerWidth > 768) {
        sidebar.classList.add("compressed");
      } else {
        sidebar.classList.add("open");
      }
    },
    setActive: setActiveMenuItem,
    initTooltips: initTooltips,
    initSubmenuHandlers: initSubmenuHandlers
  };
} // Close the if (!sidebar) else block 