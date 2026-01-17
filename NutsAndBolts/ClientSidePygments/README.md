# Running Pygments on the Client Side: Feasibility, Approaches, API Complexity, and Integration with Editors

Pygments is one of the most widely used syntax highlighters in the Python ecosystem. It supports hundreds of languages, has a powerful lexer/formatter architecture, and is deeply extensible. But Pygments is a **Python library**, and running it **client‑side** raises many architectural questions similar to Mistune — with some additional considerations specific to syntax highlighting.

This article explores all viable approaches to running Pygments in the browser, evaluates their trade‑offs, and discusses how to integrate them with WYSIWYG editors, custom syntax extensions, and alternative libraries.

---

# 1. Approaches to Running Pygments in the Browser

## Option A — **Transpile Pygments (Python → JavaScript)**

### Feasibility
Moderate. Pygments is pure Python, but:
- It contains **hundreds of lexers**, many auto‑generated.
- It uses regex-heavy logic.
- It relies on Python’s object model and dynamic dispatch.

Transpiling is possible but brittle.

### API Complexity
Pygments has a layered API:
- `lexers` (language detection, tokenization)
- `formatters` (HTML, LaTeX, RTF, etc.)
- `styles` (color themes)
- `highlight()` convenience function

Transpiling preserves the structure but:
- JS developers must work with Python‑style classes.
- Error messages become cryptic.
- Performance is slower than native JS.

### Variable Types
Transpiled Python → JS typically wraps Python types:
- Token streams become Python lists of tuples.
- Styles remain Python dicts.
- Regex behavior may differ.

### Extensions
Pygments supports:
- Custom lexers
- Custom formatters
- Custom styles

Transpiling preserves this, but writing JS‑side extensions becomes awkward.

### Verdict
**Possible but not pleasant.**  
Best only if you need exact Pygments behavior and can tolerate Python‑style APIs in JS.

---

## Option B — **Run Pygments inside a Python interpreter in the browser**

### Feasibility
High. Pyodide can run Pygments exactly as-is.

### Performance
- Startup cost: 5–10 MB WASM.
- Highlighting speed: good once loaded.
- Large code blocks: slower than native JS.

### API Complexity
Perfect fidelity:
- All lexers, formatters, and styles work.
- Custom lexers can be loaded dynamically.
- The `highlight()` function works unchanged.

### Variable Types
- Everything stays Python.
- JS ↔ Python bridging required.
- Passing large code strings back and forth is expensive.

### Extensions
Fully supported:
- You can register new lexers.
- You can override formatters.
- You can load custom styles.

### Verdict
**Most accurate, least lightweight.**  
Great for notebook-style tools, not ideal for lightweight web apps.

---

## Option C — **Client-side JS API that calls a server running Pygments**

### Feasibility
Very high.

### How it works
- Browser sends code + language to server.
- Server runs Pygments.
- Server returns HTML or token stream.

