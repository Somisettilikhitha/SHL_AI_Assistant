const chatArea =
    document.getElementById(
        "chat-area"
    );

const input =
    document.getElementById(
        "message-input" 
    );

// ===================================
// SEND MESSAGE
// ===================================

async function sendMessage() {

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    // ===================================
    // USER MESSAGE
    // ===================================

    chatArea.innerHTML += `

        <div class="user-message">
            ${message}
        </div>

    `;

    // ===================================
    // LOADING
    // ===================================

    const loadingId = Date.now();

    chatArea.innerHTML += `

        <div
            class="bot-message"
            id="loading-${loadingId}"
        >

            <div class="loading">
                Thinking...
            </div>

        </div>

    `;

    // Auto Scroll

    chatArea.scrollTop =
        chatArea.scrollHeight;

    // Clear Input

    input.value = "";

    try {

        // ===================================
        // API CALL
        // ===================================

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    messages: [

                        {
                            role: "user",
                            content: message
                        }

                    ]
                })
            }
        );

        const data =
            await response.json();

        // Remove Loading

        document
            .getElementById(
                `loading-${loadingId}`
            )
            .remove();

        // ===================================
        // BOT RESPONSE
        // ===================================

        let html = `

            <div class="bot-message">

                <p>
                    ${data.reply}
                </p>

        `;

        // ===================================
        // RECOMMENDATIONS
        // ===================================

        if (

            data.recommendations &&
            data.recommendations.length > 0

        ) {

            data.recommendations.forEach(
                item => {

                const type =
                    item.test_type
                    .toLowerCase();

                html += `

                    <div class="assessment-card">

                        <h3>
                            ${item.name}
                        </h3>

                        <p>

                            Recommended based on:
                            hiring query relevance,
                            assessment metadata,
                            and SHL semantic matching.

                        </p>

                        <a
                            href="${item.url}"
                            target="_blank"
                        >
                            View Assessment
                        </a>

                        <br>

                        <span class="tag ${type}">
                            ${item.test_type}
                        </span>

                    </div>

                `;
            });
        }

        html += `</div>`;

        // Add Response

        chatArea.innerHTML += html;

        // ===================================
        // AUTO SCROLL
        // ===================================

        chatArea.scrollTop =
            chatArea.scrollHeight;
    }

    catch (error) {

        document
            .getElementById(
                `loading-${loadingId}`
            )
            .remove();

        chatArea.innerHTML += `

            <div class="bot-message">

                Error connecting
                to backend.

            </div>

        `;
    }
}

// ===================================
// ENTER KEY SUPPORT
// ===================================

input.addEventListener(
    "keypress",

    function(event) {

        if (
            event.key === "Enter"
        ) {

            sendMessage();
        }
    }
);