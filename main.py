#!/usr/bin/env python

import app
from tendo import singleton

# load tensorflow upfront to prevent ui blocking on first experiment run
import tensorflow as tf

if __name__ == "__main__":
    instance = singleton.SingleInstance()
    app = app.GUI(instance)
