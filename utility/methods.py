from threading import Timer

# Set timeout function (like in javascript)
def set_timeout(callback, time: float) -> None:
    t = Timer(time, callback)
    t.start()