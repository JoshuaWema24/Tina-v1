import logging
import requests

logger = logging.getLogger("Tina")


class TinaLLM:
    def __init__(
        self,
        model: str = "gemma3:4b",
        host: str = "http://localhost:11434"
    ):
        self.model = model
        self.host = host
        self.chat_url = f"{host}/api/chat"

    # ==========================
    # LOAD
    # ==========================
    def load(self):
        logger.info(f"🧠 Tina connected to Ollama model: {self.model}")

    # ==========================
    # CHAT (JARVIS-STABLE CORE)
    # ==========================
    def chat(
        self,
        user_prompt: str,
        system_prompt: str = "",
        temperature: float = 0.3,
        max_tokens: int = 300
    ) -> str:

        try:
            messages = []

            # SYSTEM PROMPT
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # USER PROMPT
            messages.append({
                "role": "user",
                "content": user_prompt
            })

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=180
            )

            # ==========================
            # HTTP CHECK
            # ==========================
            if response.status_code != 200:
                logger.error(
                    f"Ollama HTTP {response.status_code}: {response.text}"
                )
                return "Ollama error occurred while processing your request."

            # ==========================
            # JSON SAFE PARSE
            # ==========================
            try:
                data = response.json()
            except Exception:
                logger.error(f"Invalid JSON from Ollama: {response.text}")
                return "Model returned invalid response format."

            # ==========================
            # SAFE EXTRACTION
            # ==========================
            message = data.get("message")

            if not message:
                logger.error(f"Unexpected Ollama response: {data}")
                return "Model returned an empty response."

            content = message.get("content", "").strip()

            if not content:
                return "I couldn't generate a response clearly."

            return content

        # ==========================
        # TIMEOUT
        # ==========================
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out.")
            return "The model took too long to respond."

        # ==========================
        # CONNECTION ERROR
        # ==========================
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama server.")
            return (
                "I can't connect to Ollama right now. "
                "Please run 'ollama serve'."
            )

        # ==========================
        # GENERAL ERROR
        # ==========================
        except Exception as e:
            logger.error(f"LLM Error: {e}", exc_info=True)
            return "Something went wrong while processing your request."

    # ==========================
    # SIMPLE GENERATE WRAPPER
    # ==========================
    def generate(self, prompt: str):
        return self.chat(user_prompt=prompt)


# ==========================
# GLOBAL INSTANCE
# ==========================
llm = TinaLLM(model="gemma3:4b")