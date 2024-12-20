import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置中文字体
try:
    font_path = pygame.font.match_font('simhei')  # 黑体
    if not font_path:
        font_path = pygame.font.match_font('microsoftyaheimicrosoftyaheiui')  # 微软雅黑
    if not font_path:
        font_path = pygame.font.match_font('simsun')  # 宋体
    if not font_path:
        font_path = "C:/Windows/Fonts/simhei.ttf"  # 直接指定黑体路径
except:
    font_path = None

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 计算游戏区域的位置使其居中
GAME_AREA_X = (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GAME_AREA_Y = (WINDOW_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.new_piece()
        self.fall_time = pygame.time.get_ticks()
        self.fall_speed = 500  # 初始下落速度（毫秒）
        self.level = 1

    def new_piece(self):
        # 随机选择一个新方块
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }

    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True

    def add_piece_to_board(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    if self.current_piece['y'] + i < 0:
                        self.game_over = True
                        return
                    self.board[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']

    def remove_complete_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.board[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2 - 1][:]
                self.board[0] = [0] * GRID_WIDTH
            else:
                y -= 1
        
        if lines_cleared:
            self.score += (lines_cleared * 100) * self.level
            self.level = self.score // 1000 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 50)

    def rotate_piece(self):
        # 创建新的旋转后的形状
        new_shape = list(zip(*reversed(self.current_piece['shape'])))
        new_piece = {
            'shape': new_shape,
            'color': self.current_piece['color'],
            'x': self.current_piece['x'],
            'y': self.current_piece['y']
        }
        if self.valid_move(new_piece, new_piece['x'], new_piece['y']):
            self.current_piece = new_piece

    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制游戏区域边框
        pygame.draw.rect(self.screen, WHITE, 
                        (GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                         GRID_WIDTH * BLOCK_SIZE + 4, 
                         GRID_HEIGHT * BLOCK_SIZE + 4), 2)

        # 绘制已固定的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(self.screen, self.board[y][x],
                                   (GAME_AREA_X + x * BLOCK_SIZE,
                                    GAME_AREA_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制当前方块
        if not self.game_over:
            for i in range(len(self.current_piece['shape'])):
                for j in range(len(self.current_piece['shape'][0])):
                    if self.current_piece['shape'][i][j]:
                        pygame.draw.rect(self.screen, self.current_piece['color'],
                                       (GAME_AREA_X + (self.current_piece['x'] + j) * BLOCK_SIZE,
                                        GAME_AREA_Y + (self.current_piece['y'] + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制分数和等级
        font = pygame.font.Font(font_path, 36) if font_path else pygame.font.Font(None, 36)
        score_text = font.render(f'分数: {self.score}', True, WHITE)
        level_text = font.render(f'等级: {self.level}', True, WHITE)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 60))

        if self.game_over:
            game_over_font = pygame.font.Font(font_path, 48) if font_path else pygame.font.Font(None, 48)
            game_over_text = game_over_font.render('游戏结束!', True, RED)
            restart_text = game_over_font.render('按R重新开始', True, WHITE)
            self.screen.blit(game_over_text, 
                           (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                            WINDOW_HEIGHT//2 - 50))
            self.screen.blit(restart_text, 
                           (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                            WINDOW_HEIGHT//2 + 10))

        pygame.display.flip()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, 
                                            self.current_piece['x'] - 1, 
                                            self.current_piece['y']):
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, 
                                            self.current_piece['x'] + 1, 
                                            self.current_piece['y']):
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, 
                                            self.current_piece['x'], 
                                            self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece, 
                                                self.current_piece['x'], 
                                                self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1

            if not self.game_over:
                # 自动下落
                if current_time - self.fall_time > self.fall_speed:
                    if self.valid_move(self.current_piece, 
                                     self.current_piece['x'], 
                                     self.current_piece['y'] + 1):
                        self.current_piece['y'] += 1
                    else:
                        self.add_piece_to_board()
                        self.remove_complete_lines()
                        self.new_piece()
                        if not self.valid_move(self.current_piece, 
                                             self.current_piece['x'], 
                                             self.current_piece['y']):
                            self.game_over = True
                    self.fall_time = current_time

            self.draw()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Tetris()
    game.run()
