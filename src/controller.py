"""
.. module:: controller
    :platform: Unix, Windows
    :synopsis: Generates events according input of various controllers connected to the game.
"""

import pygame
import events

class InputController:
    """InputController manages connected controllers and takes events generated by them sending other events to the game.

    :Attributes:
        - *event_manager* (events.EventManager): event manager
        - *joystick* (pygame.joystick.Joystick): game pad, tested here only with sony controller
    """

    def __init__(self, event_manager):
        #Register InputController, so it can handle events
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        #Register game pad, if any connected
        pygame.joystick.init()
        self.joystick = None
        self.joystick_count = pygame.joystick.get_count()
        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

    def init_right_joystick(self):
        """If there are more then one joysticks connected.
        Recognize the right one.
        """
        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            if joystick.get_button(7):
                self.joystick = joystick
                self.joystick.init()
                return

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            #Every CPU-tick handle input events
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    resize_ev = events.ResizeWindowEvent(event.w, event.h)
                    self.event_manager.post(resize_ev)
                if event.type == pygame.QUIT:
                    quit_ev = events.QuitEvent()
                    self.event_manager.post(quit_ev)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_ev = events.QuitEvent()
                        self.event_manager.post(quit_ev)

                if not self.joystick:
                    self.init_right_joystick()
                    #Handle events generated by keyboard
                    if event.type == pygame.KEYDOWN:
                        key_ev = events.KeyPressed(event.key)
                        self.event_manager.post(key_ev)
                    if event.type == pygame.KEYUP:
                        key_ev = events.KeyReleased(event.key)
                        self.event_manager.post(key_ev)
                    #Handle events generated by mouse    
                    if event.type == pygame.MOUSEMOTION:
                        direction_X, direction_Y = pygame.mouse.get_pos()
                        mouse_ev = events.MouseMoved(direction_X, 
                                                     direction_Y)
                        self.event_manager.post(mouse_ev)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        attack_request_ev = events.MouseButtonDown()
                        self.event_manager.post(attack_request_ev)

                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(7) and self.joystick.get_button(6):
                        '''
                        XBox button(6) = back button(7) = start
                        '''
                        #K-key resets the game
                        key_ev = events.KeyPressed(pygame.K_k)
                        self.event_manager.post(key_ev)
                if event.type == pygame.JOYAXISMOTION:
                    horiz_axis_pos, vert_axis_pos = self.get_axis_pos()
                    #Game pad events will be sent every tick
                    #Get second axis values and send this as an event
                    axis_ev = events.AxisMoved(horiz_axis_pos,
                                               vert_axis_pos)
                    self.event_manager.post(axis_ev)
                if event.type == pygame.JOYHATMOTION:
                    if self.joystick.get_hat(0):
                        #Get hat values and send this as an event
                        hat_x, hat_y = self.joystick.get_hat(0)
                        hat_ev = events.HatMoved(hat_x, hat_y)
                        self.event_manager.post(hat_ev)
            #
            if self.joystick and self.joystick.get_numaxes() > 3:
                horiz_axis_pos, vert_axis_pos = self.get_axis_pos()
                offset_value_for_attack_req = 0.5
                if abs(horiz_axis_pos) > offset_value_for_attack_req or abs(vert_axis_pos) > offset_value_for_attack_req:
                    attack_request_ev = events.MouseButtonDown()
                    self.event_manager.post(attack_request_ev)

    def get_axis_pos(self):
        """Get Axis position. When no joystick connected, returns (0,0)
        """
        '''
        XBox game pad 2. axis: X 3, Y 4
        Sony game pad 2. axis: X 3, Y 2
        '''
        horiz_axis_pos = 0
        vert_axis_pos = 0
        if self.joystick and self.joystick.get_numaxes() > 3:
            horiz_axis_pos = self.joystick.get_axis(2)
            vert_axis_pos = self.joystick.get_axis(3)
        return(horiz_axis_pos, vert_axis_pos)
                        
