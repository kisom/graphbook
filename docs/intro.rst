Introduction
============

As a programmer, I'm constantly learning new things - and should be taking
notes on them. There are a lot of strategies for doing this, which will be
discussed later. However, none of these strategies effectively captures the
several key properties that are of particular interest to a programmer (and
to several other professions). The problem is to enable the programmer to
develop and build their own personal repository of knowledge in a useful
ontology that also facilitates in-band exploration of ideas. A useful system
will

1. Provide a mechanism for capturing thoughts and knowledge
2. Provide tooling for organising this collection
3. Support small programs alongside information to demonstrate ideas
4. Allow the programmer to share knowledge with other programmers

As mentioned before, there is quite a bit of related work:

+ Wikis are useful in that they provide an easy way to organise and capture
  knowledge. There are limits to these: the more featured examples require
  running on a server (usually to facilitate information sharing), and those
  that don't are harder to synchronise with other users.
+ Jupyter notebooks are useful explorations of a particular topic, but they
  suffer from a few misfeatures: they have a shared lexical environment and
  their only real built-in organisational feature is a tree structure with
  hyperlinks.
+ Many programmers keep a collection of notes as plaintext files stored locally
  and perhaps synchronised across multiple machines via source control (e.g.
  git) or a networked file system (like Dropbox or Google Drive).
                                                                        
The approach taken by GraphBook, as the name might imply, is a notebook where
the pages are organised as a graph of nodes. In its current nascent state,
many details are still being explored. However, the following basic structure
is currently being pursued:

+ A notebook is a graph: a collection of nodes that are linked to other
  nodes.
+ The persisted form of the notebook should be suitable for synchronisation
  via a network file system.
+ The notebook can run as a local process that can provide a server interface
  over the notebook. A peer-to-peer scheme (like a DHT) could provide remote
  access and sharing.
+ A sandboxed execution environment will provide the opportunity for programs
  to be embedded alongside other forms of knowledge capture (like plaintext).
  
The goals of this project are to provide such an interface that can operate
as a useful extension of the programmer, with programs as illustrations of
ideas. The end result should be something of a cross between a wiki, a code
snippet store, and a Jupyter notebook.

Current ideas for the sandboxed environment are

+ A WASM virtual machine.
+ Shelling out to a program on the user's machine, e.g. a Lua interpreter.