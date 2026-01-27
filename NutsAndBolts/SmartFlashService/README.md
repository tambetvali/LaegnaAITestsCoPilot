# Introduction

## A Gentle Introduction to Flashcard‑Based Training and Smart Services

Modern AI systems learn in ways that feel surprisingly familiar. When you train a model like LitGPT, you’re essentially giving it a deck of flashcards. Each card has a **front** (a question or prompt) and a **back** (the correct answer). The model sees the front, tries to guess the back, and then gets immediate feedback. Over time, it becomes better at predicting the right answer—just like a student who reviews cards every day.

This introduction explains how a **smart flashcard service** works, how formats like **JSON**, **JSONL**, and **Anki** fit into the picture, and why this approach is useful for everyone—from casual users to IT managers and programmers.

---

## Why Flashcards Matter for AI Training

Flashcards aren’t just a study tool for humans—they’re a universal teaching pattern:

- **Front → Back**: The model learns to map an input to an output.
- **Repetition**: The model improves by seeing many examples.
- **Correction**: The model adjusts itself when it gets something wrong.
- **Structure**: Well‑organized cards produce better learning.

This is why so many fine‑tuning datasets look like flashcards, even when stored in technical formats.

---

## JSON and JSONL: The Two Main Storage Formats

Even if you’ve never heard of JSON or JSONL, you’ve used software that relies on them. They’re simple text formats for storing structured information.

### JSON (JavaScript Object Notation)

- Human‑readable  
- One big structure (like a box full of cards)  
- Must be complete before it can be read  

### JSONL (JSON Lines)

- One JSON object **per line**  
- Perfect for streaming  
- Can be read while still downloading  
- Ideal for large datasets and AI training  

**Think of JSON as a book and JSONL as a stack of loose cards.**  
You can flip through JSONL one card at a time without waiting for the whole stack.

---

## Why JSONL Becomes a “Service”

LitGPT treats JSONL in a special way: it reads **one line at a time**, without loading the whole file. This means:

- A JSONL file can be local or remote  
- It can be a real file or a server generating lines on the fly  
- It can be infinite  
- It can mix multiple sources  

This turns JSONL into a **protocol**, not just a file format. Anything that produces one JSON object per line can act as a flashcard service.

---

## Anki: The Human‑Friendly Side of the Workflow

Anki is a popular flashcard app used by students, doctors, engineers, and language learners. It stores cards in a **SQLite database**, which is a simple file‑based database. You don’t need to understand SQL to use Anki, but if you *do* know SQL, you can inspect and manipulate your cards directly.

### Why Anki Matters Here

- Humans can create and test cards visually  
- AI‑generated cards can be imported into Anki  
- Anki decks can be exported into JSON/JSONL  
- You can evaluate AI‑generated cards by studying them yourself  
- You can reorganize or label cards before training the model  

Anki becomes the **bridge** between human pedagogy and machine learning.

---

## The Preprocessing Stage: Gathering Cards from Everywhere

A typical preprocessing script collects flashcards from many sources:

- JSON files  
- JSONL files  
- Anki collections  
- CSV files  
- Synthetic generators (e.g., math problems)  
- Custom or hypothetical formats  

Each reader class:

- Reads one card at a time  
- Adds metadata such as **category**, **source**, or **difficulty**  
- Normalizes the card into a standard structure  

All cards are then combined into a **unified Anki deck** or a **unified JSONL dataset**.

This is where administrators and IT managers often get involved: organizing data, labeling categories, and ensuring consistency.

---

## Conscious Processing: The Human Quality‑Control Phase

Before training the AI, a human should **test the deck**:

- Review cards in Anki  
- Check clarity and correctness  
- Identify weak or confusing cards  
- Decide which categories should appear more or less often  

This is where human teaching instincts shine. A person who understands the subject can:

- Spot errors the AI would never notice  
- Improve phrasing  
- Adjust difficulty  
- Balance categories  
- Decide probability weights (e.g., “show math cards 10% of the time”)  

This step dramatically improves the quality of the final model.

---

## The Flashcard Service: A Smart JSONL Stream

Finally, a Flask‑based service can:

- Read from the Anki SQLite file  
- Choose cards based on category probabilities  
- Serve them as JSONL lines  
- Stream them indefinitely to LitGPT  

This service acts like a **live deck shuffler**:

- It picks a deck based on probability  
- Selects a random card  
- Converts it to JSON  
- Sends it to the AI  

Because it reads directly from SQLite, it doesn’t load the whole deck into memory. It only fetches what it needs, when it needs it.

---

## Why This Matters for Different Audiences

### For non‑technical users
- You can create cards visually in Anki  
- You can test AI‑generated cards yourself  
- You don’t need to understand JSON or SQL  

### For administrators
- You can manage datasets without deep programming  
- You can control categories and probabilities  
- You can ensure data quality before training  

### For IT managers
- The system is modular and maintainable  
- JSONL streaming is efficient and scalable  
- Anki provides a human‑friendly editing layer  

### For programmers
- You can extend the system with new readers  
- You can generate synthetic datasets  
- You can integrate with training pipelines  
- You can inspect and manipulate the SQLite database  

---

## Final Thoughts

This workflow—mixing human‑friendly tools like Anki with machine‑friendly formats like JSONL—creates a powerful, flexible, and understandable system for training AI models. It respects both sides of the equation:

- **Humans** curate, test, and improve the material  
- **Machines** learn from clean, structured flashcards  

The result is a training pipeline that is transparent, maintainable, and surprisingly intuitive, even for beginners.

# Building a smart service for LitGPT

## Standard terms

Here is a brief introduction to the standard terms, which are background into understanding Flashcard service: one which feeds flashcards to LitGPT or other fine-tuning
or training service of an AI.

### What is Flashcard?

