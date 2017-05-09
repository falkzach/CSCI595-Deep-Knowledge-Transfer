# Deep Knowledge Transfer


## Experiments
* must be a python file using tensforflow core libraries

* must implement the `__call__(self, *args, **kwargs)` function

* the `__call__` function must return a message as a String and the session. `return msg, sess`

* the tensorflow session cannot be called using a `with` statement as it closes the session freeing all resources