// A.R.C.H. Labs Customer Support Widget - Portfolio Integration
document.addEventListener('DOMContentLoaded', function() {
    // Configuration - A.R.C.H. Labs RAG Chatbot Production URL
    const CHATBOT_URL = 'https://web-production-d049c.up.railway.app';
    
    let isOpen = false;
    let hasInteracted = false;

    // Create and inject widget HTML
    function createWidget() {
        const widgetHTML = `
            <div class="arch-support-widget" id="archSupportWidget">
                <button class="arch-support-button" id="archSupportButton" type="button">
                    <div class="arch-button-content">
                        <i class="fa fa-headset"></i>
                        <span class="arch-button-text">Support</span>
                    </div>
                    <div class="arch-pulse-ring"></div>
                </button>

                <div class="arch-chat-window" id="archChatWindow">
                    <div class="arch-chat-header">
                        <div class="arch-header-content">
                            <div class="arch-avatar">
                                <i class="fa fa-robot"></i>
                            </div>
                            <div class="arch-header-text">
                                <h4>A.R.C.H. Labs Support</h4>
                                <span class="arch-status">
                                    <span class="arch-status-dot"></span>
                                    Online
                                </span>
                            </div>
                        </div>
                        <button class="arch-close-btn" id="archCloseBtn" type="button">
                            <i class="fa fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="arch-chat-iframe-container">
                        <iframe 
                            id="archChatIframe"
                            src="${CHATBOT_URL}"
                            frameborder="0"
                            width="100%"
                            height="100%">
                        </iframe>
                    </div>
                    
                    <div class="arch-chat-footer">
                        <div class="arch-footer-text">
                            <span>🚀 Powered by A.R.C.H. Labs AI</span>
                        </div>
                    </div>
                </div>

                <div class="arch-notification-badge hidden" id="archNotificationBadge">
                    <span>1</span>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    // Toggle chat window
    function toggleChat() {
        if (isOpen) {
            closeChat();
        } else {
            openChat();
        }
    }

    // Open chat
    function openChat() {
        const chatWindow = document.getElementById('archChatWindow');
        const badge = document.getElementById('archNotificationBadge');
        
        chatWindow.classList.add('active');
        badge.classList.add('hidden');
        isOpen = true;
        hasInteracted = true;
        
        if (window.innerWidth <= 768) {
            document.body.style.overflow = 'hidden';
        }
    }

    // Close chat
    function closeChat() {
        const chatWindow = document.getElementById('archChatWindow');
        chatWindow.classList.remove('active');
        isOpen = false;
        document.body.style.overflow = '';
    }

    // Initialize widget
    createWidget();

    // Event listeners
    document.getElementById('archSupportButton').addEventListener('click', toggleChat);
    document.getElementById('archCloseBtn').addEventListener('click', closeChat);

    // Close on outside click
    document.addEventListener('click', function(e) {
        const widget = document.getElementById('archSupportWidget');
        if (isOpen && !widget.contains(e.target)) {
            closeChat();
        }
    });

    // Close on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isOpen) {
            closeChat();
        }
    });

    // Show notification after 8 seconds
    setTimeout(function() {
        if (!hasInteracted) {
            document.getElementById('archNotificationBadge').classList.remove('hidden');
        }
    }, 8000);

    console.log('🚀 A.R.C.H. Labs Support Widget loaded');
}); 