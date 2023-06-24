import pygame
import random
import time as tm
import sqlite3 as sql

# SQL database connection
max_score = 0
connection = sql.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS scores(score)")
cursor.execute("INSERT INTO scores VALUES ('{}')".format(max_score))
connection.commit()
cursor.execute("SELECT * FROM scores")
data = cursor.fetchall()

# Pygame başlat
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Box Game Master")

# Renkler
rect_color = ["red", "blue", "yellow", "purple", (204, 0, 102), "green", "brown", (64, 224, 208), (128, 128, 128), "orange"]
color_index = random.randrange(len(rect_color))
x = random.randrange(100, 600)
y = random.randrange(100, 550)

# Sesler
sound1 = pygame.mixer.Sound("sound1.wav")
sound2 = pygame.mixer.Sound("sound2.wav")

# Zamanlayıcı ve puanlar
counter = random.randrange(3, 11)
clock = tm.time()
start_time = pygame.font.SysFont("Calibri", int(screen_height * 0.05))

score = 0
start_score = counter
score_text = pygame.font.SysFont("Calibri", int(screen_height * 0.05))
high_score = pygame.font.SysFont("Calibri", int(screen_height * 0.04))
high_score_rect = high_score.render("High Score: {}".format(data[0][0]), True, "black")
score_text_rect = score_text.render("Score:{}".format(str(score)), True, "black")

started = True
running = True

while running:
    if not started:
        screen.fill("white")
        start_time_cor = start_time.render("Timer: {}".format(round(120 - (tm.time() - clock)), 2), True, "black")
        cursor.execute("SELECT * FROM scores")
        data = cursor.fetchall()
        high_score_rect = high_score.render("High Score: {}".format(data[0][0]), True, "black")
        if round(120 - (tm.time() - clock)) <= 0:
            started = True
        box_size = int(screen_width * 0.2)
        box = pygame.draw.rect(color=rect_color[color_index], surface=screen, rect=(x, y, box_size, box_size), width=0, border_radius=10)
        box_letter = pygame.font.SysFont("Calibri", int(screen_height * 0.08))
        box_letter_rect = box_letter.render(str(counter), True, "white")
        score_text_rect = score_text.render("Score:{}".format(str(score)), True, "black")
        screen.blit(start_time_cor, (int(screen_width * 0.4), int(screen_height * 0.02)))
        screen.blit(box_letter_rect, (x + int(box_size * 0.15), y + int(box_size * 0.1)))
        screen.blit(score_text_rect, (int(screen_width * 0.015), int(screen_height * 0.015)))
        screen.blit(high_score_rect, (int(screen_width * 0.02), int(screen_height * 0.07)))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if (e.pos[0] > box.x and e.pos[0] < (box.x + box_size)) and (e.pos[1] > box.y and e.pos[1] < box.y + box_size):
                    if counter != 1:
                        sound1.play()
                        counter -= 1
                        box_letter_rect = box_letter.render(str(counter), True, "white")
                    else:
                        sound2.play()
                        score += start_score
                        counter = random.randrange(3, 11)
                        start_score = counter
                        if score > int(data[0][0]):
                            cursor.execute("UPDATE scores SET score='{}'".format(score))
                            connection.commit()
                        score_text_rect = score_text.render("Score:{}".format(str(score)), True, "black")
                        color_index = random.randrange(len(rect_color))
                        x = random.randrange(100, 600)
                        y = random.randrange(100, 550)
                        box = pygame.draw.rect(color=rect_color[color_index], surface=screen, rect=(x, y, box_size, box_size), width=0, border_radius=10)
                        box_letter_rect = box_letter.render(str(counter), True, "white")
    else:
        score = 0
        screen.fill("white")
        box_size = int(screen_width * 0.1)
        box1 = pygame.draw.rect(color=rect_color[color_index], surface=screen, rect=(int(screen_width * 0.125), int(screen_height * 0.15), box_size, box_size), width=0, border_radius=10)
        box_letter1 = pygame.font.SysFont("Calibri", int(screen_height * 0.08))
        box_letter_rect1 = box_letter1.render(str(counter), True, "white")
        box2 = pygame.draw.rect(color="green", surface=screen, rect=(int(screen_width * 0.525), int(screen_height * 0.61), box_size, box_size), width=0, border_radius=10)
        box_letter2 = pygame.font.SysFont("Calibri", int(screen_height * 0.08))
        box_letter_rect2 = box_letter2.render("2", True, "white")
        letter = pygame.font.SysFont("Calibri", int(screen_height * 0.08))
        letter_cor = letter.render("Let's Play", True, "black")
        rect = pygame.draw.rect(surface=screen, color="red", rect=(int(screen_width * 0.425), int(screen_height * 0.5), int(screen_width * 0.15), int(screen_height * 0.08)), width=0, border_radius=15)
        inner_text = pygame.font.SysFont("Calibri", int(screen_height * 0.03))
        inner_text_cor = inner_text.render("Start", True, "white")
        screen.blit(letter_cor, (int(screen_width * 0.3), int(screen_height * 0.37)))
        screen.blit(inner_text_cor, (int(screen_width * 0.47), int(screen_height * 0.515)))
        screen.blit(box_letter_rect1, (int(screen_width * 0.155), int(screen_height * 0.18)))
        screen.blit(box_letter_rect2, (int(screen_width * 0.565), int(screen_height * 0.67)))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if (e.pos[0] > rect.x and e.pos[0] < (rect.x + rect.width)) and (e.pos[1] > rect.y and e.pos[1] < (rect.y + rect.height)):
                    clock = tm.time()
                    started = False
                    score = 0

pygame.quit()

