# DIAGRAMS.md — TipTap–Flask Markdown Workbench Architecture & UML

This document provides an architectural overview of the TipTap–Flask Markdown Workbench.  
All diagrams use **Mermaid**, compatible with GitHub’s renderer.

---

# 1. Introduction

## 1.1 Purpose
This document explains the structure, behavior, and intent of the system using diagrams and short narrative explanations.

## 1.2 Audience
- Architects  
- Programmers  
- Frontend engineers  
- Backend engineers  
- Non‑technical readers  

---

# 2. High‑Level Overview

The system is a **browser‑based Markdown workbench** backed by Flask:

- Left pane → TipTap rich‑text editor  
- Right pane → rendered HTML  
- Bottom pane → syntax‑highlighted Markdown  
- Backbone.js view coordinates UI and AJAX  
- Vite bundles frontend into `static/js/assets/main.js`  
- Flask serves UI and parses Markdown  

---

# 3. Project Structure Diagram

### Explanation
A map of the project’s folders and key files.

```mermaid
flowchart TD
  subgraph Root["project-root"]
    APP[app.py]
    REQ[requirements.txt]
    VITECFG[vite.config.js]

    subgraph Frontend["frontend"]
      MAINJS[main.js]
    end

    subgraph Static["static"]
      subgraph CSS["css"]
        STYLE[style.css]
      end
      subgraph JS["js"]
        subgraph Assets["assets"]
          BUNDLE[main.js - Vite bundle]
        end
      end
    end

    subgraph Templates["templates"]
      INDEX[index.html]
    end
  end

  VITECFG --> MAINJS
  MAINJS --> BUNDLE
  APP --> INDEX
  APP --> BUNDLE
  INDEX --> STYLE
```

---

# 4. Core Component Architecture

### Explanation
Shows the main runtime components and how they relate.

```mermaid
classDiagram
  class FlaskApp {
    +index()
    +parse()
    -markdown_parser
    -formatter
  }

  class IndexTemplate {
    +TipTap mount point
    +Pane layout
    +Loads JS bundle
    +Loads CSS
  }

  class AppView {
    -editor
    +initialize()
    +getMarkdown()
    +setMarkdown(md)
    +onSubmit()
    +localRender()
    +updateRightPane(html)
    +updateMarkdownPane(md)
    +syncHeights()
  }

  class TipTapEditor {
    -content
    +getHTML()
    +setContent()
  }

  class HtmlToMarkdown {
    +htmlToMarkdown(html)
  }

  class FlaskParser {
    +POST /parse
    -markdown_parser
    -highlight()
  }

  FlaskApp --> IndexTemplate : renders
  IndexTemplate --> AppView : instantiated
  AppView --> TipTapEditor : controls
  AppView --> HtmlToMarkdown : converts
  AppView --> FlaskParser : AJAX calls
  FlaskParser --> FlaskApp : internal
```

---

# 5. Behavioral Diagram

## 5.1 Sequence: Editing → Submitting → Rendering

```mermaid
sequenceDiagram
  actor User
  participant Browser as Browser - AppView and TipTap
  participant Editor as TipTap Editor
  participant Converter as HtmlToMarkdown
  participant Flask as Flask parse endpoint
  participant Parser as Markdown Parser

  User->>Editor: Type rich text
  Editor-->>Browser: getHTML()
  User->>Browser: Click Submit
  Browser->>Editor: getHTML()
  Editor-->>Browser: HTML content
  Browser->>Converter: htmlToMarkdown(HTML)
  Converter-->>Browser: Markdown
  Browser->>Flask: POST /parse
  Flask->>Parser: parse(markdown)
  Parser-->>Flask: html + highlighted md
  Flask-->>Browser: JSON response
  Browser->>Browser: update panes
  Browser-->>User: Updated HTML + Markdown
```

---

# 6. Deployment Diagram

```mermaid
flowchart LR
  subgraph UserMachine["User Machine"]
    BROWSER[Web Browser - TipTap and Backbone]
  end

  subgraph Server["Flask Server"]
    APP[app.py]
    TEMPLATE[index.html]
    STATICJS[main.js bundle]
    STATICCSS[style.css]
  end

  BROWSER -->|GET /| APP
  APP --> TEMPLATE
  APP --> STATICJS
  APP --> STATICCSS

  BROWSER -->|POST /parse| APP
  APP --> BROWSER
```

---

# 7. Summary

## 7.1 What This Architecture Achieves
- Clear separation of frontend and backend  
- Single‑page workbench with synchronized panes  
- Simple deployment  
- Extensible Markdown + HTML pipeline  

## 7.2 Why It Matters
A clean example of integrating TipTap, Backbone, Vite, and Flask into a cohesive editing environment.

---

# End of DIAGRAMS.md
