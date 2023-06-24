import pygame
import random
import time as tm
import sqlite3 as sql

#sql database connection
max_score=0
connection=sql.connect("database.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS scores(score)")
cursor.execute("INSERT INTO scores VALUES ('{}')".format(max_score))
connection.commit()
cursor.execute("SELECT * FROM scores")
data=cursor.fetchall()


pygame.init()
screen=pygame.display.set_mode((500,650))
pygame.display.set_caption("Box Game Master")
rect_color=["red","blue","yellow","purple",(204,0,102),"green","brown",(64,224,208),(128,128,128),"orange"]
color_index=random.randrange(len(rect_color))
x=random.randrange(100,400)
y=random.randrange(100,550)

#sounds
sound1=pygame.mixer.Sound("sound1.wav")
sound2=pygame.mixer.Sound("sound2.wav")


counter=random.randrange(3,11)
clock=tm.time()
start_time=pygame.font.SysFont("Calibri",40)

score=0
start_score=counter
score_text=pygame.font.SysFont("Calibri",40)
high_score=pygame.font.SysFont("Calibri",25)
high_score_rect=high_score.render("High Score: {}".format(data[0][0]),True,"black")
score_text_rect=score_text.render("Score:{}".format(str(score)),True,"black")

started=True
running=True

print(cursor.fetchall())
while running:
    if not(started):
        screen.fill("white")
        start_time_cor=start_time.render("timer: {}".format(round(120-(tm.time()-clock)),2),True,"black")
        cursor.execute("SELECT * FROM scores")
        data=cursor.fetchall()
        high_score_rect=high_score.render("High Score: {}".format(data[0][0]),True,"black")
        if(round(120-(tm.time()-clock))<=0):
            started=True
        box=pygame.draw.rect(color=rect_color[color_index],surface=screen,rect=(x,y,100,100),width=0,border_radius=10)
        box_letter=pygame.font.SysFont("Calibri",60)
        box_letter_rect=box_letter.render(str(counter),True,"white")
        score_text_rect=score_text.render("Score:{}".format(str(score)),True,"black")
        screen.blit(start_time_cor,(250,10))
        screen.blit(box_letter_rect,(x+15,y+10))
        screen.blit(score_text_rect,(10,10))
        screen.blit(high_score_rect,(10,50))
        pygame.display.update()
        for e in pygame.event.get():
            if(e.type==pygame.QUIT):
                running=False
            if(e.type==pygame.MOUSEBUTTONDOWN):
                if((e.pos[0]>box.x and e.pos[0]<(box.x+100)) and (e.pos[1]>box.y and e.pos[1]<box.y+100)):
                    if(counter!=1):
                        sound1.play()
                        counter-=1
                        box_letter_rect=box_letter.render(str(counter),True,"white")
                    else:
                        sound2.play()
                        score+=start_score
                        counter=random.randrange(3,11)
                        start_score=counter
                        if(score>int(data[0][0])):
                            cursor.execute("UPDATE scores SET score='{}'".format(score))
                            connection.commit()
                        score_text_rect=score_text.render("Score:{}".format(str(score)),True,"black")
                        color_index=random.randrange(len(rect_color))
                        x=random.randrange(100,400)
                        y=random.randrange(100,550)
                        box=pygame.draw.rect(color=rect_color[color_index],surface=screen,rect=(x,y,100,100),width=0,border_radius=10)
                        box_letter_rect=box_letter.render(str(counter),True,"white")
    else:
        score=0
        screen.fill("white")
        box1=pygame.draw.rect(color=rect_color[color_index],surface=screen,rect=(100,100,100,100),width=0,border_radius=10)
        box_letter1=pygame.font.SysFont("Calibri",60)
        box_letter_rect1=box_letter1.render(str(counter),True,"white")
        box2=pygame.draw.rect(color="green",surface=screen,rect=(330,370,100,100),width=0,border_radius=10)
        box_letter2=pygame.font.SysFont("Calibri",60)
        box_letter_rect2=box_letter2.render("2",True,"white")
        letter=pygame.font.SysFont("Calibri",50)
        letter_cor=letter.render("Let's Play",True,"black")
        rect=pygame.draw.rect(surface=screen,color="red",rect=(230,300,100,50),width=0,border_radius=15)
        inner_text=pygame.font.SysFont("Calibri",20)
        inner_text_cor=inner_text.render("Start",True,"white")
        screen.blit(letter_cor,(190,220))
        screen.blit(inner_text_cor,(250,320))
        screen.blit(box_letter_rect1,(120,120))
        screen.blit(box_letter_rect2,(350,390))
        pygame.display.update()
        for e in pygame.event.get():
            if(e.type==pygame.QUIT):
                running=False
            if(e.type==pygame.MOUSEBUTTONDOWN):
                if((e.pos[0]>rect.x and e.pos[0]<(rect.x+100)) and (e.pos[1]>rect.y and e.pos[1]<rect.y+50)):
                    clock=tm.time()
                    started=False
                    score=0

pygame.quit()