# Implementation: Flask + Mistune + TipTap + Backbone + Pygments

Below is a minimal but complete implementation matching the previously defined API and Spec.  
File layout:

- `app.py`
- `templates/index.html`
- `static/js/app.js`
- `static/css/style.css`
- `requirements.txt`

---

## `requirements.txt`

```txt
Flask
mistune
Pygments
```

---

## `app.py`

```python
from flask import Flask, render_template, request, jsonify
import mistune
from pygments import highlight
from pygments.lexers import MarkdownLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

markdown_parser = mistune.create_markdown()
formatter = HtmlFormatter(cssclass="codehilite", nowrap=False)


@app.route("/", methods=["GET"])
def index():
    example_markdown = """# TipTap–Flask Markdown Workbench

Type on the left, press the arrow button,
and see the parsed result on the right.

```python
def hello():
    print("Hello, world!")
```
"""
    return render_template("index.html", example_markdown=example_markdown)


@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json(force=True)
    html = data.get("html", "")

    markdown_text = data.get("markdown", "").strip()

    if not markdown_text:
        markdown_text = "_(No markdown provided by client)_"

    rendered_html = markdown_parser(markdown_text)

    highlighted_markdown = highlight(
        markdown_text,
        MarkdownLexer(),
        formatter
    )

    return jsonify(
        {
            "markdown": markdown_text,
            "html": rendered_html,
            "highlighted_markdown": highlighted_markdown,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
```

---

## `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TipTap–Flask Markdown Workbench</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    <style>
        {{ formatter.get_style_defs('.codehilite')|safe }}
    </style>

    <script src="https://unpkg.com/@tiptap/core@2.0.0-beta.220/dist/tiptap-core.umd.js"></script>
    <script src="https://unpkg.com/@tiptap/starter-kit@2.0.0-beta.220/dist/tiptap-starter-kit.umd.js"></script>

    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.13.6/underscore-min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.5.0/backbone-min.js"></script>
</head>
<body>
<div id="app-container">
    <div id="top-pane">
        <div id="left-pane">
            <div id="editor"></div>
        </div>

        <div id="center-pane">
            <button id="submit-button" title="Submit and parse">
                ➜
            </button>
        </div>

        <div id="right-pane">
            <div id="rendered-output"></div>
        </div>
    </div>

    <div id="bottom-pane">
        <h3>Intermediate Markdown</h3>
        <pre><code id="markdown-output" class="codehilite"></code></pre>
    </div>
</div>

<script>
    window.INITIAL_MARKDOWN = {{ example_markdown|tojson }};
</script>

<script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

---

## `static/css/style.css`

```css
body {
    margin: 0;
    font-family: sans-serif;
    background: #f5f5f5;
}

#app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

#top-pane {
    display: flex;
    flex: 1 1 auto;
    overflow: hidden;
}

#left-pane,
#right-pane {
    flex: 1 1 50%;
    padding: 10px;
    box-sizing: border-box;
    overflow: auto;
    background: #ffffff;
}

#center-pane {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    background: #f0f0f0;
    border-left: 1px solid #ddd;
    border-right: 1px solid #ddd;
}

#submit-button {
    font-size: 24px;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 50%;
    border: none;
    background: #4a90e2;
    color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

#submit-button:hover {
    background: #357ab8;
}

#editor {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    min-height: 200px;
}

#rendered-output {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    min-height: 200px;
    background: #fafafa;
}

#bottom-pane {
    padding: 10px;
    box-sizing: border-box;
    background: #f9f9f9;
    border-top: 1px solid #ddd;
    max-height: 40vh;
    overflow: auto;
}

#markdown-output {
    display: block;
    white-space: pre-wrap;
    word-wrap: break-word;
}
```

---

## `static/js/app.js`

```javascript
(function () {
    const { Editor } = window['@tiptap/core'];
    const StarterKit = window['@tiptap/starter-kit'].StarterKit;

    function htmlToMarkdown(html) {
        return html
            .replace(/<strong>(.*?)<\/strong>/g, '**$1**')
            .replace(/<em>(.*?)<\/em>/g, '*$1*')
            .replace(/<code>(.*?)<\/code>/g, '`$1`')
            .replace(/<h1>(.*?)<\/h1>/g, '# $1\n\n')
            .replace(/<h2>(.*?)<\/h2>/g, '## $1\n\n')
            .replace(/<h3>(.*?)<\/h3>/g, '### $1\n\n')
            .replace(/<p>(.*?)<\/p>/g, '$1\n\n')
            .replace(/<br\s*\/?>/g, '\n')
            .trim();
    }

    const AppView = Backbone.View.extend({
        el: '#app-container',

        events: {
            'click #submit-button': 'onSubmit'
        },

        initialize: function () {
            this.editor = new Editor({
                element: document.querySelector('#editor'),
                extensions: [StarterKit],
                content: window.INITIAL_MARKDOWN || ''
            });

            this.localRender();
        },

        getMarkdown: function () {
            const html = this.editor.getHTML();
            return htmlToMarkdown(html);
        },

        setMarkdown: function (markdown) {
            this.editor.commands.setContent(markdown);
        },

        onSubmit: function () {
            const html = this.editor.getHTML();
            const markdown = this.getMarkdown();

            const payload = { html: html, markdown: markdown };

            this.editor.commands.clearContent();

            const self = this;

            $.ajax({
                url: '/parse',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(payload),
                success: function (response) {
                    self.updateRightPane(response.html);
                    self.updateMarkdownPane(response.highlighted_markdown);
                    self.syncHeights();
                }
            });
        },

        localRender: function () {
            const markdown = this.getMarkdown();
            $('#markdown-output').text(markdown);
            this.syncHeights();
        },

        updateRightPane: function (html) {
            $('#rendered-output').html(html);
        },

        updateMarkdownPane: function (highlighted) {
            $('#markdown-output').html(highlighted);
        },

        syncHeights: function () {
            const left = document.getElementById('left-pane');
            const right = document.getElementById('right-pane');

            const leftHeight = left.scrollHeight;
            const rightHeight = right.scrollHeight;
            const maxHeight = Math.max(leftHeight, rightHeight);

            left.style.height = maxHeight + 'px';
            right.style.height = maxHeight + 'px';
        }
    });

    $(function () {
        new AppView();
    });
})();
```
