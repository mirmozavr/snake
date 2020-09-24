import pygame, sys, random, pygame_menu
pygame.init()
FRAME_COLOR = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
BLACK = (5, 5, 5)
BLOCK_SIZE = 20
COUNT_BLOCK = 20
SNAKE_COLOR = (0, 102, 0)
MARGIN = 1
HEADER_MARGIN = 50
size = (BLOCK_SIZE * COUNT_BLOCK + 2 * BLOCK_SIZE + MARGIN * COUNT_BLOCK,
        BLOCK_SIZE * COUNT_BLOCK + 2 * BLOCK_SIZE + HEADER_MARGIN + MARGIN * COUNT_BLOCK)
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SNAKE')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)
bg_image = pygame.image.load('snake.jpg')

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x<COUNT_BLOCK and 0<= self.y<COUNT_BLOCK

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

    # def collision(self):
    #     return SnakeBlock(self.x, self.y) in snake_blocks





def draw_block(color, row, column):
    pygame.draw.rect(screen, color,
     [20 + BLOCK_SIZE * column + MARGIN * (column + 1),
      HEADER_MARGIN + 20 + BLOCK_SIZE * row + MARGIN * (row + 1), BLOCK_SIZE, BLOCK_SIZE])


def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCK - 1)
        y = random.randint(0, COUNT_BLOCK - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            x = random.randint(0, COUNT_BLOCK - 1)
            y = random.randint(0, COUNT_BLOCK - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()



    d_row = 0
    d_col = 1
    score = 0
    speed = 5
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)

        text_score = courier.render(f"Score: {score}", 0, BLACK)
        screen.blit(text_score, (BLOCK_SIZE, BLOCK_SIZE))

        for row in range(COUNT_BLOCK):
            for column in range(COUNT_BLOCK):
                if (column + row) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)


        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            # pygame.quit()
            # sys.exit()
            break


        draw_block(RED, apple.x, apple.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            score += 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('collision')
            # pygame.quit()
            # sys.exit()
            break


        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        speed = score // 5 + 3
        pygame.display.flip()
        timer.tick(speed)

my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.set_background_color_opacity(0.9)

menu = pygame_menu.Menu(300, 250, 'Snake!', theme=my_theme)
menu.add_text_input('Name :', default='Bobby')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


while True:

    screen.blit(bg_image, (0,0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()