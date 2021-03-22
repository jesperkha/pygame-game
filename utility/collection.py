# Collection class for lagless storage

# ROOT NODE ------------------------------------------------------------- #
class Node:
    def __init__(self, value=None) -> None:
        self.value = value
        self.next = None
        self.prev = None
        self.nodes = 0

    
    def new(self, value) -> object:
        """
        Add new node to list. Nodes are added at the beginning of the list.
        Returns:
        • int: Number of current nodes
        """
        new_node = Node(value)

        if self.next:
            next_node = self.next
            new_node.prev = new_node
            new_node.next = next_node
            self.next = new_node
            new_node.prev = self
        else:
            self.next = new_node
            new_node.prev = self
        
        return new_node
            

    def find(self, value) -> object:
        """Returns the first Node with the requested value"""
        if self.value == value:
            return self
        elif self.next:
            return self.next.find(value)
    
    
    def print_out(self) -> None:
        """Prints out the value for each node. Not recommended if the values are objects"""
        print(self.value)
        if self.next:
            self.next.print_out()


    def remove(self) -> None:
        """Removes node from collection"""
        if self.prev:
            self.prev.next = self.next


    def map_func(self, func) -> None:
        """Maps a function to all elements in collection. The function should expect a Node as a parameter."""
        if self.value:
            func(self)
        if self.next:
            self.next.map_func(func)


def test():
    # Test 1: Creating new nodes
    try:
        root = Node()
        root.new(1)
        root.new(2)
        print("Test 1: Complete")
    except:
        print("Test 1: Failed")

    # Test 2: Deleting nodes
    try:
        root = Node()
        a = root.new(10)
        a.remove()
        if root.next:
            raise Exception()
        print("Test 2: Complete")
    except:
        print("Test 2: Failed")

    # Test 3: Finding a Node
    try:
        root = Node()
        root.new(1)
        root.new(2)
        a = root.find(1)
        if a:
            print("Test 3: Complete")
        else:
            raise Exception()
    except:
        print("Test 3: Failed")

    # Test 4: Mapping a function
    try:
        root = Node()
        b = root.new(1)
        def map_func(a):
            a.value += 1
        root.map_func(map_func)
        if b.value == 2:
            print("Test 4: Complete")
        else:
            raise Exception()
    except:
        print("Test 4: Failed")
test()