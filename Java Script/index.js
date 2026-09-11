/* ==========================================================================
   Krishna Utsav 2026 - Main JS Code (Simplified Landing Page)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initAmbientAudio();
    initMobileNavigation();
    initScrollEffects();
    initTwinCarousels();
    initBouncingFeathers();
    initKrishnaDarshanSlider();
});

/* ==========================================================================
   1. Ambient Audio Autoplay Logic
   ========================================================================== */
function initAmbientAudio() {
    const music = document.getElementById("bgMusic");
    if (!music) return;

    // Browser policy requires user gesture to start audio.
    // We register a one-time gesture listener on first interaction.
    function playAudioOnGesture() {
        music.play()
            .then(() => {
                console.log("Ambient devotional music is now playing.");
            })
            .catch(e => {
                console.log("Audio playback notice:", e);
            });

        document.removeEventListener("click", playAudioOnGesture);
        document.removeEventListener("touchstart", playAudioOnGesture);
    }

    document.addEventListener("click", playAudioOnGesture);
    document.addEventListener("touchstart", playAudioOnGesture);
}

/* ==========================================================================
   2. Mobile Navigation Menu Toggle
   ========================================================================== */
function initMobileNavigation() {
    const menuBtn = document.querySelector(".menu-btn");
    const navLinks = document.querySelector(".nav-links");
    const links = document.querySelectorAll(".nav-links a");

    if (!menuBtn || !navLinks) return;

    menuBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        navLinks.classList.toggle("active");

        // Toggle menu icon between bars and close X
        const icon = menuBtn.querySelector("i");
        if (navLinks.classList.contains("active")) {
            icon.className = "fa-solid fa-xmark";
        } else {
            icon.className = "fa-solid fa-bars";
        }
    });

    // Close menu when clicking links
    links.forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("active");
            menuBtn.querySelector("i").className = "fa-solid fa-bars";
        });
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
        if (!navLinks.contains(e.target) && !menuBtn.contains(e.target)) {
            navLinks.classList.remove("active");
            menuBtn.querySelector("i").className = "fa-solid fa-bars";
        }
    });
}

/* ==========================================================================
   3. Scroll Effects (Reveal Animations, Progress Bar, Top Button)
   ========================================================================== */
function initScrollEffects() {
    const scrollProgress = document.getElementById("scrollProgress");
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    const revealElements = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, .reveal-scale");

    function onScroll() {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

        // 1. Reading progress bar
        if (scrollProgress && docHeight > 0) {
            const pct = (scrollTop / docHeight) * 100;
            scrollProgress.style.width = `${pct}%`;
        }

        // 2. Scroll to top button visibility
        if (scrollTopBtn) {
            if (scrollTop > 400) {
                scrollTopBtn.classList.add("visible");
            } else {
                scrollTopBtn.classList.remove("visible");
            }
        }

        // 3. Reveal elements animation
        revealElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const triggerOffset = window.innerHeight * 0.85; // 85% of screen height
            if (rect.top < triggerOffset) {
                el.classList.add("active");
            }
        });
    }

    // Scroll to top execution
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    // Initial check and scroll listener
    window.addEventListener("scroll", onScroll);
    onScroll(); // Fire on load
}

/* ==========================================================================
   4. Reusable Carousel/Slider Component
   ========================================================================== */
function initTwinCarousels() {
    // 1. Initialize Events Carousel
    initCarousel(
        "#eventsCarousel",
        "#eventContainer",
        ".event-card"
    );

    // 2. Initialize Timeline / Schedule Carousel
    initCarousel(
        "#timelineCarousel",
        "#timelineContainer",
        ".timeline-item"
    );

    // 3. Initialize Gallery Carousel
    initCarousel(
        "#galleryCarousel",
        "#galleryContainer",
        ".gallery-card"
    );
}

