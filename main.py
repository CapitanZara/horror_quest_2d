import pygame
import sys

pygame.init()

end_game = False  # Флаг для обозначения конца игры

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Хоррор квест')

# Координаты и скорость персонажа
x, y = 50, 50
speed = 0.5

# Координаты и размер привидения
ghost_x, ghost_y = 300, 200  # Начальные координаты привидения
ghost_size = 50

# Определение локаций
locations = {
    'location1': {'items': [(100, 150, 90, 60), (300, 300, 50, 50)], 'message': ["Найден ключ", "Ты нашел зажигалку"]},
    'location2': {'items': [(200, 200, 70, 70), (400, 100, 60, 60)],
                  'message': ["Ты обнаружил загадочный свиток", "Ты нашел старинную монету"]},
    'location3': {'items': [(150, 100, 70, 70), (450, 350, 60, 60)],
                  'message': ["Ты нашел старинный фонарь", "Ты услышал странный шепот"]}

}

# Координаты и размер привидения
ghost_x, ghost_y = 150, 200  # Поместим привидение в третью комнату
ghost_size = 50

# Направление и скорость движения привидения
ghost_speed = 1
ghost_direction = 1  # 1 для движения вправо, -1 для движения влево

# Текущая локация
current_location = 'location1'

# Порталы для перемещения между локациями
portals = {
    'location1': (550, 400, 50, 50, 'location2'),
    'location2': (50, 400, 50, 50, 'location1'),
    'location2': (550, 100, 50, 50, 'location3'),
    'location3': (50, 400, 50, 50, 'location1')
}

font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = max(0, x - speed)  # Не позволяем x быть меньше 0
    if keys[pygame.K_RIGHT]:
        x = min(width - 50, x + speed)  # Не позволяем x быть больше ширины экрана минус ширина спрайта
    if keys[pygame.K_UP]:
        y = max(0, y - speed)  # Не позволяем y быть меньше 0
    if keys[pygame.K_DOWN]:
        y = min(height - 50, y + speed)  # Не позволяем y быть больше высоты экрана минус высота спрайта

    # Определяем прямоугольник персонажа здесь
    player_rect = pygame.Rect(x, y, 50, 50)

    # Логика движения привидения
    if current_location == 'location3':
        ghost_x += ghost_speed * ghost_direction
        # Изменяем направление, если привидение достигло края комнаты
        if ghost_x + ghost_size > width or ghost_x < 0:
            ghost_direction *= -1

    screen.fill((0, 0, 0))

    # Проверка столкновений с привидением
    if current_location == 'location3' and not end_game:
        player_rect = pygame.Rect(x, y, 50, 50)
        ghost_rect = pygame.Rect(ghost_x, ghost_y, ghost_size, ghost_size)
        if player_rect.colliderect(ghost_rect):
            end_game = True  # Устанавливаем флаг конца игры

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

    # Рисуем привидение только в третьей комнате
    if current_location == 'location3':
        pygame.draw.rect(screen, (100, 100, 255), (ghost_x, ghost_y, ghost_size, ghost_size))

        # Рисуем персонажа
    if not end_game:
        # Рисуем персонажа, если игра не завершена
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
    else:
        # Отображаем сообщение о конце игры
        end_text = font.render("Вас задушили, конец игры", True, (255, 255, 255))
        screen.blit(end_text, (width // 2 - end_text.get_width() // 2, height // 2 - end_text.get_height() // 2))

    # Проверка столкновений с порталами
    if portal_rect.collidepoint(x + 25, y + 25):  # Если персонаж вступил в портал
        x, y = 50, 50  # Стартовая позиция в новой локации
        current_location = portal_info[4]  # Изменяем текущую локацию

    pygame.display.flip()

    # Если игра завершена, останавливаем основной цикл
    if end_game:
        pygame.time.wait(3000)  # Задержка перед выходом, чтобы игрок увидел сообщение
        running = False

pygame.quit()
sys.exit()
