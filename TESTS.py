import threading
from queue import Queue

def display_worker(display_queue):
    while True:
        line = display_queue.get()
        if line is None:  # simple termination logic
            break
        print(line)


def some_other_worker(display_queue):
    # NOTE accepts queue reference as an argument, though it could be a global
    display_queue.put("something which should be printed from this thread")

    string = "HELLO WORLD"
    for i in string:
        display_queue.put(i)

    display_queue.put(input("type:"))


def main():
    display_queue = Queue()  # synchronizes console output

    writer_thread = threading.Thread(
        target=some_other_worker,
        args=(display_queue,),
    )
    screen_printing_thread = threading.Thread(
        target=display_worker,
        args=(display_queue,),
    )
    writer_thread.start()
    screen_printing_thread.start()

main()

    ### other logic ###