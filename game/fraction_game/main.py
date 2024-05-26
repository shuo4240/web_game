import pygame as pg
from sys import exit
import asyncio

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LIGHT_CYAN = (224, 255, 255)

# 進入關卡的按鈕
class level_Button():
    def __init__(self, left, top, width, height, text):
        self.text = text
        self.rect = pg.Rect(left, top, width, height)
        self.font = pg.font.SysFont('arial', 32)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0)) #(文字, 平滑值, 文字顏色)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.active = False

    def draw_btn(self, canvas):
        if self.active:
            pg.draw.rect(canvas, (255, 255, 51), self.rect, 0) #(畫布, 顏色, [x坐標, y坐標, 寬度, 高度], 線寬)
        else:
            pg.draw.rect(canvas, (255, 255, 153), self.rect, 0)
        canvas.blit(self.text_surface, self.text_rect)

    def play_correct(self):
        correct_sound = pg.mixer.Sound(r"C:\myProject\flaskProject\game_media\correct.ogg")
        correct_sound.set_volume(0.2)
        correct_sound.play()

    def play_wrong(self):
        wrong_sound = pg.mixer.Sound(r"C:\myProject\flaskProject\game_media\error.ogg")
        wrong_sound.set_volume(0.2)
        wrong_sound.play()

    def play_otherBtn(self):
        otherBtn_sound = pg.mixer.Sound(r"C:\myProject\Web\app\static\game_media\other_btn.ogg")
        otherBtn_sound.set_volume(0.2)
        otherBtn_sound.play()


class image_Button():
    def __init__(self, img_name, img_address, img_address_clicked, top, left):
        self.img_name = img_name
        self.image = pg.image.load(img_address)
        self.img_clicked = pg.image.load(img_address_clicked)
        self.img_width = 100
        self.img_height = 100
        self.rect = pg.Rect(left, top, self.img_width, self.img_height)
        self.rect.topleft = (top, left)
        self.active = False
    
    def draw(self, screen):
        if self.active:
            self.scaled_image = pg.transform.scale(self.image, (self.img_width, self.img_height))
            screen.blit(self.scaled_image, (self.rect.topleft))
        else:
            self.scaled_image = pg.transform.scale(self.img_clicked, (self.img_width, self.img_height))
            screen.blit(self.scaled_image, (self.rect.topleft))
            
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def play_correct(self):
        correct_sound = pg.mixer.Sound(r"C:\myProject\Web\app\static\game_media\correct.ogg")
        correct_sound.set_volume(0.2)
        correct_sound.play()

    def play_wrong(self):
        wrong_sound = pg.mixer.Sound(r"C:\myProject\Web\app\static\game_media\error.ogg")
        wrong_sound.set_volume(0.2)
        wrong_sound.play()

    def play_otherBtn(self):
        otherBtn_sound = pg.mixer.Sound(r"C:\myProject\Web\app\static\game_media\other_btn.ogg")
        otherBtn_sound.set_volume(0.2)
        otherBtn_sound.play()


async def main():
    await menu()

# Game Menu
async def menu():
    pg.init()
    pg.mixer.init()

    # 創建視窗
    width, height = 1200, 800
    screen = pg.display.set_mode((width, height))
    screen.fill(LIGHT_CYAN)

    pg.display.set_caption("Menu")
    type1_level = [] # game type1
    for i in range(0, 5):
        type1_level.append(level_Button(100 + 200 * i, 100, 150, 250, "Level " + str(i + 1)))
        type1_level[i].draw_btn(screen)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for btn in type1_level:
                    if btn.rect.collidepoint(event.pos):
                        btn.active = True
                        btn.draw_btn(screen)
            if event.type == pg.MOUSEBUTTONUP:
                for btn in type1_level:
                    if btn.rect.collidepoint(event.pos):
                        btn.active = False
                        btn.draw_btn(screen)
                        if btn == type1_level[0]:
                            btn.play_otherBtn()
                            await game_type1(1, 530, "4", "10", 40, 20, 4, 9, screen)
                        elif btn == type1_level[1]:
                            btn.play_otherBtn()
                            await game_type1(2, 600, "3", "4", 100, 25, 1, 7, screen)
                        elif btn == type1_level[2]:
                            await game_type1(3, 625, "7", "8", 25, 50, 7, 3, screen)
                        elif btn == type1_level[3]:
                            await game_type1(4, 450 + (400 / 3), "2", "3", (200 / 3), (200 / 6), 2, 5, screen)
                        elif btn == type1_level[4]:
                            await game_type1(5, 450 + (500 / 6), "5", "12", (200 / 6), (200 / 4), 5, 3, screen)
        pg.display.update()
        await asyncio.sleep(0)


async def display_text(canvas, numerator, denominator):
    font = pg.font.SysFont("simhei", 150)
    text_numer = font.render(numerator, True, BLACK, LIGHT_CYAN)
    text_denominator = font.render(denominator, True, BLACK, LIGHT_CYAN)

    canvas.blit(text_numer, (890, 140))
    pg.draw.line(canvas, BLACK, (850, 250), (1000, 250), 10)
    if int(denominator) > 9:
        canvas.blit(text_denominator, (865, 270))
    else:
        canvas.blit(text_denominator, (890, 270))


async def draw_dashLine(canvas, start_point, end_point):
    dash_length = 5
    gap_length = 5
    line_thickness = 2

    x1, y1 = start_point
    x2, y2 = end_point
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    dx = dx / distance
    dy = dy / distance

    x, y = x1, y1
    for i in range(int(distance / (dash_length + gap_length))):
        pg.draw.line(canvas, GRAY, (x, y), (x + dx * dash_length, y + dy * dash_length), line_thickness)
        x += dx * (dash_length + gap_length)
        y += dy * (dash_length + gap_length)


