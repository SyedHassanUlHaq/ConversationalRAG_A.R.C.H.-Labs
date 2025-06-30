// A.R.C.H. Labs Customer Support Widget
document.addEventListener('DOMContentLoaded', function() {
    const supportButton = document.getElementById('supportButton');
    const chatWindow = document.getElementById('chatWindow');
    const closeBtn = document.getElementById('closeBtn');
    const notificationBadge = document.getElementById('notificationBadge');
    
    let isOpen = false;
    let hasInteracted = false;

    // Toggle chat window
    function toggleChat() {
        if (isOpen) {
            closeChat();
        } else {
            openChat();
        }
    }

    // Open chat window
    function openChat() {
        chatWindow.classList.add('active');
        notificationBadge.classList.add('hidden');
        isOpen = true;
        hasInteracted = true;
        
        // Prevent body scroll on mobile
        if (window.innerWidth <= 768) {
            document.body.style.overflow = 'hidden';
        }
        
        console.log('Support chat opened');
    }

    // Close chat window
    function closeChat() {
        chatWindow.classList.remove('active');
        isOpen = false;
        document.body.style.overflow = '';
        console.log('Support chat closed');
    }

    // Event listeners
    supportButton.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeChat();
    });

    // Close on outside click
    document.addEventListener('click', function(e) {
        if (isOpen && !chatWindow.contains(e.target) && !supportButton.contains(e.target)) {
            closeChat();
        }
    });

    // Prevent chat window clicks from closing
    chatWindow.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    // Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isOpen) {
            closeChat();
        }
    });

    // Show notification badge after 10 seconds if not interacted
    setTimeout(function() {
        if (!hasInteracted) {
            notificationBadge.classList.remove('hidden');
            console.log('Notification badge shown');
        }
    }, 10000);

    // Auto-hide notification after 30 more seconds
    setTimeout(function() {
        if (!hasInteracted) {
            notificationBadge.classList.add('hidden');
        }
    }, 40000);

    // Responsive handling
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768 && isOpen) {
            document.body.style.overflow = 'hidden';
        } else if (!isOpen) {
            document.body.style.overflow = '';
        }
    });

    // Accessibility improvements
    supportButton.setAttribute('aria-label', 'Open customer support chat');
    supportButton.setAttribute('role', 'button');
    supportButton.setAttribute('tabindex', '0');
    
    closeBtn.setAttribute('aria-label', 'Close chat window');
    
    chatWindow.setAttribute('role', 'dialog');
    chatWindow.setAttribute('aria-label', 'Customer support chat');

    // Keyboard navigation for support button
    supportButton.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleChat();
        }
    });

    console.log('🚀 A.R.C.H. Labs Support Widget initialized successfully!');
});

// Customer Support Widget JavaScript
class SupportWidget {
    constructor() {
        this.isOpen = false;
        this.hasInteracted = false;
        this.notificationTimeout = null;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupNotification();
        this.setupIframeHandling();
        this.preloadWidget();
    }

