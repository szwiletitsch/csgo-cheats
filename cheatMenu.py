import tkinter as tk
import threading
import time
from hacks.wallHack import wall_hack
from functools import partial


def thread_function1(should_run):
    while should_run.is_set():
        print("Thread 1 is running.")
        time.sleep(1)


def thread_function2(should_run):
    while should_run.is_set():
        print("Thread 2 is running.")
        time.sleep(2)


class CheatMenu:
    def __init__(self, root, config):
        self.root = root
        self.root.title("CheatMenu")
        self.root.call('wm', 'attributes', '.', '-topmost', True)

        self.check_vars = []
        self.check_boxes = []
        for index, (title, func) in enumerate(config["cheats"]):
            self.check_vars.append(tk.BooleanVar())
            self.check_boxes.append(
                tk.Checkbutton(
                    root,
                    text=title,
                    variable=self.check_vars[-1],
                    command=partial(self.toggle_thread, index, func)
                )
            )
            self.check_boxes[-1].pack(anchor='w')  # Align to the left

        self.threads = []

    def toggle_thread1(self):
        self.toggle_thread(1, wall_hack)

    def toggle_thread2(self):
        self.toggle_thread(2, thread_function2)

    def toggle_thread(self, thread_number, target_function):
        if thread_number in [t[0] for t in self.threads]:
            for thread in self.threads:
                if thread[0] == thread_number:
                    thread[1].clear()
                    self.threads.remove(thread)
                    break
        else:
            # start thread and keep track of it in self.threads
            should_run = threading.Event()
            should_run.set()
            thread = threading.Thread(target=target_function, args=(should_run,))
            self.threads.append((thread_number, should_run, thread))
            thread.start()

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = CheatMenu(tk_root, {
        "cheats": [
            ["Wall-Hack", wall_hack],
            ["Test1", thread_function1],
            ["Test2", thread_function2]
        ]
    })

    tk_root.mainloop()