A flashcard consists of two sides: the **front**, which presents a prompt or question, and the **back**, which contains the expected answer. This simple structure mirrors
how a language model processes information. During training or fine‑tuning, the model is repeatedly shown the “front” of many such cards and asked to predict the “back.”
Each time it guesses, the training system immediately reveals the correct answer, allowing the model to adjust its internal parameters and become slightly more accurate.
During inference, the model again sees only the “front” and produces its best guess for the “back.” If a user corrects the output, that correction can be fed back into a
future training or fine‑tuning cycle, reinforcing the desired pattern in much the same way a student benefits from being corrected while studying.

Many of the learning patterns humans experience also appear in these algorithms. Repetition strengthens associations, varied examples improve generalization, and timely
feedback accelerates mastery. Because of these parallels, human‑centered teaching strategies—clear prompts, structured examples, incremental difficulty, and corrective
guidance—translate surprisingly well into machine‑learning workflows. Thinking of training data as a carefully curated deck of flashcards helps emphasize that models,
like people, learn best when the material is organized, consistent, and pedagogically intentional.

### What is JSON: what is JSONL?

#### JSON

JSON is a lightweight text format for structured data, originally based on JavaScript’s object literal syntax. It emerged in the early 2000s as a simple, human‑readable
alternative to XML for exchanging information between browsers and servers. Although it began in the JavaScript world, JSON is now language‑independent and supported
almost everywhere, thanks to its minimal set of types—objects, arrays, strings, numbers, booleans, and null.

The name is commonly pronounced **“jay‑sahn”** or **“jay‑son.”** The second pronunciation often amuses developers because it sounds like a person’s name, which gives JSON
an oddly friendly, almost conversational feel despite being a data format.

#### JSONL

JSONL stands for **JSON Lines**, a format where each line of a file contains one complete JSON object. It is usually pronounced **“jay‑sahn‑ell”** or simply **“json lines.”** The idea is straightforward: instead of wrapping many objects inside a single JSON array, JSONL stores them one per line, making the file easy to stream, append to, and process incrementally.

In regular JSON, you might represent a list of items like this:

```json
[
  {"a": 1},
  {"b": 2},
  {"c": 3}
]
```

In JSONL, the same data appears as three separate lines, each containing one JSON object:

```json
{"a": 1}
{"b": 2}
{"c": 3}
```

This difference matters in practice. A JSON array must be read as one complete structure, with opening and closing brackets and commas between items. JSONL, by contrast,
treats each line as an independent record, which makes it ideal for large datasets, streaming over the network, or training machine‑learning models that read one example
at a time. It’s still JSON—just arranged in a way that’s friendlier for sequential processing.

## JSONL Service

For sake of simplicity, LitGPT resolves a tricky question:
- JSONL can be a standard file, either online or stored locally, and the training system can read it, and train.
- Exactly the same format specification might define a streaming server, in case both sides can do stream.

### How the JSON\[L\] cards read?

#### JSON and JSONL Flashcard Storage

JSON and JSONL flashcards both store small training examples built around a prompt (the “front” of the card) and an expected answer (the “back”). The required fields are
typically just two: one for the model’s input and one for the model’s target output. Optional fields—such as metadata, tags, difficulty, or source information—can be
included for organization or reference but are not required by most fine‑tuning systems.

#### JSON vs. JSONL (Short Explanation)

A JSON dataset places many flashcards inside a single array, while JSONL stores one flashcard per line. JSON is a single structured document; JSONL is a stream of
independent records. JSONL is generally preferred for machine‑learning pipelines because it can be read incrementally and scales better for large datasets.

#### Fields Used Directly for Fine‑Tuning

Fine‑tuning systems typically consume only the fields that correspond to the model’s input and expected output—commonly named `instruction` and `output`, or `prompt`
and `response`. These names are not canonical; they can be changed as long as the fine‑tuning script knows which fields to read. All other fields are ignored unless
explicitly incorporated into preprocessing.

#### Fine‑Tuning Tool Usage

Tool usage can be fine‑tuned by providing structured examples that show when and how the model should call a tool, how to format the call, and how to respond after
receiving tool output. Many tools follow similar patterns: a user request, a model‑initiated tool call, the tool’s result, and a final model answer. With enough
examples, models can learn to use tools intelligently and respond appropriately to typical situations.

### What is the JSONL flashcard service?

#### JSON and JSONL as a Service

Although JSONL is technically just a file format, LitGPT’s streaming‑friendly reader allows it to behave like a service. Because each line is a complete JSON object, LitGPT can treat any source—local file, remote URL, pipe, or network stream—as a continuous provider of flashcards. JSON, while not naturally stream‑oriented, can also be consumed in a similar way through a streaming parser, though this is more of a workaround than a native fit.

#### JSONL Service Attributes

LitGPT interprets JSONL in a way that naturally supports streaming:

- Reads line by line  
- Each line is parsed independently  
- No need for a final closing bracket  
- Can stream from remote URLs  
- Memory‑efficient  
- Most common format for fine‑tuning  

Because each line is self‑contained, LitGPT can begin training immediately, even if the file is still being downloaded or generated dynamically.

#### JSON Service Hack

JSON arrays were not designed for streaming, but LitGPT can still process them using a streaming JSON parser:

- Uses a streaming JSON parser  
- Does not load the entire array into memory  
- Reads one object at a time  
- Requires valid JSON structure, but:  
  - It does not wait for the entire file to finish  
  - It yields each object as soon as it is parsed  

This creates a small paradox: LitGPT must assume the JSON file will eventually be valid, even though it begins consuming items before the final closing bracket exists. It treats the file as complete while reading it as a stream, which makes JSON‑as‑a‑service feel like a clever workaround.

#### A Unified, Philosophical Reading Model

LitGPT’s dataset reader is agnostic about the source. It can read:

- local files  
- remote files  
- pipes  
- network streams  
- generators  
- proxies  
- infinite sources  

It follows one principle:

**It reads only what it needs for the next batch.**

The training loop works like this:

- DataLoader requests a batch  
- Dataset iterator yields the next N samples  
- LitGPT tokenizes them  
- Training step runs  
- Repeat  

