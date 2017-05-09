import tkinter as tk

class TkIoRedirect(object):
    def __init__(self,text_area):
        self.text_area = text_area

    def write(self, message):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message)
        self.text_area.config(state="disabled")
        self.text_area.see("end")

    def flush(self):
        pass