function initCarousel(containerSelector, trackSelector, cardSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const track = container.querySelector(trackSelector);
    const prevBtn = container.querySelector(".carousel-ctrl-btn.prev");
    const nextBtn = container.querySelector(".carousel-ctrl-btn.next");
    const cards = container.querySelectorAll(cardSelector);

    if (!track || !prevBtn || !nextBtn || cards.length === 0) return;

    let currentIndex = 0;

    function getVisibleCount() {
        const width = window.innerWidth;
        if (width <= 768) return 1;
        if (width <= 992) return 2;
        return 3;
    }

    function updateSlider() {
        const visibleCount = getVisibleCount();
        const totalCards = cards.length;
        const maxIndex = Math.max(0, totalCards - visibleCount);

        // Clamp index
        if (currentIndex > maxIndex) {
            currentIndex = maxIndex;
        }

        const cardWidth = cards[0].offsetWidth;
        const gap = parseFloat(getComputedStyle(track).gap) || 0;

        // Calculate transition translate offset
        const moveAmount = currentIndex * (cardWidth + gap);
        track.style.transform = `translateX(-${moveAmount}px)`;

        // Update button states
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= maxIndex;
    }

    nextBtn.addEventListener("click", () => {
        const visibleCount = getVisibleCount();
        const maxIndex = cards.length - visibleCount;
        if (currentIndex < maxIndex) {
            currentIndex++;
            updateSlider();
        }
    });

    prevBtn.addEventListener("click", () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlider();
        }
    });

    // Support touch swipe gestures on mobile
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    track.addEventListener("touchend", (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diffX = touchStartX - touchEndX;
        if (Math.abs(diffX) > 40) {
            if (diffX > 0) {
                // Swiped left -> Next
                const visibleCount = getVisibleCount();
                const maxIndex = cards.length - visibleCount;
                if (currentIndex < maxIndex) {
                    currentIndex++;
                    updateSlider();
                }
            } else {
                // Swiped right -> Prev
                if (currentIndex > 0) {
                    currentIndex--;
                    updateSlider();
                }
            }
        }
    }, { passive: true });

    // Support window resizing and dynamic adjustments
    window.addEventListener("resize", updateSlider);

    // Initial draw
    setTimeout(updateSlider, 150); // Small timeout to ensure styles and offsets are loaded
}

/* ==========================================================================
   5. Bouncing Peacock Feathers (Screensaver Style Animation)
   ========================================================================== */