At no point does it load the entire dataset into memory. This is why both JSONL and streaming JSON work seamlessly.

#### What a Streaming Server Is

A streaming server is any system that produces a sequence of JSONL‑compatible objects over time. It does not need to know the total dataset size and does not need to finish. It can be finite or infinite.

A streaming server can:

- **Proxy another server**: forward, filter, or shuffle upstream cards  
- **Read from files**: emit cards sequentially or randomly  
- **Generate cards dynamically**: synthetic or curriculum‑based  
- **Mix multiple sources**: combine generated, proxied, and file‑based cards  

All of these behave identically to LitGPT because the model only needs a stream of JSON objects.

#### Technical Meaning and Efficiency

A JSONL‑over‑HTTP stream and a traditional streaming server behave almost the same from LitGPT’s perspective. JSONL is efficient because:

- each line is a complete unit  
- no buffering of the entire dataset is required  
- the parser can operate incrementally  

This makes JSONL ideal for large datasets, distributed training, online learning, and infinite data generation.

#### Hosting a Local Streaming Service

Yes, you can host a service such as `localhost:SMARTFLASHPORT` that emits JSONL objects indefinitely. As long as each line is valid JSON, LitGPT will treat it as a valid dataset source and train on it as the data arrives.

## Tech solutions

Here are two solutions for this.

### Flask‑Based JSONL Router (Design Specification)

#### Introduction

This router acts as a unified streaming endpoint that merges multiple JSONL sources—local files or remote URLs—into a single probabilistic stream. Each source is assigned a weight, and the router selects which source to read from based on these probabilities. The router never downloads or buffers entire files; instead, it streams line‑by‑line and only requests new data when the previous items have been consumed.

#### Source List and Probability Vector

The router receives a list of sources. Each source entry contains:

- A URL or local filename  
- A probability weight (e.g., `1.4`)  

From these weights, the router constructs a cumulative probability vector. For example:

- Source A: weight `1.4`  
- Source B: weight `4.2`  

The cumulative ranges become:

- A: `[0.0, 1.4)`  
- B: `[1.4, 5.6)`  

For each card request, the router generates a random number in `[0, total_weight)` and selects the source whose range contains the number.

#### Streaming JSONL Behavior

The router supports only JSONL, not JSON arrays. JSONL is ideal because:

- Each line is a complete JSON object  
- Lines can be streamed independently  
- No closing bracket is required  
- Remote sources can be consumed incrementally  
- Memory usage stays low  

The router does not parse JSON beyond what is necessary to ensure that line boundaries are respected. Escaped newline characters inside JSON strings must be preserved, not treated as actual line breaks.

#### Controlled Fetching and Backpressure

To avoid downloading entire files, the router uses a controlled‑pull model:

- It reads only one line at a time from the selected source  
- It does not request the next line until the previous one has been delivered  
- Remote sources are streamed using chunked HTTP or range‑based reads  
- Local files are read lazily using file iterators  

This ensures minimal memory usage and prevents unnecessary network consumption.

#### Streaming Server Behavior

The router behaves like a streaming server:

- It can proxy upstream JSONL streams  
- It can interleave multiple sources  
- It can handle infinite sources (e.g., generators)  
- It can mix generated and file‑based data  
- It can shuffle or filter lines before sending them  

The router’s output is a continuous JSONL stream suitable for training systems that expect line‑delimited records.

#### Implementation Outline

A typical implementation includes:

- A Flask route that returns a streaming response  
- A probability selector that chooses the next source  
- A set of iterators, one per source  
- A mechanism to open remote URLs as streaming readers  
- A loop that yields one JSONL line at a time  
- Proper handling of network timeouts and reconnections  
- Preservation of line boundaries and escaped characters  

The router does not parse JSON objects; it simply forwards each line as raw text.

#### Hosting and Usage

The router can be hosted locally, for example at:

```
http://localhost:SMARTFLASHPORT/stream
```

Clients can connect to this endpoint and receive an indefinite JSONL stream. Training systems such as LitGPT can consume this stream directly, treating it as a live dataset.

### Flask‑Based SmartCardService JSONL Router

#### Overview

The code below implements a `SmartCardService` class and a Flask app that exposes a `/stream` endpoint. The service can:

- Read JSONL lines from:
  - local files
  - remote HTTP(S) URLs
- Combine multiple sources with probabilities
- For each `read()` call, select a source according to its weight and return the next JSONL line from that source
- Stream lines without loading entire files into memory

Each source is defined as a dictionary with either a `filename` or an `address` (URL), plus a `probability`.

#### Full Code

