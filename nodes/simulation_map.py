import pygame
pygame.init()

screen = pygame.display.set_mode((1000, 600))

strip = pygame.image.load("yellow_strip.jpg")

strip_resized = pygame.transform.scale(strip, (25, 25))

white = (255, 255, 255)


road_size = 50
gray = (119, 119, 119)

def draw_road(x, y, scale_w = 1, scale_h = 1):
    return pygame.draw.rect(screen, gray, pygame.Rect(x, y, road_size*scale_w, road_size*scale_h))
    
def background():
    draw_road(100, 0, 1, 4)
    draw_road(0, 100, 12, 1)
    draw_road(600, 0, 1, 8)

screen.fill(white)
background()

pygame.display.update()
runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    pygame.display.flip()
