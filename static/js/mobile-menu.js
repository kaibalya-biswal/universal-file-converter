// Mobile Menu Toggle
(function() {
    'use strict';
    
    // Create mobile menu button
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;
    
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    // Create mobile menu button
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.setAttribute('aria-label', 'Toggle menu');
    mobileMenuBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    `;
    
    // Add close icon (hidden initially)
    const closeIcon = document.createElement('svg');
    closeIcon.style.display = 'none';
    closeIcon.setAttribute('width', '24');
    closeIcon.setAttribute('height', '24');
    closeIcon.setAttribute('viewBox', '0 0 24 24');
    closeIcon.setAttribute('fill', 'none');
    closeIcon.setAttribute('stroke', 'currentColor');
    closeIcon.setAttribute('stroke-width', '2');
    closeIcon.innerHTML = `
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
    `;
    mobileMenuBtn.appendChild(closeIcon);
    
    // Insert before nav-actions
    const navActions = document.querySelector('.nav-actions');
    if (navActions) {
        navContainer.insertBefore(mobileMenuBtn, navActions);
    }
    
    // Toggle menu
    mobileMenuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('mobile-open');
        mobileMenuBtn.classList.toggle('active');
        
        // Toggle icons
        const menuIcon = mobileMenuBtn.querySelector('svg:first-child');
        if (menuIcon) {
            menuIcon.style.display = navLinks.classList.contains('mobile-open') ? 'none' : 'block';
        }
        closeIcon.style.display = navLinks.classList.contains('mobile-open') ? 'block' : 'none';
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
            navLinks.classList.remove('mobile-open');
            mobileMenuBtn.classList.remove('active');
            const menuIcon = mobileMenuBtn.querySelector('svg:first-child');
            if (menuIcon) {
                menuIcon.style.display = 'block';
            }
            closeIcon.style.display = 'none';
        }
    });
    
    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('mobile-open');
            mobileMenuBtn.classList.remove('active');
            const menuIcon = mobileMenuBtn.querySelector('svg:first-child');
            if (menuIcon) {
                menuIcon.style.display = 'block';
            }
            closeIcon.style.display = 'none';
        });
    });
})();