### API Complexity
Very simple client-side API:
\`\`\`js
highlight(code, lang).then(html => ...)
\`\`\`

### Variable Types
- Client receives HTML or JSON.
- No Python objects leak into JS.

### Extensions
- All extensions remain Python-side.
- No need to port lexers or formatters.
- Easy to maintain.

### Downsides
- Requires network round-trips.
- Offline mode impossible unless cached.
- Latency affects UX.

### Verdict
**Most practical for production.**  
Ideal for documentation sites, collaborative editors, and Moonlight-style servers.

---

## Option D — **Manual port of Pygments to JavaScript**

### Feasibility
Low to moderate.  
Pygments is large and complex:
- 300+ lexers
- Many regex-heavy rules
- Complex token hierarchies

A full port is unrealistic.  
A **subset port** is feasible.

### API Complexity
You can mimic Pygments:
- `highlight(code, lang)`
- `registerLexer()`
- `registerStyle()`

But it will not be 1:1.

### Variable Types
- Native JS arrays and objects.
- Much easier to integrate with web apps.

### Extensions
You must rewrite:
- Lexers
- Styles
- Formatters

This is a lot of work.

### Upsides
- Fastest performance.
- Smallest bundle size.
- Best integration with WYSIWYG editors.
- Works offline.

### Downsides
- Hard to maintain parity with Pygments.
- Every new lexer must be ported manually.
- Hard to match Pygments’ accuracy.

### Verdict
**Best for performance, worst for maintenance.**  
Use only if you need a small subset of languages.

---

# 2. Additional Considerations Unique to Pygments

Pygments is more complex than Mistune in several ways:

### 1. **Language detection**
Pygments can guess languages using heuristics.  
Porting this to JS is expensive.

### 2. **Token hierarchy**
Pygments uses a rich token taxonomy:
- `Token.Keyword`
- `Token.Literal.String`
- `Token.Comment`
- etc.

JS libraries often use simpler token sets.

### 3. **Formatter complexity**
Pygments supports:
- HTML
- LaTeX
- RTF
- Terminal colors
- Image output

Only HTML is relevant client-side.

### 4. **Performance**
Syntax highlighting is CPU-heavy.  
Running it in WASM or JS must be optimized.

---

# 3. Integration with WYSIWYG Editors

Integrating syntax highlighting into editors like:
- CodeMirror
- Monaco
- TipTap
- ProseMirror
- Quill
- TinyMCE

requires special handling.

### Option A — Highlight on paste or blur
- User pastes code.
- Editor sends code to Pygments (client or server).
- Highlighted HTML is inserted.

### Option B — Highlight on-the-fly
- Editor triggers highlighting on each keystroke.
- Requires **fast** highlighter (JS-native).
- Pygments-in-Pyodide is too slow for this.

### Option C — Token-based editor integration
- Editor uses Pygments token stream.
- Editor applies its own styling.

This requires:
- A JSON formatter for Pygments.
- A mapping from Pygments tokens → editor tokens.

### Option D — Hybrid approach
- Use JS-native highlighter for live editing.
- Use Pygments for final rendering.

This is common in documentation systems.

---

# 4. Extending Syntax

Pygments supports:
- Custom lexers
- Custom token rules
- Custom styles

### Python-side extensions
Work perfectly in:
- Pyodide
- Server-side Pygments

### JS-side extensions
Only possible if:
- You manually port lexers
- Or you write a JS wrapper around transpiled Python

This is painful.

### Best practice
**Keep lexers in Python** and run them server-side or in Pyodide.

---

# 5. Alternative Client-Side Syntax Highlighters

If your goal is simply client-side highlighting, consider native JS libraries:

### **Highlight.js**
- Very popular
- Many languages
- Easy to extend
- Good performance

### **Prism.js**
- Lightweight
- Modular
- Great for documentation sites
- Easy to theme

### **Shiki**
- Uses VSCode grammars
- High accuracy
- Beautiful themes
- Runs in WebAssembly

### **CodeMirror / Monaco built-in lexers**
- Designed for editors
- Fast incremental parsing
- Great for WYSIWYG integration

### When to prefer alternatives
- When you need live highlighting.
- When you need small bundle size.
- When you need native JS performance.
- When you don’t need Pygments’ exact token taxonomy.

---

# 6. Summary of Approaches

| Approach | Accuracy | Performance | Startup Cost | Extensibility | Maintenance | Best Use Case |
|---------|----------|-------------|--------------|---------------|-------------|----------------|
| Python → JS transpile | Medium | Medium | Medium | Medium | High | Exact behavior in JS |
| Python interpreter in JS | High | Medium | High | High | Low | Notebook-like tools |
| JS API → server | High | High | Low | High | Low | Production apps |
| Manual JS port | Medium | High | Low | Medium | Very High | Offline + fast |

---

# 7. Final Recommendations

### If you want **exact Pygments behavior**:
Use **Pyodide** or **server-side Pygments**.

### If you want **fast client-side highlighting**:
Use **Prism.js**, **Highlight.js**, or **Shiki**.

### If you want **WYSIWYG integration**:
Use a **JS-native highlighter** for live editing and Pygments for final rendering.

### If you want **custom lexers**:
Keep them in Python and run Pygments server-side or in Pyodide.

---

If you want, I can now generate:
- A combined Mistune + Pygments client-side architecture guide  
- A Moonlight-style “SyntaxServer.md” addon  
- Or a comparison table of all Markdown + highlighting strategies  