```python
import random
import requests
from flask import Flask, Response

app = Flask(__name__)


class SingleSourceReader:
    """
    Reads JSONL lines from a single source:
    - local file (filename)
    - remote HTTP(S) URL (address)
    """

    def __init__(self, filename=None, address=None):
        if not filename and not address:
            raise ValueError("Either filename or address must be provided")

        self.filename = filename
        self.address = address
        self._iterator = None
        self._open_source()

    def _open_source(self):
        if self.filename:
            # Local file, opened lazily as an iterator
            f = open(self.filename, "r", encoding="utf-8")
            self._iterator = f
        else:
            # Remote URL, streamed with requests
            resp = requests.get(self.address, stream=True)
            resp.raise_for_status()
            # iter_lines() yields lines without loading the whole response
            self._iterator = resp.iter_lines(decode_unicode=True)

    def read(self):
        """
        Return the next JSONL line as a string, or None if the source is exhausted.
        """
        if self._iterator is None:
            return None

        try:
            line = next(self._iterator)
        except StopIteration:
            return None

        # For local files, line is already a string.
        # For remote streams, iter_lines(decode_unicode=True) returns strings.
        if line is None:
            return None

        # Ensure we return a clean line without trailing newlines
        return line.rstrip("\r\n")


class SmartCardService:
    """
    A service that can:
    - Wrap a single source (file or URL), or
    - Wrap multiple sources with probabilities and route read() calls among them.
    """

    def __init__(self, sources):
        """
        sources: list of dicts, each like:
            {
                "filename": "/path/to/file.jsonl",  # optional
                "address": "https://example.com/data.jsonl",  # optional
                "probability": 1.4
            }

        At least one of "filename" or "address" must be present per source.
        """
        if not sources:
            raise ValueError("At least one source must be provided")

        self.sources = sources
        self._readers = []
        self._weights = []
        self._total_weight = 0.0

        self._initialize_readers()

    def _initialize_readers(self):
        for src in self.sources:
            filename = src.get("filename")
            address = src.get("address")
            prob = float(src.get("probability", 1.0))

            if prob <= 0:
                continue

            reader = SingleSourceReader(filename=filename, address=address)
            self._readers.append(reader)
            self._weights.append(prob)

        if not self._readers:
            raise ValueError("No valid sources with positive probability")

        self._total_weight = sum(self._weights)

    def _choose_reader(self):
        """
        Choose a reader according to the probability weights.
        """
        r = random.uniform(0, self._total_weight)
        cumulative = 0.0
        for reader, weight in zip(self._readers, self._weights):
            cumulative += weight
            if r <= cumulative:
                return reader
        # Fallback (should not happen due to floating point, but safe)
        return self._readers[-1]

    def read(self):
        """
        Return the next JSONL line from one of the sources, or None if all are exhausted.
        """
        if not self._readers:
            return None

        # We may need to try multiple readers if some are exhausted
        attempts = len(self._readers)
        while attempts > 0:
            reader = self._choose_reader()
            line = reader.read()
            if line is not None:
                return line
            else:
                # This reader is exhausted; remove it and adjust weights
                idx = self._readers.index(reader)
                self._total_weight -= self._weights[idx]
                del self._readers[idx]
                del self._weights[idx]

                if not self._readers:
                    return None

            attempts -= 1

        return None


# Example configuration: mix local and remote JSONL sources
SOURCES_CONFIG = [
    {
        "filename": "data/local1.jsonl",
        "probability": 1.4,
    },
    {
        "address": "https://example.com/remote_stream.jsonl",
        "probability": 4.2,
    },
]

smart_service = SmartCardService(SOURCES_CONFIG)


def stream_generator():
    """
    Generator that yields JSONL lines from SmartCardService as a streaming response.
    """
    while True:
        line = smart_service.read()
        if line is None:
            break
        # Ensure each line is terminated with a newline for JSONL
        yield line + "\n"


@app.route("/stream")
def stream():
    """
    Flask endpoint that streams JSONL lines indefinitely (or until sources are exhausted).
    """
    return Response(stream_generator(), mimetype="application/jsonl")


if __name__ == "__main__":
    # Run the Flask app, e.g., at localhost:5000/stream
    app.run(host="0.0.0.0", port=5000, debug=False)
```

### Flashcard Sources as Services

A streaming flashcard service does not need to rely solely on static files. Any mechanism capable of producing one JSONL‑compatible record at a time can act as a source. This includes mathematical generators, Anki note collections, and ordinary JSONL files. The unifying idea is simple: each source implements a `read()` method that returns the next flashcard as a single JSONL line, without loading the entire dataset into memory.

#### Flashcards Generated by a Mathematical Function

One powerful approach is to generate flashcards dynamically from a mathematical function. Instead of reading from a file, the service produces new cards on demand. For example, a simple arithmetic generator can create an infinite stream of addition problems:

- It picks two random integers.
- It constructs a natural‑language question such as:  
  **“Sum 7 and 12.”**
- It constructs the corresponding answer:  
  **“7 and 12 summed give 19.”**
- It returns this pair as a JSONL object.

Because the generator never exhausts its source, it can stream indefinitely. This is ideal for curriculum‑style training, synthetic data generation, or reinforcing specific skills. The service behaves exactly like a file‑based JSONL source, but the data is produced algorithmically rather than stored.

#### Flashcards Read from an Anki File

Another useful source is an Anki note collection. Anki’s plain‑text export format lists one note per line, with fields separated by tabs. A streaming reader can open this file and return one line at a time, converting each into a JSONL flashcard. Two modes are possible:

- **Ordered mode**: read the file sequentially, one note per request.
- **Random mode**: pick a random line each time, without loading the entire file.

In both cases, the service avoids reading the full file into memory. It simply opens the file, seeks or iterates as needed, and emits one flashcard per request. This allows large decks to be used as training sources without preprocessing or conversion.

#### Flashcards from an Existing JSONL File

The simplest source is a standard JSONL file. Because JSONL is already line‑delimited, the service can stream it directly:

- Open the file.
- Read one line at a time.
- Return each line as a flashcard.

This is functionally equivalent to serving the file itself, but wrapped in a consistent interface so it can be combined with other sources. JSONL is ideal for large datasets because it supports incremental reading, remote streaming, and efficient memory usage.

#### A Unified Model for All Sources

Despite their differences, all three source types follow the same pattern:

- They produce one JSONL object per request.
- They do not load the entire dataset.
- They can be infinite or finite.
- They can be mixed with other sources using probability weights.

This unified design allows a streaming service to combine mathematical generators, Anki decks, and JSONL files into a single probabilistic stream. Training systems can then consume this stream as if it were a single dataset, even though it may be composed of multiple heterogeneous sources.

### Flashcard Source Examples + Flask Service

This chapter contains four complete examples:

1. **MathFlashcardSource** — infinite synthetic math flashcards  
2. **AnkiFlashcardSource** — streams cards from an Anki TSV export  
3. **JSONLFileSource** — streams an existing JSONL file  
4. **FlaskFlashcardService** — exposes any of the above as a streaming JSONL service  

Each source implements:

```python
read() -> str | None
```

---

#### 1. Mathematical Flashcard Generator (infinite)

