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
        self.chat_url = f"{host}/api/chat"

    # ==========================
    # LOAD
    # ==========================
    def load(self):

        logger.info(
            f"🧠 Tina connected to Ollama model: {self.model}"
        )

    # ==========================
    # CHAT
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

            # ==========================
            # SYSTEM PROMPT
            # ==========================
            if system_prompt:

                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # ==========================
            # USER PROMPT
            # ==========================
            messages.append({
                "role": "user",
                "content": user_prompt
            })

            # ==========================
            # REQUEST
            # ==========================
            response = requests.post(
                self.chat_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=180
            )

            response.raise_for_status()

            data = response.json()

            content = (
                data.get("message", {})
                .get("content", "")
                .strip()
            )

            if not content:
                return "I didn't understand that clearly."

            return content

        except requests.exceptions.ConnectionError:

            logger.error("Ollama server is not running.")

            return (
                "I can't connect to Ollama right now. "
                "Please start it using 'ollama serve'."
            )

        except Exception as e:

            logger.error(
                f"LLM Error: {e}",
                exc_info=True
            )

            return (
                "Something went wrong while "
                "processing your request."
            )

    # ==========================
    # SIMPLE GENERATE
    # ==========================
    def generate(self, prompt: str):

        return self.chat(user_prompt=prompt)


# ==========================
# GLOBAL INSTANCE
# ==========================
llm = TinaLLM(
    model="gemma3:4b"
)