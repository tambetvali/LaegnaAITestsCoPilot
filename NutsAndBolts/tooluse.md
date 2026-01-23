# 🤝 Tool Use as a “Contract” Between You and the AI  
A practical, implementation‑focused explanation for Python, Flask, and Ollama developers.

This describes **how an AI knows tools exist**, **how it decides to use them**, **how metadata is injected**, and **how syntax conventions (JSON/XML) trigger tool‑aware behavior**.

## Introduction

These ten sections here are meant to give you a clear, practical roadmap for understanding how modern AI systems handle questions, tools, and hidden internal logic. The goal is to show how a simple user request becomes a structured exchange involving system prompts, tool definitions, backend orchestration, and the model’s final answer. By breaking the process into layers, the chapters explain how an AI decides what to do, when to call a tool, and how the backend quietly manages everything behind the scenes.

Across the chapters, you’ll see how tool contracts are formed, how the model interprets them, and how hidden metadata shapes the visible output. You’ll also learn how session context is maintained, how tool calls and results are separated from user-facing text, and why certain internal steps must remain invisible. Each chapter builds on the previous one, gradually revealing the full structure of a tool-enabled AI conversation.

By the end, you’ll have a practical mental model for designing your own AI systems—whether you’re building a chatbot, an automation agent, or a Flask-based application using a local model like Ollama. The chapters give you the conceptual foundation to combine Q&A, tools, context, and backend logic into a coherent, reliable workflow.

---

# 1. 🟦 How an AI Knows a “Tool Use Contract” Exists

An AI **does not inherently know** that tools exist.  
It only knows because **you explicitly give it a contract** in the request.

This contract is created through:

### ✔ A. System instructions  
Example:
```
You have access to the following tools. Use them when appropriate.
```

### ✔ B. Tool definitions  
You provide a structured description of each tool:
- name  
- description  
- parameters  
- parameter types  
- required fields  

Example:
```json
{
  "name": "search_web",
  "description": "Search the internet for factual information.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  }
}
```

### ✔ C. A model trained on tool‑calling patterns  
Modern LLMs have seen millions of examples of:
- JSON schemas  
- function signatures  
- API calls  
- structured arguments  

So when you give them a tool definition, they recognize the pattern and treat it as a contract.

### ✔ D. The AI responds according to the contract  
Once the contract is established, the model knows:

- **when** to call a tool  
- **how** to format the call  
- **what arguments** to include  
- **how to continue the conversation** after the tool result is returned  

---

# 2. 🟩 How Metadata and Parameters Are Added

Metadata is injected into the model request by **your backend**, not by the model.

Typical metadata includes:

### ✔ System prompt  
Defines behavior, persona, rules.

### ✔ Tool definitions  
JSON schema or XML description.

### ✔ Conversation history  
All previous messages.

### ✔ Tool results  
Returned as:
```json
{"role": "tool", "content": "..."}
```

### ✔ Additional metadata  
Depending on framework:
- temperature  
- max tokens  
- stop sequences  
- model name  
- user ID  
- safety settings  

### ✔ The model sees all metadata as part of its input context  
It does not distinguish between:
- system instructions  
- tool definitions  
- developer messages  
- user messages  

It simply processes the entire context window.

---

# 3. 🟨 JSON vs XML Tool Syntax — Meta‑Guidelines

There is **no universal standard**, but there are strong conventions.

## 🟦 JSON Function Calling (OpenAI‑style)
This is the **dominant** and most reliable syntax.

### Why JSON works best:
- Models are trained heavily on JSON  
- Easy to parse  
- Strict structure  
- Works across almost all modern LLMs  
- Supported by OpenAI, Anthropic, Google, Mistral, Groq, LiteLLM, etc.

### When to use JSON:
- When you want maximum reliability  
- When you want automatic argument parsing  
- When you want the model to choose tools autonomously  

### Trigger signs for the model:
- Presence of `"tools": [...]`  
- JSON schema definitions  
- System instructions referencing tools  
- Prior examples in the prompt  

The model recognizes:
> “I should output a JSON object with a tool name and arguments.”

---

## 🟧 XML / Tag‑Based Syntax
Older or custom models sometimes prefer XML‑like tags.

### Why XML works:
- Models have seen HTML/XML during training  
- Easy to embed in natural language  
- Good for custom or legacy systems  

### When to use XML:
- When JSON parsing is unreliable  
- When building a custom DSL  
- When working with older models  

### Trigger signs:
- `<tool>` tags in the prompt  
- System instructions referencing XML  
- Examples of XML tool calls  

The model recognizes:
> “I should wrap tool calls in XML tags.”

---

## 🟨 Natural Language Tool Invocation
Example:
```
CALL search_web(query="weather in Barcelona")
```

### When to use:
- When working with small models  
- When JSON/XML is too strict  
- When building a conversational agent  

### Trigger signs:
- System prompt instructs natural language calls  
- Examples provided  

---

# 4. 🟪 Is This the Same for All Models?

### ✔ Mostly yes — but with differences.

| Model Type | JSON Support | XML Support | Natural Language |
|------------|--------------|-------------|------------------|
| OpenAI GPT | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Anthropic Claude | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Google Gemini | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Mistral | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Llama 3 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Qwen | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Small local models | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### Key insight:
> Models respond best to the syntax they were trained on.

JSON is the safest universal choice.

---

# 5. 🟫 Summary — The Tool Use Contract

### ✔ You define the contract  
Through system prompts + tool definitions.

### ✔ The model recognizes the contract  
Because it has seen similar patterns during training.

### ✔ Metadata is injected by your backend  
Not by the model.

### ✔ JSON is the strongest standard  
XML and natural language work but are less consistent.

