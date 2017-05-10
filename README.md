# Deep Knowledge Transfer
A GUI utility implemented in python to simplify the running of TensorFlow experiments, save models, and transfer knowledge between them.

## Dependencies
* `python 3.5` for compatibility with `tensorflow-gpu`

* `tensorflow` preferably `tensorflow-gpu`

* `tkinter`

* `tendo`

## Running
`python3 main.py`

## Experiments
* must be a python file using tensforflow core libraries

* must implement the `__call__(self, *args, **kwargs)` function

* the `__call__` function must return a message as a String and the session. `return msg, sess`

* the TensorFlow session cannot be called using a `with` statement as it closes the session freeing all resources
