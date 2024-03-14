import pygame
import sys

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Хоррор квест')

# Координаты и скорость персонажа
x, y = 50, 50
speed = 0.5

# Определение локаций
locations = {
    'location1': {'items': [(100, 150, 90, 60), (300, 300, 50, 50)], 'message': ["Найден ключ", "Ты нашел зажигалку"]},
    'location2': {'items': [(200, 200, 70, 70), (400, 100, 60, 60)],
                  'message': ["Ты обнаружил загадочный свиток", "Ты нашел старинную монету"]}
}

# Текущая локация
current_location = 'location1'

# Порталы для перемещения между локациями
portals = {'location1': (550, 400, 50, 50, 'location2'), 'location2': (50, 400, 50, 50, 'location1')}

font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    screen.fill((0, 0, 0))

    # Рисуем предметы текущей локации
    message = None
    for idx, item in enumerate(locations[current_location]['items']):
        rect = pygame.draw.rect(screen, (0, 255, 0), item)
        if rect.collidepoint(x, y):
            message = locations[current_location]['message'][idx]

    if message:
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (10, 10))

    # Рисуем портал
    portal_info = portals[current_location]
    portal_rect = pygame.draw.rect(screen, (0, 0, 255), portal_info[:4])

        # Рисуем персонажа
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))

    # Проверка столкновений с порталами
    if portal_rect.collidepoint(x + 25, y + 25):  # Если персонаж вступил в портал
        x, y = 50, 50  # Стартовая позиция в новой локации
        current_location = portal_info[4]  # Изменяем текущую локацию

    pygame.display.flip()


pygame.quit()
sys.exit()
