# Smart List class

class SmartList:

    def __init__(self) -> None:
        self.list = []

    
    def __repr__(self):
        return f"SmartList: {len(self.list)}"

    
    def add(self, item) -> int:
        """Adds item to list. Returns number of items in list."""
        self.list.append(item)
        return len(self.list)
    

    def remove(self, item) -> int:
        """Removes item from list. Returns number of items left."""
        if item in self.list:
            self.list.remove(item)
        return len(self.list)

    
    def find(self, value) -> any:
        """Finds an item equal to the specified value. Returns item."""
        for n in self.list:
            if n == value:
                return n
        
    
    def find_attr(self, key, value) -> object:
        """Finds an item with matching key-value pair. Returns item or None."""
        for i in self.list:
            if hasattr(i, key) and getattr(i, key) == value:
                return i

        return None
    

    def attr(self, key, value) -> None:
        """Sets a new attribute."""
        setattr(self, key, value)