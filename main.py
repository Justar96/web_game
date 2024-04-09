import numpy as np
import pygame
from math import *
import asyncio

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]
angle = 0

points = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            points.append(np.matrix([x, y, z]))

print(points)

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i,j,points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()

async def main():
    global angle
    while True:
        i = 0
        angle += 0.01
        screen.fill(WHITE)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)],
        ])
        rotation_y = np.matrix([
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)],
        ]) 
        rotation_z = np.matrix([
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1],
        ])
 
        for point in points:
            rotated_2d = np.dot(rotation_x, point.reshape((3, 1)))
            rotated_2d = np.dot(rotation_y, rotated_2d)
            rotated_2d = np.dot(rotation_z, rotated_2d)


            
            projected_2d = np.dot(projection_matrix, rotated_2d)
            x = int(projected_2d[0][0] * scale) + circle_pos[0]
            y = int(projected_2d[1][0] * scale) + circle_pos[1]        
            
            projected_points[i] = [x, y]
            pygame.draw.circle(screen, RED, (x,y), 5)
            i += 1
        
        connect_points(0,1,projected_points)
        connect_points(1,3,projected_points)
        connect_points(2,0,projected_points)
        connect_points(3,2,projected_points)
        
        connect_points(5,4,projected_points)
        connect_points(6,4,projected_points)
        connect_points(7,6,projected_points)
        connect_points(7,5,projected_points)

        connect_points(0,4,projected_points)
        connect_points(1,5,projected_points)
        connect_points(2,6,projected_points)
        connect_points(3,7,projected_points)
        
        pygame.display.update()
        await asyncio.sleep(0)
        
asyncio.run(main())