### ✔ The model matches the syntax you provide  
It adapts to the examples and structure you give it.

This is the foundation of reliable tool‑enabled AI systems.

# 6. 🟦 Lowest-Level Q&A Strings and the Tool-Use Contract

At the lowest level, an LLM request is just a **sequence of messages**:

```json
[
  {"role": "system", "content": "You can use tools."},
  {"role": "user", "content": "Find all markdown files in my project."}
]
```

But the *contract* for tool use is created by adding **tool definitions** to the metadata of the request:

```json
"tools": [
  {
    "name": "find_files",
    "description": "Search the filesystem for files matching a pattern.",
    "parameters": {
      "type": "object",
      "properties": {
        "pattern": { "type": "string" }
      },
      "required": ["pattern"]
    }
  }
]
```

The model sees this and understands:

- A tool named `find_files` exists  
- It has a purpose  
- It has a schema  
- It can call it by outputting a JSON object  

When the model decides to use the tool, it responds with a **tool-use report**:

```json
{
  "tool": "find_files",
  "arguments": {
    "pattern": "*.md"
  }
}
```

Your backend executes the tool and returns:

```json
{
  "role": "tool",
  "content": "Found 12 markdown files."
}
```

Then the model continues the conversation:

```json
{
  "role": "assistant",
  "content": "I found 12 markdown files in your project."
}
```

This is the full contract:  
**You define the tools → the model calls them → you return results → the model explains the results.**

---

# 7. 🟩 What Is Hidden and Why — Developer Responsibilities

### Hidden from the user:
- System prompt  
- Tool definitions  
- Tool schema  
- Developer instructions  
- Tool results (raw form)  
- Conversation metadata  
- Safety rules  
- Routing logic  
- Summaries of earlier messages  

### Why it’s hidden:
- To avoid confusing the user  
- To prevent prompt injection  
- To keep the interface clean  
- To allow the model to reason internally  
- To allow tools to operate securely  

### What the interface developer must do:
1. **Inject system prompts**  
   Define behavior, persona, rules.

2. **Inject tool definitions**  
   Provide JSON schemas or XML definitions.

3. **Capture tool calls**  
   Detect when the model outputs a tool request.

4. **Execute tools safely**  
   Validate arguments, sanitize paths, enforce permissions.

5. **Return tool results**  
   Feed results back as `"role": "tool"` messages.

6. **Continue the conversation**  
   Let the model generate a final user-facing answer.

The developer is responsible for the entire orchestration layer.

---

# 8. 🟨 Three Case Stories of Tool Use

## Case 1: Finding Files (Local Search Tool)

**User:**  
“Show me all Python files in my project.”

**Model:**  
```json
{"tool": "find_files", "arguments": {"pattern": "*.py"}}
```

**Backend:**  
Runs a filesystem search.

**Tool result:**  
```json
{"role": "tool", "content": ["app.py", "utils/helpers.py"]}
```

**Model final answer:**  
“You have 2 Python files: `app.py` and `utils/helpers.py`.”

---

## Case 2: Accessing a Web Page (Web Fetch Tool)

**User:**  
“Summarize the latest Python release notes.”

**Model:**  
```json
{"tool": "fetch_url", "arguments": {"url": "https://python.org/news"}}
```

**Backend:**  
Downloads the page, extracts text.

**Tool result:**  
```json
{"role": "tool", "content": "Python 3.x introduces ..."}
```

**Model final answer:**  
“Python 3.x introduces improvements to ...”

---

## Case 3: Modifying User Data or Files (Write Tool)

**User:**  
“Add a note to my todo list: ‘Fix the login bug.’”

**Model:**  
```json
{"tool": "append_to_file", "arguments": {"path": "todo.txt", "text": "Fix the login bug"}}
```

**Backend:**  
Appends to the file.

**Tool result:**  
```json
{"role": "tool", "content": "Note added successfully."}
```

**Model final answer:**  
“I added the note to your todo list.”

---

# 9. 🟧 Hidden Communication in Tool-Enabled Systems

Hidden communication includes:

### ✔ Tool definitions  
The model sees them; the user does not.

### ✔ Tool call messages  
The model outputs them; the user does not see them.

### ✔ Tool results  
Returned to the model; the user sees only the final summary.

### ✔ System-level metadata  
Temperature, max tokens, stop sequences.

### ✔ Developer instructions  
Rules, constraints, safety instructions.

### ✔ Summaries of earlier messages  
Used to maintain context without exceeding token limits.

### ✔ Routing logic  
Which model to use, when to switch models.

### ✔ Internal reasoning  
Models generate chain-of-thought internally but do not reveal it.

The developer must manage all of this behind the scenes.

---

# 10. 🟪 A Common Mental Model for Building Q&A + Tools

Here is a practical framework for thinking about tool-enabled AI systems:

### **1. Inputs**
- User question  
- System prompt  
- Tool definitions  
- Conversation history  
- Developer metadata  

### **2. Interpretation**
The model decides:
- Does the user want an answer?  
- Does the user want an action?  
- Does the user want data retrieval?  
- Does the user want file manipulation?  

### **3. Decision**
The model chooses:
- Respond normally  
- Call a tool  
- Ask for clarification  

### **4. Tool Execution**
Backend:
- Validates arguments  
- Executes the tool  
- Returns results  

### **5. Integration**
Model:
- Reads tool results  
- Synthesizes a final answer  

### **6. Output**
User sees:
- A clean, natural-language answer  
- No tool noise  
- No metadata  
- No internal reasoning  

### **7. Developer Loop**
You maintain:
- Tool definitions  
- System prompts  
- Safety rules  
- Context management  
- File access rules  
- API integrations  

This mental model helps you design reliable, predictable Q&A systems with tools.
