[index.html.html](https://github.com/user-attachments/files/24064138/index.html.html)[script.js.js](https://github.com/user-attachments/files/24064126/script.js.js)[README.md](https://github.com/user-attachments/files/24064111/README.md)
# Gemaila Backend
Servidor oficial para el sistema empresarial inteligente GEMAILLA IA.

## Requisitos
- Node.js
- npm[server.js.js](https://github.com/user-attachments/files/24064130/server.js.js)import express from "express";
import cors from "cors";
const app = express();[Uploa<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GEMAILLA AI</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header class="header">
    <h1>GEMAILLA AI</h1>
    <p>Asistente Inteligente — Proyecto Real</p>
  </header>
  <main class="main">
    <section class="chat-box">
      <div id="messages" class="messages"></div>
      <textarea id="userInput" placeholder="Escribe tu mensaje..."></textarea>
      <button id="sendBtn">Enviar</button>
    </section>
  </main>
  <script src="script.js"></script>
</body>
</html>ding index.html.html…]()

app.use(cors());
app.use(express.json());
app.post("/api/chat", (req, res) => {
  const { message } = req.body;
  let reply = "";
  if (!message) reply = "No entendí tu mensaje.";
  else if (message.toLowerCase().includes("hola")) reply = "¡Hola Gilda! ¿Lista para avanzar con GEMAILLA AI?";
  else if (message.toLowerCase().includes("gemaila")) reply = "GEMAILLA AI es tu asistente conectado a un backend real.";
  else reply = `Recibí tu mensaje: ${message}`;
  res.json({ reply });
});
app.listen(3000, () => console.log("Servidor GEMAILLA AI corriendo en http://localhost:3000"));

- OpenAI API Key (en archivo .env)

## Instalación
Para instalar depe{[Uploadingdocument.getElementById("sendBtn").addEventListener("click", sendMessage);
function addMessage(who, text) {
  const box = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = who === "user" ? "user-msg" : "bot-msg";
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}
async function sendMessage() {
  const input = document.getElementById("userInput");
  const msg = input.value.trim();
  if (!msg) return;
  addMessage("user", msg);
  input.value = "";
  try {
    const res = await fetch("http://localhost:3000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    addMessage("bot", data.reply);
  } catch (e) {
    addMessage("bot", "Error al conectar con el servidor.");
  }
} script.js.js…]()

    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Ejecutar el script start",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "start"],
            "cwd": "${workspaceFolder}/01-banckend",
            "console": "integratedTerminal"
        }
    ]
}
[package.json](https://github.com/user-attachments/files/24064121/package.json)
ndencias:

