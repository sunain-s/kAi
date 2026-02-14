# kAI
Semi-retrieval AI based chatbot made in Python using TensorFlow + Pygame

A-Level OCR CS H446 2023 NEA

## Project Requirements

- Interface is a clean and simple dark theme, easy to view for the visually impaired
- 1280x720 resolution display
- Message display similar to that of a standard messaging app e.g. message bubbles, time of message
- Main menu with notification controls and application user instructions
- Topic prompts that focus AI conversation to the side of the message display
- Only takes keyboard and mouse inputs
- Outputs notification sound alerts (can be muted from menu)
- Uses as little storage space as possible
- Runs on Win10 and later versions as an .exe ==> runs as a .py file on Python 3.9 and later, provided all external libraries are installed and up to date

## How to Run and Use

**Raw Python File**:
<ol>
    <li>Download the zip file and extract the contents</li>
    <li>Install Python 3.9+</li>
    <li>Use pip to install tensorflow 2.11.0+, numpy 1.22.3+, nltk 3.7+, pygame 2.1.2+</li>
    <li>Run the 'graphics.py' file</li>
    <li>'kAi.exe' can be deleted to save storage space</li>
</ol>

**Executable**:
<ol>
    <li>Download the zip file and extract the contents</li>
    <li>Run 'kAi.exe'</li>
</ol>

User manual can be accessed at all times within the menu and chat window by clicking the help icon

## What I Learnt

### Theory
- Development Methodologies - used an agile and waterfall model
- Data reshaping and pre-processing
    - input-output pair creation
    - tokenisation and lemmatisation
- Neural Network Theory
    - layering, activation and bias
    - mathematical expression via linear algebra
    - cost functions and backpropagtion (SGD)
    - RNNs and Seq2Seq models
- Pre-decomposition
    - flowcharts, top down diagrams and function/procedure tables
    - algorithm design using pseudocode
- Types of testing e.g. black box, alpha and beta

### Programming
- Using TensorFlow to create and use a NN model
    - forming numpy arrays to creating training binaries
- Conditional list comprehensions and lambda functions
- Message thread processing and splitting
- Storing data for multi-file use
    - JSON for training data
    - Pickling data for BOW algorithm
- Use of win32 library to create transparent window

## Improvements

- The currently used corpus is a dummy corpus - general corpora needs to be implemented
    - Originally implemented with a custom corpora designed for my client
- Deep learning AI rather than a semi-retrieval based AI which constructs the messages itself
    - would require lots of training to reach an acceptable quality
- Fix the message send and recieve timings, along with the notifications
    - currently occur at the same time
- Combine all corpora and models into a single model to maximise program storage size
- Create a neural network from scratch to remove dependency and bloat from TensorFlow
- Allow for use of emojis/emoticons that can be recognised by the AI

