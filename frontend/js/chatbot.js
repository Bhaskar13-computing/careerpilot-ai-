const chatInput = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChatBtn");
const chatMessages = document.getElementById("chatMessages");

sendChatBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  // Show user message
  appendMessage("You", message, "chat-user");

  chatInput.value = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });

    const data = await response.json();

    appendMessage("AI", data.reply, "chat-bot");

  } catch (error) {
    appendMessage(
      "AI",
      "Sorry, I am not able to respond right now.",
      "chat-bot"
    );
  }
}

function appendMessage(sender, text, className) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-message ${className}`;
  msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
