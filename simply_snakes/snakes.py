#!/usr/bin/env python

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import (ListProperty,
                             NumericProperty,
                             ObjectProperty,
                             ReferenceListProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector


class SnakesGame(Widget):
    """The root `Widget` for displaying and running the game."""

    trails = ListProperty()
    snake1 = ObjectProperty()
    snake2 = ObjectProperty()
    status_bar = ObjectProperty()

    def __init__(self, **kwargs):
        super(SnakesGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 's':
            if self.snake1.direction != [0, 1]:
                self.snake1.direction = (0, -1)
        elif keycode[1] == 'w':
            if self.snake1.direction != [0, -1]:
                self.snake1.direction = (0, 1)
        elif keycode[1] == 'a':
            if self.snake1.direction != [1, 0]:
                self.snake1.direction = (-1, 0)
        elif keycode[1] == 'd':
            if self.snake1.direction != [-1, 0]:
                self.snake1.direction = (1, 0)
        elif keycode[1] == 'down':
            if self.snake2.direction != [0, 1]:
                self.snake2.direction = (0, -1)
        elif keycode[1] == 'up':
            if self.snake2.direction != [0, -1]:
                self.snake2.direction = (0, 1)
        elif keycode[1] == 'left':
            if self.snake2.direction != [1, 0]:
                self.snake2.direction = (-1, 0)
        elif keycode[1] == 'right':
            if self.snake2.direction != [-1, 0]:
                self.snake2.direction = (1, 0)

    def run(self):
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        """Moves snakes and gives points if collision occured."""
        if self.snake1.move(self.snake2):
            self.snake2.score += 1
            self.reset()
        elif self.snake2.move(self.snake1):
            self.snake1.score += 1
            self.reset()

    def reset(self):
        """Resets the positions/directions and removes trails."""
        self.snake1.center = (self.width/3., self.height/2.)
        self.snake2.center = (self.width*2/3., self.height/2.)
        self.snake1.direction = (0, 0)
        self.snake2.direction = (0, 0)

        for trail in self.trails:
            self.remove_widget(trail)
        del self.trails[:]


class Snake(Widget):
    """Represents the head of a snake, which can be moved around."""

    color = ListProperty()
    direction_x = NumericProperty()
    direction_y = NumericProperty()
    direction = ReferenceListProperty(direction_x, direction_y)
    trail = ObjectProperty()
    score = NumericProperty()

    def collide_widget(self, wid):
        """Collision detection that works with negative sizes.

        Args:
            wid: The `Widget` to check for collision against.

        Returns:
            True if a collision occured, otherwise False.

        """
        if wid.width < 0:
            if self.right < wid.right + 1:
                return False
            if self.x > wid.x - 1:
                return False
        else:
            if self.right < wid.x + 1:
                return False
            if self.x > wid.right - 1:
                return False

        if wid.height < 0:
            if self.top < wid.top + 1:
                return False
            if self.y > wid.y - 1:
                return False
        else:
            if self.top < wid.y + 1:
                return False
            if self.y > wid.top - 1:
                return False

        return True

    def move(self, other):
        """Moves the `Snake` and returns whether a collision occured."""
        # Scale speed in relation to game widget size
        if self.parent.width < self.parent.height:
            speed_scale = self.parent.width / 250.
        else:
            speed_scale = self.parent.height / 250.

        self.pos = Vector(self.direction) * speed_scale + self.pos
        if self.trail:
            self.trail.width += self.direction_x * speed_scale
            self.trail.height += self.direction_y * speed_scale

        # Check for collision with edges of arena and other snake
        if self.right >= self.parent.width or self.x <= 0:
            return True
        if self.top >= self.parent.status_bar.y or self.y <= 0:
            return True
        if self.collide_widget(other):
            self.score += 1  # Gives point to self as well
            return True

        # Check for collision with all trails
        for trail in self.parent.trails:
            if self.collide_widget(trail):
                return True
        return False

    def on_direction(self, snake, direction):
        """Creates and positions a new trail."""
        self.trail = Trail(size=self.size, pos=self.pos, color=self.color)

        # Position trail for following directly behind snake head
        if self.direction_x == 1:
            self.trail.width = 0
        elif self.direction_x == -1:
            self.trail.width = 0
            self.trail.x = self.right
        elif self.direction_y == 1:
            self.trail.height = 0
        elif self.direction_y == -1:
            self.trail.height = 0
            self.trail.y = self.top

        self.parent.add_widget(self.trail)
        self.parent.trails.append(self.trail)


class Trail(Widget):
    """Represents a trail left behind as the `Snake` moves."""

    color = ListProperty()


class StatusBar(BoxLayout):
    """A container for displaying scores."""

    pass


class SnakesApp(App):
    def build(self):
        """Creates and runs the game."""
        Config.set('kivy', 'exit_on_escape', '0')
        game = SnakesGame()
        game.run()
        return game


def main():
    SnakesApp().run()


if __name__ == '__main__':
    main()
