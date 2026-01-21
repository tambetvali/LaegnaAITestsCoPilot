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