# game_type1
async def game_type1(level, problem, numerator, denominator, rect1_width, rect2_width, split_line_num1, split_line_num2, screen):
    pg.init()
    pg.mixer.init()

    screen.fill(LIGHT_CYAN)

    await display_text(screen, numerator, denominator)

    start_pointX = 450
    start_pointY = 350
    answerBlock_width = 200
    answerBlock_height = 70
    pg.draw.rect(screen, WHITE, [start_pointX, start_pointY, answerBlock_width, answerBlock_height])
    pg.draw.rect(screen, BLACK, [start_pointX, start_pointY, answerBlock_width, answerBlock_height], 2)

    rect1_pointX = 300
    rect1_pointY = 650
    rect2_pointX = 600
    rect2_pointY = 650
    rect_height = 70

    rect1_surr = pg.draw.rect(screen, WHITE, [rect1_pointX, rect1_pointY, rect1_width * (split_line_num1 + 1), rect_height])
    pg.draw.rect(screen, RED, [rect1_pointX, rect1_pointY, rect1_width, rect_height], 0)
    pg.draw.rect(screen, BLACK, [rect1_pointX, rect1_pointY, rect1_width * (split_line_num1 + 1), rect_height], 2)
    for n in range(1, (split_line_num1 + 1)):
        await draw_dashLine(screen, (rect1_pointX + rect1_width * n, rect1_pointY), (rect1_pointX + rect1_width * n, rect1_pointY + rect_height))

    rect2_surr = pg.draw.rect(screen, WHITE, [rect2_pointX, rect2_pointY, rect2_width * (split_line_num2 + 1), rect_height])
    pg.draw.rect(screen, GREEN, [rect2_pointX, rect2_pointY, rect2_width, rect_height], 0)
    pg.draw.rect(screen, BLACK, [rect2_pointX, rect2_pointY, rect2_width * (split_line_num2 + 1), rect_height], 2)
    for n in range(1, (split_line_num2 + 1)):
        await draw_dashLine(screen, (rect2_pointX + rect2_width * n, rect2_pointY), (rect2_pointX + rect2_width * n, rect2_pointY + rect_height))

    all_btn = []
    Restart_button = image_Button("Restart", r"C:\myProject\Web\app\static\game_image\restart_clicked.png", r"C:\myProject\Web\app\static\game_image\restart.png", 100, 100)
    all_btn.append(Restart_button)
    Restart_button.draw(screen)

    Menu_button = image_Button("Menu", r"C:\myProject\Web\app\static\game_image\GoToMenu_clicked.png", r"C:\myProject\Web\app\static\game_image\GoToMenu.png", 100, 200)
    all_btn.append(Menu_button)
    Menu_button.draw(screen)

    Submit_button = image_Button("Submit", r"C:\myProject\Web\app\static\game_image\tick_clicked.png", r"C:\myProject\Web\app\static\game_image\tick.png", 100, 300)
    all_btn.append(Submit_button)
    Submit_button.draw(screen)

    Next_button = image_Button("Next", r"C:\myProject\Web\app\static\game_image\Next_clicked.png", r"C:\myProject\Web\app\static\game_image\Next.png", 800, 500)
    all_btn.append(Next_button)

    num1 = 0
    num2 = 0
    locaX = 450

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if rect1_surr.collidepoint(event.pos):
                    pg.draw.rect(screen, RED, [locaX, start_pointY, rect1_width, rect_height], 0)
                    pg.draw.rect(screen, BLACK, [start_pointX, start_pointY, answerBlock_width, answerBlock_height], 2)
                    locaX += rect1_width
                if rect2_surr.collidepoint(event.pos):
                    pg.draw.rect(screen, GREEN, [locaX, start_pointY, rect2_width, rect_height], 0)
                    pg.draw.rect(screen, BLACK, [start_pointX, start_pointY, answerBlock_width, answerBlock_height], 2)
                    locaX += rect2_width

            if event.type == pg.MOUSEBUTTONDOWN:
                for btn in all_btn:
                    mouse_pos = pg.mouse.get_pos()
                    if btn.is_clicked(mouse_pos):
                        btn.active = True
                        btn.draw(screen)

            if event.type == pg.MOUSEBUTTONUP:
                for btn in all_btn:
                    if btn.is_clicked(mouse_pos):
                        btn.active = False
                        btn.draw(screen)
                        if btn == Restart_button:
                            pg.draw.rect(screen, WHITE, [start_pointX, start_pointY, answerBlock_width, answerBlock_height], 0)
                            pg.draw.rect(screen, BLACK, [start_pointX, start_pointY, answerBlock_width, answerBlock_height], 2)
                            locaX = 450

                        elif btn == Submit_button:  # 提交答案並判斷是否正確
                            if abs(locaX - (450 + problem)) < 0.001:
                                btn.play_correct()
                                Next_button.draw(screen)
                                if level <= 4:
                                    level += 1
                                else:
                                    await menu()
                            else:
                                btn.play_wrong()

                        elif btn == Menu_button:
                            btn.play_otherBtn()
                            await menu()

                        elif btn == Next_button:
                            screen.fill(LIGHT_CYAN)
                            if level == 2:
                                await game_type1(2, 600, "3", "4", 100, 25, 1, 7, screen)
                            elif level == 3:
                                await game_type1(3, 625, "7", "8", 25, 50, 7, 3, screen)
                            elif level == 4:
                                await game_type1(4, 450 + (400 / 3), "2", "3", (200 / 3), (200 / 6), 2, 5, screen)
                            elif level == 5:
                                await game_type1(5, 450 + (500 / 6), "5", "12", (200 / 6), (200 / 4), 5, 3, screen)
        pg.display.update()
        await asyncio.sleep(0)


asyncio.run(main())
