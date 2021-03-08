# Keyboard controls

from pygame import key

# This function is an attempt at optimizing the efficiency of controller updates. Before, each controller
# would get the pressed_keys list locally in the update function. Now the key.get_pressed() method is only called once.

def update_controllers():

    # Get all keys that are currently pressed
    pressed_keys = key.get_pressed()

    for c in Controller.controllers:
        c.update(pressed_keys)


class Key:

    # Key class for individual keys

    def __init__(self, key, key_type: str, callback) -> None:

        # Key type provided by pygame module. Ex: pygame.K_p ("p")
        self.key = key

        # Current state of the key (down or not down)
        self.down = False

        # State of key that is looked for. Includes: keydown, keyup, keypressed
        # The callback function will be called if the key has the given state.
        # A key can only have one state. To have more functions for the same key, use more key listeners.
        self.type = key_type
        self.callback = callback


# _________________________________________________________________________________________________


class Controller:

    # List of controller objects. Updated in Game object every frame
    controllers = []

    def __init__(self):
        self.keys = []
        Controller.controllers.append(self)


    # -------------------------------

    # Add new input key to controller

    # -------------------------------

    # Add new key listener. Listenes for the key in every call of update and checks for the given state. Calls callback.
    # Params: pygame key, state of key, callback function
    def listen(self, key, state: str, callback):
        
        """
        Args:
        * key: pygame key
        * state: ("keypressed", "keyup", "keydown")
        * callback: callback function for keypress
        """

        self.keys.append(Key(key, state, callback))


    # -------------------------------------------

    # Updates key states and cheks for new inputs

    # -------------------------------------------
    
    def update(self, pressed_keys: list) -> None:

        # For every Key object in this controller, check to see if it is part of the pressed keys list.
        
        # Then handle the state changes and callbacks:
        # Ex: If the key state is down and the key is pressed, call callback
        # Also stores the state of the key in the Key object
        for key_index in self.keys:

            # All if statements check the state of the key by looking to see if it is included in the
            # pressed_keys array provided by the pygame module.

            # --- #

            # For the "keypressed" state
            # If key is pressed and state is up then change state to down and call callback
            if key_index.type == "keypressed" and pressed_keys[key_index.key] and key_index.down == False:
                key_index.callback()
                key_index.down = True

            # Reset if key is not pressed
            if key_index.type == "keypressed" and not pressed_keys[key_index.key]:
                key_index.down = False


            # --- #

            # For the "keyup" state
            # If key is not pressed and state is down then change state to up and call callback
            if key_index.type == "keyup" and not pressed_keys[key_index.key] and key_index.down == True:
                key_index.callback()
                key_index.down = False
            
            # Reset if key is pressed
            if key_index.type == "keyup" and pressed_keys[key_index.key]:
                key_index.down = True


            # --- #
            
            # For the "keydown" state
            # If key is pressed then call callback
            if key_index.type == "keydown" and pressed_keys[key_index.key]:
                key_index.callback()
        

    def remove(self):
        Controller.controllers.remove(self)