import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
# screen initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

class Paddle:
    VEL = 5  # paddle velocity
    
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, direction=1):
        self.x = self.x + self.VEL * direction

class Ball:
    VEL = 5
    
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color  # Fixed: removed extra space
        self.x_vel = 0
        self.y_vel = -self.VEL
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y, width, height, health, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide(self, ball):
        if not(ball.x <= self.x + self.width and ball.x >= self.x):
            return False
        if not(ball.y - BALL_RADIUS <= self.y + self.height):
            return False
        self.hit()
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True
    
    def hit(self):
        self.health -= 1

    
    
        
        
def draw(screen, paddle, ball, bricks):
    screen.fill("white")
    paddle.draw(screen)
    ball.draw(screen)

    for brick in bricks:
        brick.draw(screen)
    pygame.display.update()

def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
    if ball.y + BALL_RADIUS >= HEIGHT or ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)

def ball_paddle_collision(ball, paddle):
    if not(ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
        return
    if not(ball.y + BALL_RADIUS >= paddle.y):
        return
    
    paddle.centre = paddle.x + paddle.width/2
    distance_to_centre = paddle.centre - ball.x

    percent_width = distance_to_centre / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL

    ball.set_vel(x_vel, -y_vel)

def generate_bricks(rows, cols):
    gap = 2
    brick_width = (WIDTH // cols) - gap
    brick_height = 30

    bricks = []
    for row in range(rows):
        for col in range(cols):
            x = col * (brick_width + gap)
            y = row * (brick_height + gap)
            brick = Brick(col * brick_width + gap * col, row * brick_height + gap * row, brick_width, brick_height, 1, 'black')
            bricks.append(brick)

    return bricks



def main():
    clock = pygame.time.Clock()
    
    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2  # Use integer division
    paddle_y = HEIGHT - PADDLE_HEIGHT - 5
    
    paddle = Paddle(paddle_x, HEIGHT - PADDLE_HEIGHT - 5, PADDLE_WIDTH, PADDLE_HEIGHT, 'black')
    ball = Ball(paddle_x + PADDLE_WIDTH // 2, paddle_y - BALL_RADIUS, BALL_RADIUS, 'black')
    bricks = generate_bricks(3, 10)
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
            paddle.move(-1)
        if keys[pygame.K_RIGHT] and paddle.x + PADDLE_WIDTH + paddle.VEL <= WIDTH:
            paddle.move(1)
        
        ball.move()
        ball_collision(ball)
        ball_paddle_collision(ball, paddle)
        
        bricks_to_delete = []
        for brick in bricks[:]:
            brick.collide(ball)

            if brick.health <= 0:
                 bricks.remove(brick)

        draw(screen, paddle, ball, bricks)
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()