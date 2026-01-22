# Things you might need to do later:

- Add complete support for HTML code which is parsed into Markdown
  - Currently, it supports all "human" markdown, like bold and italic
  - Advanced Markdown like code blocks is not directly supported, but rendered properly into Markdown html blocks
    - If AI is given this less-than Markdown as input, it will parse the code blocks and treat it as normal input
    - If it is converted back to HTML, it works
  - I could not treat this problem, because
    - I would not be sure if you get all the headers in simple form
    - Either one can parse HTML by
      - search-and-replace,
      - parsing with tools like DatSu or external grammar,
      - bring compability between their WYSIWYG editor output and mistune's input by themes or options of both
    - I am not sure whether an user wants to switch the editor, allow their own set of tags, or disable the code blocks entirely.
      - This is heavily dependent on HTML export styles and themes and exact syntax, so I considered my "fix" an overhead.
     
**Markdown HTML**
- HTML is supported inside Markdown, and AI can use this as input.
- AI output is supported, whether they use code blocks as inner html, or whether they do them properly.
- So I hardly conceive a problem, rather I want to know what is the function of simple code user can understand and use directly, and paste to their CoPilot as whole.

- Add edges to WYSIWYG input box
  - Additional CSS and it's JS rendering would make my code more complicated, and I am not sure in your graphical design choices.
  - Empty textbox could get lines above and below to identify as input box.
    - For example, if first line is empty, the line could appear above and on right side of input box.
    - For example, if last line is empty, the line could appear below and on left side of input box.
  - The input box, also, could have brighter background color than surrounding area.
  - Anyway, I cannot confirm that being blank and white could not be a textbox's default and expected behaviour for you to implement your own functionality with assistance of an AI.

- Add buttons for rich text formatting
  - Currently, you can use Ctrl+B for bold, Ctrl+I for italic, and any built-in keyboard shortcut for formatting.
  - Adding buttons and selections depends on your preferrations on how the user can format their input, and you can even disable keyboard shortcut or parse out certain things.
  - I am sure the few lines to enable this graphics would first keep you distracted from having a minimalist design, second my own customization of your input box would possibly not enable your own own design solutions in minimalist environment.

By this minimalist choice, I only make sure that in the end of getting this code snippet decoded, you have:
- Minimal set of code lines, design syntax and configurations to get exactly the desired functionality.
- A way to enter your formatted text into Markdown system.
- A way to get it's answer back.
- A minimalist Flask environment which can be easily connected to an AI.

I avoided such kind of complexities:
- Giving you more than one of every graphical element, such as emulating the whole conversation.
  - You can build very different features, from an AI giving you one answer such as translation to a conversation or branched conversation.
  - Each critical feature is shown only once, for example it would be interesting feature to edit and fix the output box otherwise.
  - In the end of lesson, you have ensured that you can work with graphical editor, parse the output, remain HTML-native on client-side and Markdown-native in conversations with an AI; also according to best conventions such as proper file tree and Model-View-Controller interface.
  - There is only one Flask entry point: "/" (root), but basically to have multiple elements in your UI and add the nodes for interaction: from this entry point, you can learn, how the entry points work.
 
For basic users, implementing one input box and one ouput with one entry node might be all they need and they can achieve this by AI programming:
- To append hidden task automatically each time they enter the text, which gives and order to an AI such as "translate this text to sweden" or "turn it into 10 pairs of Q&A". They can work on this manually.

*For those who apply advanced architecture, the basic demonstration gives them all the technical overview to do this:*
- This part of programming is kind of "management", getting the file system, server, version handling and basic user interaction to work; for example box below can be used as a debugger.
- The rest of the code is something from an other world:
  - It is standard, generic python code which is an *abstract* programming, where you work on variables, classes and features in linear fashion.
  - It can be understood on functional basis, such as taking user input, processing it with an AI, and sending the output.
  - It is not setup of environment and basic things a framework would do for you, for example tackling the signals and defining what "input" and "output" are in abstract form.
  - Generally, in any new environment, I always want to reach point where I can write linear code without tackling into project management: in this way, you can add your single feature as-is and do not run into additional configuration, set-up and search for libraries.
  - I can ensure your libraries and setting works with an AI.

Maybe I was confusing, but note this:
- Normally, there is a "code" in it's abstract form, where you *already have* a very basic thing: I/O, compiler or interpreter, fast way to include base libraries.
- Past that point, you are enable to implement your specific features, which can be a very complex or simple thing, but it's definitely ***logical*** - that you need markdown parser and html processing for AI conversation, kind of, is not trivially logical or something what would associate in very abstract, scientific terms with this concept: what does, now, is to send this input to AI and process the result, which is perfectly what you expect from AI workflow in abstract terms.

# Outside the terms of this code snippet

This, indeed, is not my goal to *not provide the abstract code*:
- I will handle several different methods of Markdown processing, such as code block parsing, otherwhere.
- I will enable more advanced uses of this editor and implement the AI-interaction.
- I am sure when more advanced users will already catch many of those things from air and love based on this code snippet; more basic, but active users will get things to real use:
  - You can get more things done based on my future snippets, but you are already ahead of the competition if you do not wait too long.
  - We will slowly work to get the general public involved by providing more advanced or other areas of code, but in agile development you do not only have the basic code now, but also the basic information for your personal development.
  - The agile users of this code, indeed, are already enabled to create their own products and understand the place of each library.
