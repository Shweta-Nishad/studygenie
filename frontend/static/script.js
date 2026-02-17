// ===============================
// STUDYGENIE MAIN JAVASCRIPT FILE
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    // ====================================
    // 1️⃣ Smooth Scroll for Anchor Links
    // ====================================
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");

            if (targetId.length > 1) {
                e.preventDefault();
                const targetSection = document.querySelector(targetId);

                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: "smooth"
                    });
                }
            }
        });
    });


    // ====================================
    // 2️⃣ Fade-in Animation on Scroll
    // ====================================
    const fadeElements = document.querySelectorAll(".fade-in");

    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        }, { threshold: 0.2 });

        fadeElements.forEach(el => observer.observe(el));
    }


    // ====================================
    // 3️⃣ Navbar Background Change on Scroll
    // ====================================
    const navbar = document.querySelector(".navbar");

    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 50) {
                navbar.style.background = "rgba(0, 0, 0, 0.8)";
                navbar.style.backdropFilter = "blur(10px)";
            } else {
                navbar.style.background = "transparent";
                navbar.style.backdropFilter = "none";
            }
        });
    }


    // ====================================
    // 4️⃣ Profile Dropdown (FIXED CLEAN VERSION)
    // ====================================

    const profileContainer = document.querySelector(".profile-container");
    const profileDropdown = document.getElementById("profileDropdown");

    if (profileContainer && profileDropdown) {

        // Toggle dropdown when clicking profile button
        profileContainer.addEventListener("click", function (e) {
            e.stopPropagation();

            if (profileDropdown.style.display === "block") {
                profileDropdown.style.display = "none";
            } else {
                profileDropdown.style.display = "block";
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function () {
            profileDropdown.style.display = "none";
        });
    }

});