function initBouncingFeathers() {
    const feather1 = document.querySelector(".bg-peacock-feather-1");
    const feather2 = document.querySelector(".bg-peacock-feather-2");

    if (!feather1 && !feather2) return;

    function setupBounce(element, speedX, speedY, startX, startY, rotSpeed = 0.08) {
        let posX = startX;
        let posY = startY;
        let dx = speedX;
        let dy = speedY;
        let rot = 0;

        function step() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            const rect = element.getBoundingClientRect();

            posX += dx;
            posY += dy;
            rot += rotSpeed;

            // Responsive boundary clamp if viewport resized
            if (rect.width > 0 && posX + rect.width >= width) {
                posX = Math.max(0, width - rect.width);
                dx = -Math.abs(dx);
            } else if (posX <= 0) {
                posX = 0;
                dx = Math.abs(dx);
            }

            if (rect.height > 0 && posY + rect.height >= height) {
                posY = Math.max(0, height - rect.height);
                dy = -Math.abs(dy);
            } else if (posY <= 0) {
                posY = 0;
                dy = Math.abs(dy);
            }

            element.style.left = `${posX}px`;
            element.style.top = `${posY}px`;
            element.style.transform = `rotate(${rot}deg)`;

            requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    if (feather1) {
        setupBounce(feather1, 0.5, 0.4, 50, 100, 0.08);
    }
    if (feather2) {
        setupBounce(feather2, -0.4, 0.5, Math.max(10, window.innerWidth - 260), Math.max(10, window.innerHeight - 260), -0.06);
    }
}

/* ==========================================================================
   6. Continuous Krishna Darshan Slider (3s Auto-advance with Seamless Loop)
   ========================================================================== */
function initKrishnaDarshanSlider() {
    const container = document.getElementById("krishnaSliderContainer");
    const track = document.getElementById("krishnaSliderTrack");
    const timerBar = document.getElementById("krishnaTimerBar");
    const counter = document.getElementById("darshanCounter");
    const dotsContainer = document.getElementById("krishnaDots");
    const prevBtn = document.getElementById("krishnaPrev");
    const nextBtn = document.getElementById("krishnaNext");

    if (!container || !track) return;

    const originalCount = 11; // 11 distinct Krishna images
    const slideDuration = 3000; // 3 seconds per image
    const transitionMs = 700; // 0.7s transition duration

    let currentIndex = 0;
    let progressStartTime = null;
    let animFrameId = null;
    let isPaused = false;
    let isTransitioning = false;

    // Generate pagination dots
    if (dotsContainer) {
        dotsContainer.innerHTML = "";
        for (let i = 0; i < originalCount; i++) {
            const dot = document.createElement("button");
            dot.className = "krishna-dot" + (i === 0 ? " active" : "");
            dot.setAttribute("aria-label", `Go to Krishna Darshan ${i + 1}`);
            dot.addEventListener("click", () => {
                if (isTransitioning) return;
                goToSlide(i);
            });
            dotsContainer.appendChild(dot);
        }
    }

    function updateIndicators(displayIdx) {
        if (counter) {
            counter.textContent = `${displayIdx + 1} / ${originalCount}`;
        }
        if (dotsContainer) {
            const dots = dotsContainer.querySelectorAll(".krishna-dot");
            dots.forEach((d, idx) => {
                d.classList.toggle("active", idx === displayIdx);
            });
        }
    }

    function renderSlide(animate = true) {
        if (animate) {
            track.style.transition = `transform ${transitionMs}ms cubic-bezier(0.4, 0, 0.2, 1)`;
        } else {
            track.style.transition = "none";
        }
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        const displayIdx = currentIndex >= originalCount ? 0 : currentIndex;
        updateIndicators(displayIdx);
    }

    function nextSlide() {
        if (isTransitioning) return;
        isTransitioning = true;
        currentIndex++;
        renderSlide(true);
    }

    function prevSlide() {
        if (isTransitioning) return;
        isTransitioning = true;
        if (currentIndex === 0) {
            // Jump instantly to the cloned end, then animate to last slide
            currentIndex = originalCount;
            renderSlide(false);
            track.offsetHeight; // force reflow
            currentIndex = originalCount - 1;
            renderSlide(true);
        } else {
            currentIndex--;
            renderSlide(true);
        }
    }

    function goToSlide(targetIdx) {
        currentIndex = targetIdx;
        renderSlide(true);
        resetTimer();
    }

    // Seamless loop reset when sliding past 11th image to clone
    track.addEventListener("transitionend", () => {
        isTransitioning = false;
        if (currentIndex >= originalCount) {
            // Silently snap back to the first slide without animation
            currentIndex = 0;
            renderSlide(false);
        }
    });

    // 3-second Progress bar animation & automatic progression
    function startProgress() {
        if (animFrameId) cancelAnimationFrame(animFrameId);
        progressStartTime = performance.now();

        function frame(now) {
            if (isPaused) {
                animFrameId = requestAnimationFrame(frame);
                return;
            }
            const elapsed = now - progressStartTime;
            const pct = Math.min(100, (elapsed / slideDuration) * 100);
            if (timerBar) {
                timerBar.style.width = `${pct}%`;
            }

            if (elapsed < slideDuration) {
                animFrameId = requestAnimationFrame(frame);
            } else {
                if (timerBar) timerBar.style.width = "0%";
                nextSlide();
                startProgress();
            }
        }

        animFrameId = requestAnimationFrame(frame);
    }

    function resetTimer() {
        if (timerBar) timerBar.style.width = "0%";
        startProgress();
    }

    // Manual navigation buttons
    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            nextSlide();
            resetTimer();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            prevSlide();
            resetTimer();
        });
    }

    // Pause on hover
    container.addEventListener("mouseenter", () => {
        isPaused = true;
    });

    container.addEventListener("mouseleave", () => {
        isPaused = false;
        const currentWidthPct = parseFloat(timerBar ? timerBar.style.width : 0) || 0;
        progressStartTime = performance.now() - (currentWidthPct / 100) * slideDuration;
    });

    // Mobile touch swipe gesture
    let touchStartX = 0;
    container.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].screenX;
        isPaused = true;
    }, { passive: true });

    container.addEventListener("touchend", (e) => {
        const touchEndX = e.changedTouches[0].screenX;
        const diffX = touchStartX - touchEndX;
        isPaused = false;
        resetTimer();
        if (Math.abs(diffX) > 40) {
            if (diffX > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }, { passive: true });

    // Initial render
    renderSlide(false);
    startProgress();
}

