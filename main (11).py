import pygame
import sys
import serial

pygame.init()
screen = pygame.display.set_mode((700, 700))

ser = serial.Serial('COM5', 9600, timeout=0)  # Replace 'COM10' with your Arduino's serial port


class Player:
    def __init__(self, x, y, speed, color, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.size = size

    def render(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def up(self):
        self.y -= self.speed

    def down(self):
        self.y += self.speed

    def left(self):
        self.x -= self.speed

    def right(self):
        self.x += self.speed

player = Player(350, 350, 0.05, (0, 0, 0), 25)  # Increased speed for better movement

running = True

x = [0.0]
y = [0.0]

while running:
    data = ser.read(ser.inWaiting() or 1).decode('utf-8', errors='ignore')
    if data:
        try:
            x_value, y_value = map(float, data.split(','))
            x[0] = x_value
            y[0] = y_value
            print(data)
        except ValueError:
            pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if abs(x[0] - 0) < 0.1 and 2.5 <= y[0] <= 2.53:
        player.up()
    elif abs(x[0] - 5) < 0.1 and 2.5 <= y[0] <= 2.53:
        player.down()
    elif 2.5 <= x[0] <= 2.53 and abs(y[0] - 0) < 0.1:
        player.left()
    elif 2.5 <= x[0] <= 2.53 and abs(y[0] - 5) < 0.1:
        player.right()

    screen.fill((255, 255, 255))
    player.render()
    pygame.display.flip()

pygame.quit()
sys.exit()
