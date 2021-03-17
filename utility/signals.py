# Signals

class Signal:
    signals = {}

    @staticmethod
    def add(name: str, callback) -> None:
        """
        Adds a signal reciever
        Args:
        • name: name of signal
        • callback: functon that will execute upon recieving signal
        """
        if not name in Signal.signals:
            Signal.signals[name] = [callback]
        else:
            Signal.signals[name].append(callback)

    
    @staticmethod
    def emit(name: str, *args: any) -> int:
        """
        Emits signal by signal name
        Args:
        • name: name of signal
        • *args: arguments for functions
        Returns:
        • int: number of signals emitted
        """
        num_called = 0
        if name in Signal.signals:
            for callback in Signal.signals[name]:
                callback(*args)
                num_called += 1

        return num_called
