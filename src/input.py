import pygame


class InputManager:
    def __init__(self):
        self.keys_down = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        self.quit = False

    def update(self):
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                self.keys_down.add(event.key)
                self.keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_down.discard(event.key)
                self.keys_just_released.add(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.mouse_buttons = (
                    event.button == 1,
                    event.button == 2,
                    event.button == 3,
                )
                self.mouse_pos = (x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons = (False, False, False)

    def is_key_down(self, key):
        return key in self.keys_down

    def is_key_pressed(self, key):
        return key in self.keys_just_pressed

    def is_key_released(self, key):
        return key in self.keys_just_released
