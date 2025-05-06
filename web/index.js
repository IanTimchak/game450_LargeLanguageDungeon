

$(document).ready(function () {
    const chatLog = document.getElementById('chat-log');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const scrollButton = document.getElementById('scroll-to-bottom');

    chatLog.addEventListener('scroll', () => {
        const isAtBottom = chatLog.scrollTop + chatLog.clientHeight >= chatLog.scrollHeight - 5;
        scrollButton.style.opacity = isAtBottom ? '0%' : '100%';
        scrollButton.style['pointer-events'] = isAtBottom ? 'none' : 'auto';

    });

    scrollButton.addEventListener('click', () => {
        chatLog.scrollTo({ top: chatLog.scrollHeight, behavior: 'smooth' });
    });

    chatInput.addEventListener('keydown', (e) => {
        const isInputFocused = document.activeElement === chatInput;
        const hasText = chatInput.value.trim().length > 0;

        if (e.key === 'Enter' && !e.shiftKey && isInputFocused && hasText) {
            e.preventDefault();
            sendButton.click(); // ✅ trigger existing submit logic
        }
    });

    //playSound
    // Expose the function to Python via eel
    eel.expose(playSoundEffect);
    function playSoundEffect(soundName, volume = 5, loop = false) {
        console.log(`[DEBUG] playSoundEffect called with soundName='${soundName}', volume=${volume}, loop=${loop}`);
    
        // Path to the sound files folder
        const soundFolder = 'sounds/';
        const soundPath = `${soundFolder}${soundName}.wav`;
    
        // Create an audio object
        const audio = new Audio(soundPath);
    
        // Set volume (scale 0.0 to 1.0)
        audio.volume = volume / 50;
    
        // Set loop if specified
        audio.loop = false;
    
        // Play the sound
        audio.play().catch(error => {
            console.error(`[ERROR] Failed to play sound '${soundName}':`, error);
        });
    }
    

    eel.expose(addAiMessage);
    function addAiMessage(message) {
        const aiMessage = document.createElement('div');
        aiMessage.className = 'chat-message ai';
        aiMessage.innerHTML = `
        <div class="chat-icon">A</div>
        <div class="chat-bubble">${message}</div>`;
        chatLog.appendChild(aiMessage);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function addUserMessage(message) {
        const userMessage = document.createElement('div');
        userMessage.className = 'chat-message user';
        userMessage.innerHTML = `
        <div class="chat-icon">U</div>
        <div class="chat-bubble">${message}</div>`;
        chatLog.appendChild(userMessage);
        chatInput.value = '';
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    $("#send-button").click(function () {
        eel.send_user_response(chatInput.value);
    });


    sendButton.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message === '') return;

        addUserMessage(message);
    });

    let isBouncing = false;
    chatLog.addEventListener('wheel', function (e) {
        const atTop = chatLog.scrollTop === 0;
        const atBottom = chatLog.scrollTop + chatLog.clientHeight >= chatLog.scrollHeight - 1;

        if (atTop && e.deltaY < 0 && !isBouncing) {
            isBouncing = true;
            chatLog.style.transition = 'transform 0.25s ease';
            chatLog.style.transform = 'translateY(12px)';
            setTimeout(() => {
                chatLog.style.transform = 'translateY(0)';
                setTimeout(() => {
                    chatLog.style.transition = '';
                    isBouncing = false;
                }, 250);
            }, 100);
        }

        if (atBottom && e.deltaY > 0 && !isBouncing) {
            isBouncing = true;
            chatLog.style.transition = 'transform 0.25s ease';
            chatLog.style.transform = 'translateY(-12px)';
            setTimeout(() => {
                chatLog.style.transform = 'translateY(0)';
                setTimeout(() => {
                    chatLog.style.transition = '';
                    isBouncing = false;
                }, 250);
            }, 100);
        }
    }, { passive: false });
});