```python
import random
import json

class MathFlashcardSource:
    """
    Generates infinite addition flashcards.
    Each call to read() returns one JSONL line.
    """

    def __init__(self, min_val=1, max_val=100):
        self.min_val = min_val
        self.max_val = max_val

    def read(self):
        a = random.randint(self.min_val, self.max_val)
        b = random.randint(self.min_val, self.max_val)

        question = f"Sum {a} and {b}."
        answer = f"{a} and {b} summed give {a + b}."

        obj = {
            "instruction": question,
            "output": answer
        }

        return json.dumps(obj)
```

---

#### 2. Anki File Reader (ordered or random)

```python
import json
import random

class AnkiFlashcardSource:
    """
    Reads an Anki TSV export (one note per line, fields separated by tabs).
    Converts each line into a JSONL flashcard.
    Supports ordered or random access.
    """

    def __init__(self, filename, random_mode=False):
        self.filename = filename
        self.random_mode = random_mode
        self._file = None
        self._lines = None

        if self.random_mode:
            # Load lines into memory for random access
            with open(self.filename, "r", encoding="utf-8") as f:
                self._lines = f.readlines()
        else:
            # Ordered mode: open file as iterator
            self._file = open(self.filename, "r", encoding="utf-8")

    def read(self):
        if self.random_mode:
            if not self._lines:
                return None
            line = random.choice(self._lines).rstrip("\n")
        else:
            line = self._file.readline()
            if not line:
                return None
            line = line.rstrip("\n")

        fields = line.split("\t")
        if len(fields) < 2:
            return None

        front, back = fields[0], fields[1]

        obj = {
            "instruction": front,
            "output": back
        }

        return json.dumps(obj)
```

---

#### 3. JSONL File Reader (direct streaming)

```python
class JSONLFileSource:
    """
    Streams an existing JSONL file line-by-line.
    Does not load the whole file.
    """

    def __init__(self, filename):
        self.filename = filename
        self._file = open(self.filename, "r", encoding="utf-8")

    def read(self):
        line = self._file.readline()
        if not line:
            return None
        return line.rstrip("\n")
```

---

#### 4. Flask Service That Serves Any Flashcard Source

This service:

- Accepts a **source type** via configuration  
- Instantiates the appropriate source class  
- Streams JSONL indefinitely (or until the source ends)  
- Serves at `/` (root endpoint)  

```python
from flask import Flask, Response

# Import the three source classes
# (Assume they are in the same file or imported properly)
# MathFlashcardSource
# AnkiFlashcardSource
# JSONLFileSource

app = Flask(__name__)

def create_source():
    """
    Change this configuration to select which source to serve.
    """

    # Example 1: math generator
    # return MathFlashcardSource(min_val=1, max_val=50)

    # Example 2: Anki TSV file (ordered)
    # return AnkiFlashcardSource("mydeck.txt", random_mode=False)

    # Example 3: Anki TSV file (random)
    # return AnkiFlashcardSource("mydeck.txt", random_mode=True)

    # Example 4: JSONL file
    return JSONLFileSource("dataset.jsonl")


source = create_source()


def stream_generator():
    """
    Yields JSONL lines from the selected source.
    """
    while True:
        line = source.read()
        if line is None:
            break
        yield line + "\n"


@app.route("/")
def root_stream():
    """
    Root endpoint: streams flashcards as JSONL.
    """
    return Response(stream_generator(), mimetype="application/jsonl")


if __name__ == "__main__":
    # Example: run at http://localhost:5000/
    app.run(host="0.0.0.0", port=5000, debug=False)
```

---

### Summary

You now have:

| Example | Description |
|---------|-------------|
| **MathFlashcardSource** | Infinite synthetic math flashcards |
| **AnkiFlashcardSource** | Reads TSV export, ordered or random |
| **JSONLFileSource** | Direct JSONL streaming |
| **FlaskFlashcardService** | Serves any of the above at `/` |

This gives you a complete, modular flashcard streaming system that can plug into your probabilistic router or be used standalone.

## Understanding Anki in Human Terms

Anki is a study‑card system built around a simple idea: people remember better when they review information in small, spaced‑out sessions. Although its internal storage uses a database, the parts that matter for most users—and for integrating with AI‑generated flashcards—are easy to understand in everyday terms.

### Creating and Organizing Cards Across Operating Systems

On any major operating system—Windows, macOS, Linux, Android, or iOS—the human workflow looks roughly the same. A learner creates study cards using Anki’s graphical editor or any external tool they prefer. Some people design cards in image editors, others write them directly in Anki’s text fields, and many mix text, images, and formatting. These cards are then grouped into collections or decks, which act like folders of related material. The user can rearrange, tag, or reorganize them at any time, building a personal structure that reflects how they think about the subject.

### Playing Through Cards in a Graphical Test Session

Once cards are created, the learner uses Anki’s review mode. The interface shows the front of a card—usually a question, prompt, or cue—and waits for the learner to recall the answer. When the learner reveals the back, they judge how well they remembered it. Anki uses this feedback to schedule the next review. This process feels like a conversation with one’s own memory: the system adapts to what is easy or difficult, and the learner gradually builds long‑term retention.

### Integrating AI‑Generated Cards

Modern workflows often involve AI‑generated flashcards. These may arrive in different formats:

- native Anki text exports  
- JSON or JSONL files  
- structured lists that need conversion  

The learner imports or converts these into Anki, mixing them with their own handmade cards. This hybrid approach allows them to combine personal insight with machine‑generated breadth. The human still curates the material: they check whether the AI’s questions make sense, whether the answers are correct, and whether the phrasing matches their learning style.

### Using Cards to Evaluate AI Learning

A learner can also use these cards to evaluate how well an AI model is learning during fine‑tuning. They configure the system to produce statistical question‑and‑answer pairs and then play through them as if they were studying themselves. Their own experience becomes a reference point: if they find the cards coherent, well‑structured, and pedagogically sound, they can infer that the AI is internalizing the patterns correctly. If the cards feel confusing or poorly ordered, that signals the model may need better examples or clearer structure.

