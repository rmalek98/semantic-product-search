// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('sendButton');
    const chatInput = document.getElementById('chatInput');
    const chatHistory = document.getElementById('chatHistory');
    const productResults = document.getElementById('productResults');
    
    sendButton.addEventListener('click', sendMessage);
    
    // Enter key to send message
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Focus input on load
    chatInput.focus();
    
    // Welcome message
    appendMessage('assistant', '👋 Hi! I\'m your SmartShop AI assistant. Ask me to find products like "I need running shoes" or "Show me electronics"!');
    
    function appendMessage(sender, text) {
        const messageElem = document.createElement('div');
        messageElem.className = `chat-message ${sender}`;
        const senderName = sender === 'user' ? 'You' : 'SmartShop';
        messageElem.innerHTML = `<strong>${senderName}:</strong> ${text}`;
        chatHistory.appendChild(messageElem);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Disable input and button
        chatInput.disabled = true;
        sendButton.disabled = true;
        
        // Show user's message
        appendMessage('user', message);
        
        // Clear the input field
        chatInput.value = '';
        
        // Show loading indicator
        productResults.innerHTML = '<div class="loading">Finding the perfect products for you</div>';
        
        // Add typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'chat-message assistant';
        typingIndicator.id = 'typing-indicator';
        typingIndicator.innerHTML = '<strong>SmartShop:</strong> <span class="typing-dots">Thinking</span>';
        chatHistory.appendChild(typingIndicator);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        
        // Animate typing dots
        const typingDots = typingIndicator.querySelector('.typing-dots');
        let dotCount = 0;
        const typingInterval = setInterval(() => {
            typingDots.textContent = 'Thinking' + '.'.repeat((dotCount % 3) + 1);
            dotCount++;
        }, 500);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            clearInterval(typingInterval);
            const typingElem = document.getElementById('typing-indicator');
            if (typingElem) {
                typingElem.remove();
            }
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get recommendations');
            }
            
            const data = await response.json();
            
            // Show AI reply in chat
            appendMessage('assistant', data.reply);
            
            // Render product recommendations with animation
            if (data.recommendations && data.recommendations.length > 0) {
                productResults.innerHTML = '';
                data.recommendations.forEach((product, index) => {
                    setTimeout(() => {
                        const card = createProductCard(product);
                        productResults.appendChild(card);
                    }, index * 100); // Stagger animation
                });
            } else {
                productResults.innerHTML = '<div class="loading">No products found. Try a different search!</div>';
            }
        } catch (error) {
            console.error('Error:', error);
            appendMessage('assistant', '❌ Sorry, I encountered an error. Please try again!');
            productResults.innerHTML = '<div class="loading">Error fetching recommendations. Please try again.</div>';
        } finally {
            // Re-enable input and button
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.focus();
        }
    }
    
    function createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        // Format price
        const price = parseFloat(product.price || 0).toFixed(2);
        
        // Get similarity score if available
        const similarity = product.similarity_score ? 
            `<div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem;">Match: ${(product.similarity_score * 100).toFixed(0)}%</div>` : '';
        
        card.innerHTML = `
            <img src="${product.image_url || 'https://via.placeholder.com/200'}" 
                 alt="${product.name || 'Product'}" 
                 onerror="this.src='https://via.placeholder.com/200/cccccc/666666?text=No+Image'">
            <h2>${product.name || 'Unnamed Product'}</h2>
            <div class="category">${product.category || 'Uncategorized'}</div>
            <p>${product.description || 'No description available'}</p>
            <p class="price">$${price}</p>
            ${similarity}
        `;
        
        return card;
    }
});
