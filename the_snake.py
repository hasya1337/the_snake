import pygame
from random import randint, choice

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()

# Базовые позиции и цвет для игровых объектов
DEFAULT_POSITION = (0, 0)
DEFAULT_COLOR = (255, 255, 255)

class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=DEFAULT_POSITION, color=DEFAULT_COLOR):
        """
        Инициализирует объект игры.

        :param position: начальная позиция объекта
        :param color: цвет объекта
        """
        self.position = position
        self.body_color = color

    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position[0], self.position[1],
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, color=APPLE_COLOR):
        """Инициализирует яблоко с случайной позицией на игровом поле."""
        super().__init__(color=color)
        self.randomize_position()

    def randomize_position(self):
        """Перемещает яблоко на новую случайную позицию."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализирует змейку."""
        super().__init__(color=color)
        self.reset()

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        :return: координаты головы змейки
        """
        return self.positions[0]

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if (new_direction[0] * self.direction[0] == 0
                and new_direction[1] * self.direction[1] == 0):
            self.direction = new_direction

def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    :param snake: объект змейки
    """
    key_mapping = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in key_mapping:
                snake.update_direction(key_mapping[event.key])

def main():
    """Основная функция игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            while True:
                apple.randomize_position()
                if apple.position not in snake.positions:
                    break

        # Проверка на столкновение змейки с самой собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