### Human Pedagogy as a Fine‑Tuning Advantage

A person’s natural teaching instincts—clarity, progression, emphasis, and structure—translate surprisingly well into fine‑tuning workflows. By analyzing the cards, their order, and how they are used, a learner can shape the training data in a way that mirrors good teaching practice. This makes the resulting model more reliable, because the human’s domain knowledge and pedagogical sense act as a filter. In this way, the learner’s own study habits become a tool for improving the AI’s learning process.

## Understanding Anki’s Technical Foundations

### What Anki Is and How It Fits Into the Larger Context

Anki is a spaced‑repetition flashcard system designed to help humans learn efficiently by reviewing information at optimally timed intervals. In the context of the previous article parts—where JSON, JSONL, streaming services, and AI‑generated flashcards were discussed—Anki represents the **human‑facing end** of the workflow. JSON and JSONL are machine‑friendly formats used for generating, storing, and streaming flashcards, while Anki is the environment where those flashcards become part of a learner’s daily study routine.  

JSON/JSONL datasets can be converted into Anki decks, and Anki decks can be exported into formats that AI systems can learn from. This makes Anki a bridge between human pedagogy and machine‑driven training pipelines.

---

### SQLite File Format in Anki

Anki stores its entire collection in a single SQLite database file named `collection.anki2`. SQLite is a compact, file‑based relational database engine. It contains tables for notes, cards, review logs, deck configurations, and global settings. The structure is predictable and readable for anyone familiar with SQL.

### Extending the Schema Safely

SQLite allows arbitrary schema changes, but Anki’s application logic expects specific tables and columns.  
- **Adding new tables is safe**—Anki ignores tables it doesn’t recognize.  
- **Adding columns to existing tables is risky**, because Anki’s code may not expect them.  

If you want to add an AI‑driven scheduling system, the recommended approach is:
- Create **your own tables** for AI metadata.  
- Map your scheduling decisions onto Anki’s expected fields (e.g., due date, interval) without altering the core schema.  

This preserves compatibility with Anki’s GUI, add‑ons, and syncing.

### Organizing Cards with SQL

Because the database is SQLite, users can query and update it with standard SQL tools. This allows them to reorganize decks, update card content, extract statistics, or run custom tests. The schema is straightforward:
- `notes` stores card text  
- `cards` stores scheduling data  
- `revlog` stores review history  

A SQL‑confident person will find the structure readable and familiar. The only unusual detail is that note fields are stored as a single tab‑separated string.

### genanki for Programmatic Editing

`genanki` is a Python library that lets users create and modify Anki decks programmatically. It provides a clean interface for defining models, adding notes, and exporting `.apkg` files. This is especially useful when converting AI‑generated JSON or JSONL flashcards into Anki decks, or when generating large numbers of cards automatically.

### Editing and Organizing Cards with GUI and CLI Tools

Anki Desktop provides the most accessible way to edit and organize cards, offering tools for browsing, tagging, reorganizing, and reviewing. Mobile versions on Android and iOS support editing and reviewing on the go. For advanced workflows, users can rely on command‑line tools, SQLite clients, or Python scripts to automate bulk edits or integrate with external systems.

---

### Summary

**Anki serves as the human‑centered counterpart to JSON and JSONL flashcard systems, allowing machine‑generated or streamed content to become part of a learner’s real study process.**

Anki uses **SQLite**, which is readable and modifiable with standard SQL tools.  
You can **extend the schema safely** by adding new tables, but modifying existing ones risks breaking Anki.  
SQL‑confident users can easily query, update, and reorganize cards.  
`genanki` provides a clean Python API for generating or editing decks.  
GUI tools (Anki Desktop, AnkiMobile, AnkiDroid) remain the easiest way to manage cards.  
CLI tools and SQLite access allow deeper automation and integration with AI systems.

## End‑to‑End Pipeline: From Mixed Sources to a Probabilistic Anki/JSONL Service

This chapter walks through a full workflow:

1. **Preprocess script** — gathers flashcards from JSON, JSONL, Anki, and other formats into a unified Anki deck.  
2. **Conscious processing** — the human tests the deck, adjusts categories, and decides probabilities.  
3. **Flask service** — reads from the Anki SQLite collection and serves JSONL flashcards with deck‑based probabilities.

---

### Preprocess Script: Gathering and Normalizing Sources

We’ll define simple reader classes for different formats and a script that:

- Instantiates readers for JSON, JSONL, Anki, and hypothetical formats.  
- Adds metadata (e.g., `category`, `source_label`) to each card.  
- Builds an Anki deck using `genanki`.

#### Example readers and preprocess script (`preprocess.py`)

