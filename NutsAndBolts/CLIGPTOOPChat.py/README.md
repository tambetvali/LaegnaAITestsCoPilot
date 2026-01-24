# Object Oriented Chatting

Here, you find what are the most basic classes for our chat interaction.

They support:
* Rather than whole chat in one object, "parent" object contains the previous message, and it's parent the next previous message: this reminds of GPT model, which has each token in new layer (whole "object") rather than in the same memory space, where they would be calculated in one operation, as one object.
* This way, each new Q&A provides a static moment, which is stored into stateless object. This allows multiple interfaces:
  * If you do not add more content under the same object, you can use it for stateless work, such as having task like "Translate this to English" or "Generate 10 Q&A pairs based on this"; you can easily create the confortable type of object.
  * You can create a normal conversation, where each new question and answer pair produces a new child.
  * You can create branched conversation, as explained in my manuals.