    bindEvents() {
        const supportButton = document.getElementById('supportButton');
        const closeBtn = document.getElementById('closeBtn');
        const chatWindow = document.getElementById('chatWindow');

        // Support button click
        supportButton.addEventListener('click', () => {
            this.toggleChat();
        });

        // Close button click
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.closeChat();
        });

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (this.isOpen && !chatWindow.contains(e.target) && !supportButton.contains(e.target)) {
                this.closeChat();
            }
        });

        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeChat();
            }
        });

        // Prevent chat window clicks from closing
        chatWindow.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        const chatWindow = document.getElementById('chatWindow');
        const notificationBadge = document.getElementById('notificationBadge');
        
        chatWindow.classList.add('active');
        this.isOpen = true;
        this.hasInteracted = true;
        
        // Hide notification badge
        notificationBadge.classList.add('hidden');
        
        // Focus the iframe after animation
        setTimeout(() => {
            const iframe = document.getElementById('chatIframe');
            if (iframe) {
                iframe.focus();
            }
        }, 400);

        // Track opening event
        this.trackEvent('chat_opened');
        
        // Add body class to prevent scrolling on mobile
        if (window.innerWidth <= 768) {
            document.body.style.overflow = 'hidden';
        }
    }

    closeChat() {
        const chatWindow = document.getElementById('chatWindow');
        
        chatWindow.classList.remove('active');
        this.isOpen = false;
        
        // Remove body scroll lock
        document.body.style.overflow = '';
        
        // Track closing event
        this.trackEvent('chat_closed');
    }

    setupNotification() {
        // Show notification badge after 10 seconds if user hasn't interacted
        this.notificationTimeout = setTimeout(() => {
            if (!this.hasInteracted) {
                this.showNotification();
            }
        }, 10000);
    }

    showNotification() {
        const notificationBadge = document.getElementById('notificationBadge');
        notificationBadge.classList.remove('hidden');
        
        // Auto-hide after 30 seconds
        setTimeout(() => {
            if (!this.hasInteracted) {
                notificationBadge.classList.add('hidden');
            }
        }, 30000);
    }

    setupIframeHandling() {
        const iframe = document.getElementById('chatIframe');
        
        // Handle iframe load
        iframe.addEventListener('load', () => {
            console.log('Support chat loaded successfully');
            this.trackEvent('chat_loaded');
        });

        // Handle iframe errors
        iframe.addEventListener('error', () => {
            console.error('Failed to load support chat');
            this.showFallbackMessage();
        });
    }

    showFallbackMessage() {
        const iframeContainer = document.querySelector('.chat-iframe-container');
        iframeContainer.innerHTML = `
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                padding: 40px 20px;
                text-align: center;
                background: #f8fafc;
            ">
                <div style="
                    font-size: 48px;
                    margin-bottom: 20px;
                    color: #94a3b8;
                ">💬</div>
                <h3 style="
                    font-size: 18px;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 12px;
                ">Chat Temporarily Unavailable</h3>
                <p style="
                    color: #64748b;
                    margin-bottom: 24px;
                    line-height: 1.5;
                ">Our chat system is currently offline. Please contact us directly for immediate assistance.</p>
                <div style="
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: left;
                    max-width: 280px;
                ">
                    <div style="margin-bottom: 12px;">
                        <strong style="color: #1e293b;">📧 Email:</strong><br>
                        <a href="mailto:ahsantoufiq@archlabs.tech" style="color: #667eea; text-decoration: none;">
                            ahsantoufiq@archlabs.tech
                        </a>
                    </div>
                    <div>
                        <strong style="color: #1e293b;">📱 Phone/WhatsApp:</strong><br>
                        <a href="tel:+923121359857" style="color: #667eea; text-decoration: none;">
                            +923121359857
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    preloadWidget() {
        // Preload the iframe to improve performance
        const iframe = document.getElementById('chatIframe');
        if (iframe && iframe.src) {
            // The iframe will start loading in the background
            console.log('Preloading support chat...');
        }
    }

    trackEvent(eventName, data = {}) {
        // Track widget interactions for analytics
        console.log(`Support Widget Event: ${eventName}`, data);
        
        // You can integrate with your analytics service here
        // Example: Google Analytics, Mixpanel, etc.
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'support_widget',
                ...data
            });
        }
    }

    // Public API methods
    open() {
        this.openChat();
    }

    close() {
        this.closeChat();
    }

    toggle() {
        this.toggleChat();
    }

    // Utility methods
    isVisible() {
        return this.isOpen;
    }

    hasUserInteracted() {
        return this.hasInteracted;
    }
}

// Responsive behavior
class ResponsiveHandler {
    constructor(widget) {
        this.widget = widget;
        this.init();
    }

    init() {
        this.handleResize();
        window.addEventListener('resize', () => this.handleResize());
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.handleResize(), 100);
        });
    }

    handleResize() {
        const chatWindow = document.getElementById('chatWindow');
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile && this.widget.isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }

        // Adjust chat window size on mobile
        if (isMobile) {
            chatWindow.style.height = `${window.innerHeight - 100}px`;
        } else {
            chatWindow.style.height = '600px';
        }
    }
}

// Accessibility enhancements
class AccessibilityHandler {
    constructor() {
        this.init();
    }

    init() {
        this.addAriaLabels();
        this.addKeyboardNavigation();
        this.addFocusManagement();
    }

    addAriaLabels() {
        const supportButton = document.getElementById('supportButton');
        const closeBtn = document.getElementById('closeBtn');
        const chatWindow = document.getElementById('chatWindow');

        supportButton.setAttribute('aria-label', 'Open customer support chat');
        supportButton.setAttribute('role', 'button');
        supportButton.setAttribute('tabindex', '0');

        closeBtn.setAttribute('aria-label', 'Close chat window');
        
        chatWindow.setAttribute('role', 'dialog');
        chatWindow.setAttribute('aria-label', 'Customer support chat');
        chatWindow.setAttribute('aria-modal', 'true');
    }

    addKeyboardNavigation() {
        const supportButton = document.getElementById('supportButton');
        
        supportButton.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                supportButton.click();
            }
        });
    }

    addFocusManagement() {
        const chatWindow = document.getElementById('chatWindow');
        const supportButton = document.getElementById('supportButton');
        
        // Focus management when opening chat
        chatWindow.addEventListener('transitionend', () => {
            if (chatWindow.classList.contains('active')) {
                const iframe = document.getElementById('chatIframe');
                if (iframe) {
                    iframe.focus();
                }
            }
        });
    }
}

// Initialize the widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main widget
    window.supportWidget = new SupportWidget();
    
    // Initialize responsive handler
    new ResponsiveHandler(window.supportWidget);
    
    // Initialize accessibility
    new AccessibilityHandler();
    
    // Make widget globally accessible
    window.SupportWidget = {
        open: () => window.supportWidget.open(),
        close: () => window.supportWidget.close(),
        toggle: () => window.supportWidget.toggle(),
        isVisible: () => window.supportWidget.isVisible()
    };

    console.log('A.R.C.H. Labs Support Widget initialized successfully! 🚀');
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && window.supportWidget) {
        // Page became visible - could refresh iframe if needed
        console.log('Page visible - support widget active');
    }
});

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SupportWidget, ResponsiveHandler, AccessibilityHandler };
} 