```python
import json
import genanki
import sqlite3
from pathlib import Path

# --- Reader base class -------------------------------------------------------

class BaseReader:
    def __iter__(self):
        return self

    def __next__(self):
        line = self.read()
        if line is None:
            raise StopIteration
        return line

    def read(self):
        raise NotImplementedError


# --- JSONL reader ------------------------------------------------------------

class JSONLReader(BaseReader):
    def __init__(self, filename, category):
        self.filename = filename
        self.category = category
        self._file = open(self.filename, "r", encoding="utf-8")

    def read(self):
        line = self._file.readline()
        if not line:
            return None
        obj = json.loads(line)
        obj["category"] = self.category
        return obj


# --- JSON array reader -------------------------------------------------------

class JSONReader(BaseReader):
    def __init__(self, filename, category):
        self.filename = filename
        self.category = category
        with open(self.filename, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        self._index = 0

    def read(self):
        if self._index >= len(self._data):
            return None
        obj = self._data[self._index]
        self._index += 1
        obj["category"] = self.category
        return obj


# --- Anki SQLite reader (hypothesis: existing collection) --------------------

class AnkiSQLiteReader(BaseReader):
    """
    Reads notes from an existing Anki collection.anki2 file.
    Hypothesis: we treat each note as a card with Front/Back fields.
    """

    def __init__(self, collection_path, deck_name_label):
        self.collection_path = collection_path
        self.deck_name_label = deck_name_label
        self.conn = sqlite3.connect(self.collection_path)
        self.cur = self.conn.cursor()
        # Simple example: read all notes
        self.cur.execute("SELECT id, flds FROM notes")
        self._rows = self.cur.fetchall()
        self._index = 0

    def read(self):
        if self._index >= len(self._rows):
            return None
        note_id, flds = self._rows[self._index]
        self._index += 1
        fields = flds.split("\t")
        if len(fields) < 2:
            return None
        front, back = fields[0], fields[1]
        return {
            "instruction": front,
            "output": back,
            "category": self.deck_name_label,
        }


# --- Hypothetical CSV reader -------------------------------------------------

class CSVReader(BaseReader):
    """
    Hypothetical format: CSV with columns front,back.
    """

    def __init__(self, filename, category):
        import csv
        self.filename = filename
        self.category = category
        self._file = open(self.filename, "r", encoding="utf-8")
        self._reader = csv.DictReader(self._file)

    def read(self):
        try:
            row = next(self._reader)
        except StopIteration:
            return None
        return {
            "instruction": row["front"],
            "output": row["back"],
            "category": self.category,
        }


# --- Build Anki deck from all sources ---------------------------------------

def build_anki_deck(output_apkg, readers):
    model = genanki.Model(
        1607392319,
        "Unified Model",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Category"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}<br><small>{{Category}}</small>",
                "afmt": "{{Front}}<hr id='answer'>{{Back}}<br><small>{{Category}}</small>",
            }
        ],
    )

    deck = genanki.Deck(2059400110, "Unified AI Deck")

    for reader in readers:
        for card in reader:
            front = card.get("instruction", "")
            back = card.get("output", "")
            category = card.get("category", "uncategorized")
            note = genanki.Note(model=model, fields=[front, back, category])
            deck.add_note(note)

    genanki.Package(deck).write_to_file(output_apkg)


if __name__ == "__main__":
    # Example usage:
    readers = [
        JSONLReader("data/math.jsonl", category="math"),
        JSONReader("data/history.json", category="history"),
        AnkiSQLiteReader("existing/collection.anki2", deck_name_label="legacy"),
        CSVReader("data/custom.csv", category="custom"),
    ]

    Path("output").mkdir(exist_ok=True)
    build_anki_deck("output/unified_deck.apkg", readers)
    print("Unified Anki deck created: output/unified_deck.apkg")
```

#### Command line example

```bash
python preprocess.py
```

This gathers all sources, labels them with `category`, and produces `output/unified_deck.apkg`.

---

### Conscious Processing: Human Testing and Probability Decisions

Once the unified deck is created and imported into Anki:

1. The user **reviews cards** in Anki’s GUI, checking:
   - clarity of questions  
   - correctness of answers  
   - balance between categories (math, history, legacy, custom, etc.)  

2. They may export statistics or just rely on intuition:
   - “Math cards are too easy; show them less often.”  
   - “Legacy cards are messy; show them rarely.”  
   - “Custom cards are crucial; show them more often.”  

3. Based on this, they decide **probabilities per category/deck**, e.g.:

```text
math:   1.0
history: 2.0
legacy: 0.5
custom: 3.0
```

These weights will later be used by the Flask service to decide how often to serve cards from each category.

---

### Flask Service: Serving JSONL from Anki with Deck Probabilities

Now we build a Flask service that:

- Opens an Anki `collection.anki2` file.  
- Maps deck names (or categories) to probability weights.  
- On each request for a card, chooses a deck according to its weight.  
- Streams cards as JSONL at `http://localhost:8000/`.

#### Flask service (`service.py`)

```python
import json
import random
import sqlite3
from flask import Flask, Response

app = Flask(__name__)

COLLECTION_PATH = "existing/collection.anki2"

# Example deck probability configuration (deck name -> weight)
DECK_WEIGHTS = {
    "math": 1.0,
    "history": 2.0,
    "legacy": 0.5,
    "custom": 3.0,
}


class AnkiDeckStreamer:
    def __init__(self, collection_path, deck_weights):
        self.conn = sqlite3.connect(collection_path)
        self.cur = self.conn.cursor()
        self.deck_weights = deck_weights
        self.deck_ids = self._load_deck_ids()
        self.deck_card_ids = self._load_cards_by_deck()
        self._prepare_weight_vector()

    def _load_deck_ids(self):
        # Decks are stored as JSON in col.decks; we map names to IDs.
        self.cur.execute("SELECT decks FROM col")
        row = self.cur.fetchone()
        if not row:
            return {}
        decks_json = json.loads(row[0])
        name_to_id = {}
        for deck_id, deck_info in decks_json.items():
            name = deck_info.get("name", "")
            name_to_id[name] = int(deck_id)
        return name_to_id

    def _load_cards_by_deck(self):
        deck_card_ids = {name: [] for name in self.deck_weights.keys()}
        for deck_name, weight in self.deck_weights.items():
            if weight <= 0:
                continue
            deck_id = self.deck_ids.get(deck_name)
            if deck_id is None:
                continue
            self.cur.execute(
                "SELECT id, nid FROM cards WHERE did = ?", (deck_id,)
            )
            rows = self.cur.fetchall()
            deck_card_ids[deck_name] = [row[1] for row in rows]  # store note IDs
        return deck_card_ids

    def _prepare_weight_vector(self):
        self._names = []
        self._weights = []
        for name, w in self.deck_weights.items():
            if w > 0 and self.deck_card_ids.get(name):
                self._names.append(name)
                self._weights.append(w)
        self._total_weight = sum(self._weights)

    def _choose_deck(self):
        r = random.uniform(0, self._total_weight)
        cumulative = 0.0
        for name, w in zip(self._names, self._weights):
            cumulative += w
            if r <= cumulative:
                return name
        return self._names[-1]

    def read(self):
        """
        Return one JSONL line (string) or None if no cards available.
        """
        if not self._names:
            return None

        attempts = len(self._names)
        while attempts > 0:
            deck_name = self._choose_deck()
            cards = self.deck_card_ids.get(deck_name, [])
            if not cards:
                attempts -= 1
                continue

            note_id = random.choice(cards)
            self.cur.execute("SELECT flds FROM notes WHERE id = ?", (note_id,))
            row = self.cur.fetchone()
            if not row:
                attempts -= 1
                continue

            fields = row[0].split("\t")
            if len(fields) < 2:
                attempts -= 1
                continue

            front, back = fields[0], fields[1]
            obj = {
                "instruction": front,
                "output": back,
                "deck": deck_name,
            }
            return json.dumps(obj)

        return None


streamer = AnkiDeckStreamer(COLLECTION_PATH, DECK_WEIGHTS)


def stream_generator():
    while True:
        line = streamer.read()
        if line is None:
            break
        yield line + "\n"


@app.route("/")
def root_stream():
    return Response(stream_generator(), mimetype="application/jsonl")


if __name__ == "__main__":
    # Serve at http://localhost:8000/
    app.run(host="0.0.0.0", port=8000, debug=False)
```

