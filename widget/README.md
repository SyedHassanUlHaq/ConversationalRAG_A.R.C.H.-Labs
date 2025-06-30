# A.R.C.H. Labs Customer Support Widget

A beautiful, responsive customer support widget that integrates seamlessly with your portfolio website. Features an elegant chat interface powered by your custom RAG system.

## 🚀 Features

- **Sleek Design**: Modern, aesthetic design with smooth animations
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Accessible**: Full keyboard navigation and ARIA labels
- **Smart Notifications**: Shows attention-grabbing badge after user inactivity
- **Easy Integration**: Simple copy-paste integration
- **Dark Mode Support**: Automatic dark mode detection
- **Mobile Optimized**: Full-screen chat on mobile devices

## 📁 Files

- `index.html` - Demo page showing the widget in action
- `styles.css` - Complete styling for the widget
- `script.js` - JavaScript functionality and interactions

## 🔧 Quick Integration

### Step 1: Add CSS and JavaScript to your website

Add this to your website's `<head>` section:

```html
<!-- A.R.C.H. Labs Support Widget Styles -->
<link rel="stylesheet" href="path/to/widget/styles.css">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Add this before your closing `</body>` tag:

```html
<!-- A.R.C.H. Labs Support Widget Script -->
<script src="path/to/widget/script.js"></script>
```

### Step 2: Add Widget HTML

Add this HTML anywhere in your `<body>` (typically at the end):

```html
<!-- Customer Support Widget -->
<div class="support-widget" id="supportWidget">
    <!-- Support Button -->
    <div class="support-button" id="supportButton">
        <div class="button-content">
            <i class="fas fa-headset"></i>
            <span class="button-text">Support</span>
        </div>
        <div class="pulse-ring"></div>
    </div>

    <!-- Chat Window -->
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <div class="header-content">
                <div class="avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="header-text">
                    <h4>A.R.C.H. Labs Support</h4>
                    <span class="status">
                        <span class="status-dot"></span>
                        Online
                    </span>
                </div>
            </div>
            <button class="close-btn" id="closeBtn">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <div class="chat-iframe-container">
            <iframe 
                id="chatIframe"
                src="http://localhost:8000"
                frameborder="0"
                width="100%"
                height="100%">
            </iframe>
        </div>
        
        <div class="chat-footer">
            <div class="footer-text">
                <span>🚀 Powered by A.R.C.H. Labs AI</span>
            </div>
        </div>
    </div>

    <!-- Notification Badge -->
    <div class="notification-badge" id="notificationBadge">
        <span>1</span>
    </div>
</div>
```

### Step 3: Update the iframe URL

**Important**: Change the iframe `src` URL to your deployed RAG system:

```html
<iframe 
    id="chatIframe"
    src="https://your-rag-system-url.com"
    frameborder="0"
    width="100%"
    height="100%">
</iframe>
```

## 🎨 Customization

### Colors and Branding

Edit the CSS variables in `styles.css`:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --primary-color: #667eea;
    --primary-shadow: rgba(102, 126, 234, 0.3);
    --text-primary: #1e293b;
    --text-secondary: #64748b;
}
```

### Button Text and Labels

Modify the HTML content:

```html
<span class="button-text">Support</span> <!-- Change button text -->
<h4>A.R.C.H. Labs Support</h4> <!-- Change header title -->
<span>🚀 Powered by A.R.C.H. Labs AI</span> <!-- Change footer text -->
```

### Positioning

Change the widget position by modifying the CSS:

```css
.support-widget {
    bottom: 20px;  /* Distance from bottom */
    right: 20px;   /* Distance from right */
    left: 20px;    /* Use this instead of right for left positioning */
}
```

## 📱 Mobile Behavior

- **Small screens** (≤768px): Chat window becomes nearly full-screen
- **Touch devices**: Optimized touch targets and interactions
- **Orientation changes**: Automatically adjusts layout
- **Scroll locking**: Prevents background scrolling when chat is open

## ♿ Accessibility Features

- **Keyboard Navigation**: Full keyboard support with Tab, Enter, and Escape
- **ARIA Labels**: Proper labels for screen readers
- **Focus Management**: Logical focus flow
- **High Contrast**: Works with high contrast mode
- **Color Blind Friendly**: Doesn't rely solely on color for information

## 🔧 JavaScript API

The widget exposes these methods for programmatic control:

```javascript
// Open the chat
window.SupportWidget.open();

// Close the chat
window.SupportWidget.close();

// Toggle the chat
window.SupportWidget.toggle();

// Check if chat is visible
window.SupportWidget.isVisible();
```

## 🌐 Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+
- **Mobile browsers**: iOS Safari 14+, Chrome Mobile 90+

## 🚀 Deployment Checklist

### For Production:

1. **Update iframe URL** to your deployed RAG system
2. **Minify CSS and JavaScript** for better performance
3. **Test on all target devices** and browsers
4. **Verify HTTPS** if your main site uses HTTPS
5. **Set up analytics** tracking (optional)
6. **Test accessibility** with screen readers

### Performance Tips:

- The iframe loads in the background for faster opening
- CSS animations use `transform` for smooth performance
- JavaScript is optimized for minimal DOM manipulation
- Images and fonts are loaded from CDN for speed

## 🔐 Security Considerations

- Ensure your RAG system has proper CORS headers
- Use HTTPS for production deployment
- Validate and sanitize any user inputs
- Consider CSP (Content Security Policy) headers

## 📞 Support

For integration help or customization questions:

- **Email**: ahsantoufiq@archlabs.tech
- **Phone/WhatsApp**: +923121359857

---

## Demo

Open `index.html` in your browser to see the widget in action!

The widget will:
1. Appear with a subtle entrance animation
2. Show a pulsing ring to attract attention
3. Display a notification badge after 10 seconds
4. Expand on hover to show "Support" text
5. Open a beautiful chat window when clicked 