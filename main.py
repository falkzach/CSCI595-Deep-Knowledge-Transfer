#!/usr/bin/env python

import app
from tendo import singleton

if __name__ == "__main__":
    me = singleton.SingleInstance()
    app = app.GUI()
