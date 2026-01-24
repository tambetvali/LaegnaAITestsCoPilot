# Services/litgpt_streamer.py

import json
import os

if __name__ == "__main__" or "servicesrelative" not in globals(): servicesrelative = __name__ == "__main__"
if servicesrelative:
    # If you run the script directly, services are in the same folder.
    from service import AIService
    from filename import filename
else:
    # If you run the parent script, this folder forms a subpackage.
    from Services.service import AIService
    from Services.filename import filename

from litgpt import LLM


class LitGPTBasicStreamer(AIService):
    """
    LitGPT-backed AIService implementation using the high-level LLM API.
    - Uses LLM.load(modelname) exactly like the LitGPT quick-start.
    - No extra parameters (no temperature, no max tokens, etc.).
    - ask() creates a child instance with inherited history.
    - __call__() streams the final answer via Python yield (character-wise).
    """

    def __init__(self, modelconf, parent=None):
        super().__init__(parent)

        # Minimal config: modelpath or model
        self.modelname = modelconf.get("modelpath", modelconf.get("model"))

        # AIService compatibility
        self.lazy = True
        self.answer = ""

        # Reuse parent's LLM instance if possible
        if parent is not None and isinstance(parent, LitGPTBasicStreamer):
            self.llm = parent.llm
        else:
            # This matches the quick-start:
            # llm = LLM.load("Qwen/Qwen2.5-0.5B")
            self.llm = LLM.load(self.modelname)

    # ---------------------------------------------------------
    # ASK: create a child instance and register the question
    # ---------------------------------------------------------
    def ask(self, question, local=False):
        child = LitGPTBasicStreamer(
            {"modelpath": self.modelname},
            parent=self
        )
        child.asked(question, local)
        return child

    # ---------------------------------------------------------
    # CALL: run generation and stream the answer via yield
    # ---------------------------------------------------------
    def __call__(self):
        self.lazy = False

        messages = self.messagelist()
        prompt = self._messages_to_prompt(messages)

        # Minimalist generate, exactly like the manual:
        # text = llm.generate("Correct the spelling: ...")
        text = self.llm.generate(prompt)

        # Store and register answer
        self.answer = text
        self.answered(self.answer)

        # Stream as a sequence of chunks (here: characters)
        for ch in text:
            yield ch

    # ---------------------------------------------------------
    # Convert message list to a prompt
    # ---------------------------------------------------------
    def _messages_to_prompt(self, messages):
        out = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                out.append(f"[SYSTEM] {content}\n")
            elif role == "user":
                out.append(f"[USER] {content}\n")
            elif role == "assistant":
                out.append(f"[ASSISTANT] {content}\n")

        out.append("[ASSISTANT] ")
        return "".join(out)


# ---------------------------------------------------------
# __main__ — test harness, same pattern as other services
# ---------------------------------------------------------
if __name__ == "__main__":
    # Load selected model configuration
    selectfile = filename("model_select.json")

    with open(selectfile, "r") as f:
        modelconf = json.load(f)

    # Ensure modelpath exists; fall back to model if needed
    if "modelpath" not in modelconf:
        modelconf["modelpath"] = modelconf.get("model")

    service = LitGPTBasicStreamer(modelconf)

    question = "Explain quantum entanglement in simple terms."

    print("Q:", question)
    print("A: ", end="", flush=True)

    child = service.ask(question)

    print("NON-Streaming output!:\n")

    for chunk in child():
        print(chunk, end="", flush=True)

    print("\n\nFinal answer stored in child.answer:")
    print(child.answer)
