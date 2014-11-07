"""
.. module:: events
   :Platform: Unix, Windows
   :Synopsis: A module that contains an event manager and all types of events, that can occur in game.
"""

class Event:
    """This is a superclass for any events that might be generated by an object and sent to the EventManager.
    """

    def __init__(self):
        """Generic event.
        
        :Attributes:
            - *name* (string): Type of the event as a name
        """
        self.name = "Generic Event"

class TickEvent(Event):
    """CPU Tick event will be send every frame.
    
    :Attributes:
        - *dt* (int): Time expired since CPU Tick
    """
    
    def __init__(self, dt):
        """
        :param dt: Time expired since CPU tick.
        :type dt: int
        """
        self.name = "CPU Tick Event"
        self.dt = dt

class ResizeWindowEvent(Event):
    """Resize Window Event.
    Is send when event of type pygame.VIDEORESIZE is occurs.
    
    :Attributes:
        - *width* (int): New width of the window
        - *height* (int) New height of the window
    """
    
    def __init__(self, width, height):
        """
        :param width: New width of the window
        :type width: int
        :param height: New height of the window
        :type height: int
        """
        self.name = "Resize Window Event" 
        self.width = width
        self.height = height

class QuitEvent(Event):
    """Programm Quit Event.
    Is send when event of type pygame.QUIT is occurs.
    """
    
    def __init__(self):
        self.name = "Program Quit Event"

class KeyPressed(Event):
    """This event stores the pressed key.
    Is send when event of type pygame.KEYDOWN is occurs.
    
    :Attributes:
        - *key* (): pressed key
    """ 
    
    def __init__(self, key):
        """
        :param key: pressed key
        :type key: pygame enum
        """
        self.name = "Key Down Event"
        self.key = key

class KeyReleased(Event):
    """This event stores the released key.
    
    :Attributes:
        - *key* (): released key
    """
    
    def __init__(self, key):
        """
        :param key: released key
        :type key: pygame enum
        """
        self.name = "Key Released Event"
        self.key = key

class MouseButtonDown(Event):
    """Mouse button down event."""
    
    def __init__(self):
        self.name = "Mouse button down"

class MouseMoved(Event):
    """Mouse moved event stores new position of mouse pointer on the screen.
    
    :Attributes:
        - *x* (int): x value of new mouse pointer position
        - *y* (int): y value of new mouse pointer position
    """
    
    def __init__(self, x, y):
        """
        :param x: x value of new mouse pointer position
        :type x: int
        :param y: y value of new mouse pointer position
        :type y: int
        """
        self.name = "Mouse Moved Event"
        self.x = x
        self.y = y

class AxisMoved(Event):
    """This event stores position of a game pad axis.
    Values of the axis position can be between -1 and 1 with 0 value, when it's centered. Bottom right corner is (1,1).
    
    :Attributes:
        - *x_axis_pos* (float): x value of axis position
        - *y_axis_pos* (float): y value of axis position
    """
    
    def __init__(self, x_axis_pos, y_axis_pos):
        """
        :param x_axis_pos: x value of axis position
        :type x_axis_pos: float
        :param y_axis_pos: y value of axis position
        :type y_axis_pos: float
        """
        self.name = "Controller Axis Moved Event"
        self.x_axis = x_axis_pos
        self.y_axis = y_axis_pos

class HatMoved(Event):
    """This event stores position of a game pad hat.
    Position of the hat are two values which can be 0, 1 or -1. A value of -1 means left/down and a value of 1 means right/up.
    
    :Attributes:
        - *x* (int): x value of hat position
        - *y* (int): y value of hat position
    """
    
    def __init__(self, x, y):
        """
        :param x: x value of hat position
        :type x: int
        :param y: y value of hat position
        :type y: int
        """
        self.name = "Controller Hat Moved Event"
        self.x = x
        self.y = y

class UpdateImagePosition(Event):
    """Occurs when entity has moved and image position has to be updated.
    
    :Attributes:
        - *entity_ID* (int): entity that has been moved
        - *new_position* (int tuple): new position
    """
    
    def __init__(self, entity_ID, new_position):
        """
        :param entity_ID: entity that has been moved
        :type entity_ID: int
        :param new_position: new position
        :type new_position: int tuple
        """
        self.name = "Update Image Position"
        self.entity_ID = entity_ID
        self.new_position = new_position

class PlayerMoved(Event):
    """This event is sent every time when player moves.
    Is used in enemy AI and animation system.
    
    :Attributes:
        - *new_position* (2D list): new position of the player
    """
    
    def __init__(self, new_position):
        """
        :param new_position: new position of the player
        :type new_position: 2D list
        """
        self.name = "Player Moved Event"
        self.new_position = new_position

class PlayerStoppedMovement(Event):
    """This event is sent when player stops movement.
    Is used in enemy AI and animation system.
    """
    
    def __init__(self):
        self.name = "Player Stopped Movement"

class EventManager:
    """This class is responsible for coordinating most communication between the game systems.
    
    This class and the idea of event driven architecture was taken from `sjbrown's Writing Games Tutorial <http://ezide.com/games/writing-games.html>`_.
    
    :Attributes:
        - *listener* (): registered listeners
    """
    
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        #self.eventQueue= []

    def register_listener(self, listener):
        """Register a listener to this event manager.
        Listener must contain notify() method.
        
        :param listener: listener to register
        """
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """Unregister a listener of this event manager.
        
        :param listener: listener to unregister
        """
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        """Pass an event to all registered listeners of this event manger.
        
        :param event: event that will be passed
        :type event: Event
        """ 
        for listener in self.listeners:
            #NOTE: If the weakref has died, it will be automatically removed,
            #so we don't have to worry about it.
            listener.notify(event)