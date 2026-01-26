# Preface

Study how your basic model understands itself.
- Keeping the API structure of recursive realignment of the past Q&A cards of this conversation,
  make sure the "message", along with it's attribution into "role" and "content" tags identifying
  the same entity; make sure both your AI platform, such as Ollama or LiteLLM, and the model itself
  you have carefully chosen, mostly from Hugging Face: best platforms have their built-in ways to
  access Hugging Face models, or their own select few which are of fit architecture.
  - Keep the role-content structure if possible, or parse it to given format.
- For LitGPT, you need to implement message templates and follow it's internal format; it's meant
  for fine-tuning - sorrily you ain't the end user, you got the capability to directly access
  some form of basic tags, which should be standard interpretation, but not the only one:
  - You are meant to serve different formats of cards to access the realignment into it's training
    on "millions of examples with custom formats to distinct messages, system messages, special
    commands etc.
  - This is almost sure your litgpt model won't initially understand the basic syntax.

Things you need to add:
- They are basically configuration items to your access engines; you can switch between open source engines such as Jan, GPT4All and lmstudio.ai:
  - Jan is basically what we classically imagine as a "chattlebot": you choose small models, in current versions they have no library collection but hopefully
    it will be fast and lightweight; but it kind of supports session memory. Try to optimize it for speed: use small models, remove overhead, in future
    perhaps you don't need the document collection or you can utilize a small one to benefit from it's responsive display and optimization tags. Those are
    not so visible in exponential growth of memory and hardware use or large models, altough you can use one and try to optimize it for different goal.
  - GPT4All is able to serve one model, but I think you cannot locally use it then: I think it's basically not fine-tuned to be a server. It has document
    collections, but in current version the collections can become corrupt - you have to remove them manually and recreate.
  - Lm-studio, at first sight, is very similar chatting platform: looking closer, you can see it's optimized to provide you document embeddings, which act
    as document or document and content (pages are hashed or something like this) index; this needs some administrative abilities for configuration, or
    a hacker friend to set it up for you: perhaps a child of the neighbour. It needs a few configuration options, but might evolve into small logical puzzle
    to resolve with some study in, sometimes somewhat technical, documents. Basically you won't need much more than what you need to set up index on your
    filesystem - just turn it on -, or SQL table - also identify the type. This is the graphical interface also able to serve chat models, but command line
    tool Ollama might be better of it: it removes some graphical overhead and works hiddenly, so you won't notice how it works when you turn your computer
    on and off. It's registered as standard service: with LMStudio, it seems simpler that you turn on your graphical application, then it runs the installed
    servers and you can access them from other windows. It's ability to be invisible is not so sure and simple, as well as stability is often having causalities
    from graphical interfaces: still, it's the best you can get if you want an open source graphical user interface to extend the experience from Jan and GPT4All,
    linearly.

Each is more or less what the name says: LM Studio is rather an AI Studio; GPT4All makes GPT access for everybody; and Jan is, well, a common male name: if you want
to chat with a common, somewhat erudit man who gets stuck as there are more topics to resolve at the same time; this kind of bot appears to be a practical man,
who has studied a lots of dictionaries, but cannot much understand your personal matters above specific needs you can carefully state in a few sentences. But well,
start a new conversation and ask who was the first president of America: and hope it does not start to hallucinate if your matter is too decent.


    