#### Command line example

```bash
python service.py
```

Then, from another terminal:

```bash
curl http://localhost:8000/
```

You’ll see a stream of JSONL flashcards, each line something like:

```json
{"instruction": "What is JSONL?", "output": "A line-delimited JSON format.", "deck": "custom"}
```

---

### Summary

- The **preprocess script** gathers JSON, JSONL, Anki, and other formats into a unified Anki deck, labeling each card with metadata like `category`.  
- The **conscious processing** phase lets a human test the deck, adjust content, and decide probability weights per category/deck.  
- The **Flask service** reads directly from the Anki SQLite collection, uses deck probabilities to choose cards, and serves them as JSONL at `http://localhost:8000/`.  

This pipeline ties together human pedagogy, structured data formats (JSON/JSONL), and Anki’s scheduling ecosystem into a single, extensible system.

# General summary

## Bringing It All Together

By now, you’ve seen how flashcards, JSON/JSONL formats, Anki, preprocessing scripts, and streaming services all fit into a single coherent workflow. What begins as a simple idea—**a question on the front, an answer on the back**—scales into a complete ecosystem for training AI models, organizing human knowledge, and building maintainable data pipelines. The pieces may look technical when viewed separately, but together they form a system that is surprisingly intuitive:

- **Humans create, curate, and test cards**  
- **Scripts gather and normalize data**  
- **Anki provides structure and pedagogy**  
- **JSONL provides efficient machine‑friendly streaming**  
- **Flask services deliver cards on demand**  
- **LitGPT learns from the resulting stream**

This is the essence of the workflow: a loop where human insight and machine learning reinforce each other.

---

## Toward More Advanced Conclusions

Once you understand the basic flow, deeper patterns emerge:

- **Flashcards are a universal abstraction**  
  Whether stored in Anki, JSON, JSONL, CSV, or generated by code, they all represent the same idea: a mapping from input to output. This makes them ideal for both human learning and AI training.

- **Streaming is the natural evolution of datasets**  
  Instead of static files, you can build dynamic, probabilistic, infinite, or mixed‑source streams. This mirrors how humans learn from varied, unpredictable experiences.

- **Human pedagogy improves machine learning**  
  When you test your own cards, adjust categories, and refine phrasing, you’re not just improving your study deck—you’re improving the AI’s training data. Your teaching instincts become part of the model.

- **Anki acts as a bridge between worlds**  
  It is human‑friendly enough for beginners and structured enough for programmers. Its SQLite foundation makes it scriptable, while its GUI makes it accessible.

- **The system is modular and extensible**  
  You can add new readers, new generators, new categories, new probability rules, or new streaming behaviors without rewriting the whole pipeline.

These conclusions point toward a powerful idea: **you are not just training a model—you are designing a learning environment.**

---

## How to Use This Knowledge Efficiently (Especially with LaegnaAIExperiments)

The repository at  
**https://github.com/tambetvali/LaegnaAIExperiments/tree/main**  
contains practical examples, experiments, and scaffolding that align perfectly with the concepts explained here. To make the most of it, different types of users can follow different paths:

### For beginners and non‑technical users
- Start by creating simple cards in Anki.  
- Import AI‑generated cards and test them yourself.  
- Use the repository’s examples to see how JSONL datasets look.  
- Focus on clarity, correctness, and good teaching structure.

### For administrators and IT managers
- Use the preprocessing scripts to gather data from multiple sources.  
- Organize cards into categories that reflect your organization’s needs.  
- Adjust probability weights to emphasize important topics.  
- Ensure data quality before training begins.

### For programmers and technical users
- Explore the repository’s code to understand how readers, generators, and services are implemented.  
- Extend the system with new formats or new streaming behaviors.  
- Integrate the Flask service into your training pipeline.  
- Experiment with synthetic data generation, curriculum learning, or probabilistic routing.

### For teams working together
- Let subject‑matter experts curate cards in Anki.  
- Let developers automate preprocessing and streaming.  
- Let administrators manage categories and probabilities.  
- Let the AI learn from the combined expertise of everyone involved.

---

## Final Perspective

This entire approach—combining Anki, JSONL, preprocessing, and streaming—creates a **living learning system**. It grows with your data, adapts to your needs, and remains understandable at every level. Whether you’re a beginner or an expert, you can contribute meaningfully:

- by writing good cards  
- by organizing categories  
- by tuning probabilities  
- by extending the code  
- by evaluating the AI’s progress  

The tools are simple, the workflow is flexible, and the results can be remarkably powerful. With the foundations laid out in this material and the practical examples in the LaegnaAIExperiments repository, you now have everything you need to build, refine, and operate your own smart flashcard‑driven AI training system.
