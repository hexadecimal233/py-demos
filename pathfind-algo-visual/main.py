import pygame
import numpy as np
from queue import PriorityQueue

MAP_SIZE = 32  # map width 0-31

# 渲染设置
TILE_SIZE = 32
TILE_PADDING = 1

start = (0, 0)  # 左上角
goal = (MAP_SIZE - 1, MAP_SIZE - 1)  # 右下角
map_data = np.zeros((MAP_SIZE, MAP_SIZE))


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def hypot(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_neighbors(p):
    neighbors = [
        (p[0] + 1, p[1]),
        (p[0] - 1, p[1]),
        (p[0], p[1] + 1),
        (p[0], p[1] - 1),
    ]
    return [
        n
        for n in neighbors
        if (n[0] >= 0 and n[0] < MAP_SIZE and n[1] >= 0 and n[1] < MAP_SIZE)  # 边界内
        and map_data[n[0]][n[1]] == 0  # 非障碍
    ]


# 寻路，返回路径点和访问过的节点
def find_path():
    # 优先队列 (启发距离, 离起点距离, node, path)
    frontier = PriorityQueue()
    frontier.put((0, 0, start, [start]))

    # 存储已访问节点及其最短 g_score
    g_costs = {start: 0}

    # 已访问的节点集合 {node: (h, g)}
    visited = {}

    while not frontier.empty():
        # 获取分数最低的节点
        _, g, curr, path = frontier.get()

        if curr == goal:
            return path, visited

        # 遍历所有邻居
        for n in get_neighbors(curr):
            new_g = g + 1  # 新点离起点的距离

            if n not in g_costs or new_g < g_costs[n]:
                g_costs[n] = new_g
                h = manhattan_distance(n, goal)
                f = new_g + h
                frontier.put((f, new_g, n, path + [n]))
                visited.update({curr: new_g})  # 添加到已访问集合，可视化

    # 如果没有找到路径
    return [], visited


pygame.init()
screen = pygame.display.set_mode((MAP_SIZE * TILE_SIZE, MAP_SIZE * TILE_SIZE))
font = pygame.font.SysFont("GuanZhi", 16)
clock = pygame.time.Clock()


def draw_tile(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        (
            x * TILE_SIZE + TILE_PADDING,
            y * TILE_SIZE + TILE_PADDING,
            TILE_SIZE - TILE_PADDING * 2,
            TILE_SIZE - TILE_PADDING * 2,
        ),
    )


def draw_text(x, y, color, text):
    for t in text.split("\n"):
        text_surface = font.render(t, True, color)
        screen.blit(text_surface, (x, y))
        y += font.get_height()


# 绘制地图
def draw_map(path, visited):
    screen.fill("gray")
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            # 绘制玩家
            if start[0] == x and start[1] == y:
                draw_tile(x, y, "red")
                continue
            # 绘制终点
            elif goal[0] == x and goal[1] == y:
                draw_tile(x, y, "green")
                continue
            # 绘制障碍
            elif map_data[x][y] == 1:
                draw_tile(x, y, "white")
            # 绘制路径
            elif (x, y) in path:
                draw_tile(x, y, "yellow")
                curr = visited.get((x, y))
                draw_text(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    "blue",
                    f"{curr}",
                )
                continue
            # 绘制访问过的节点
            elif (x, y) in visited:
                draw_tile(x, y, "orange")
                curr = visited.get((x, y))
                draw_text(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    "blue",
                    f"{curr}",
                )
                continue
            # 绘制空地
            else:
                draw_tile(x, y, "black")


path, visited = find_path()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = mouse_x // TILE_SIZE
            y = mouse_y // TILE_SIZE

            if event.button == pygame.BUTTON_LEFT:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    goal = (x, y)  # shift终点
                elif pygame.key.get_pressed()[pygame.K_LCTRL]:
                    start = (x, y)  # ctrl起点
                else:
                    map_data[x][y] = 1 if map_data[x][y] == 0 else 0  # 左键障碍

            # 更新寻路
            path, visited = find_path()

    draw_map(path, visited)
    pygame.display.flip()
    # 绘制地图
    clock.tick(60)  # 60 帧显示
