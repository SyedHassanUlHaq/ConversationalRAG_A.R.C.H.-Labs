// Custom JavaScript for A.R.C.H. Labs Chainlit Support Interface

document.addEventListener('DOMContentLoaded', function() {
    console.log('A.R.C.H. Labs custom interface enhancements loaded');
    

    
    // Fix message dialog height issues
    function fixMessageHeight() {
        const messageContainers = document.querySelectorAll('.message-container');
        messageContainers.forEach(container => {
            // Ensure proper bottom padding
            container.style.paddingBottom = '1rem';
            container.style.marginBottom = '0.75rem';
        });
    }
    
    // Apply initial fixes
    setTimeout(fixMessageHeight, 500);
    
    // Monitor for new messages and apply fixes
    const messageObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // New message added, apply height fixes
                setTimeout(fixMessageHeight, 100);
            }
        });
    });
    
    // Start observing for message changes
    const chatContainer = document.querySelector('.chat-container, .messages-container, [class*="message"]');
    if (chatContainer) {
        messageObserver.observe(chatContainer, {
            childList: true,
            subtree: true
        });
    }
    
    // Professional styling enhancements
    function applyProfessionalStyling() {
        // Add professional class to body
        document.body.classList.add('arch-labs-professional');
        
        // Enhance button interactions
        const buttons = document.querySelectorAll('button, [role="button"]');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-1px)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
    
    // Apply professional styling
    setTimeout(applyProfessionalStyling, 1000);
    
    // Fix any layout issues on resize
    window.addEventListener('resize', function() {
        setTimeout(fixMessageHeight, 200);
    });
    
    // Console branding
    console.log(`
    ╔═══════════════════════════════════════╗
    ║         A.R.C.H. Labs Support         ║
    ║    Professional Software Development  ║
    ║         Custom AI Solutions           ║
    ╚═══════════════════════════════════════╝
    
    🚀 Interface enhancements loaded successfully!
    📧 Contact: ahsantoufiq@archlabs.tech
    📱 Phone: +923121359857
    `);
});

// Export for external use if needed
window.ArchLabsEnhancements = {
    version: '1.0.0',
    initialized: true,
    contact: {
        email: 'ahsantoufiq@archlabs.tech',
        phone: '+923121359857'
    }
}; 