import pygame
import sys
import traceback
import wall
import food
import myTank
import enemyTank

victory_condition = 10
delay = 100
moving = 0
movdir = 0
moving2 = 0
movdir2 = 0
enemyNumber = 3
enemydie_numer = 0
enemyCouldMove = True
switch_R1_R2_image = True
homeSurvive = True
running_T1 = True
running_T2 = True
life_num=3      #生命个数

resolution = (630, 680)  # 指明图形窗口分辨率

def start_interface():
    ck = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()  # 游戏刷新速度（我个人这么理解）
    start_ck = pygame.Surface(ck.get_size())  # 充当开始界面的画布
    start_ck2 = pygame.Surface(ck.get_size())  # 充当第一关的画布界面暂时占位（可以理解为游戏开始了）
    start_ck = start_ck.convert()  # 纪录了一个Surface对象的
    start_ck2 = start_ck2.convert()
    start_ck.fill((255, 255, 255))
    start_ck2.fill((0, 255, 0))
    # 加载各个素材图片 并且赋予变量名
    i1 = pygame.image.load("resources/images/start/s1.png")
    i1.convert()
    i11 = pygame.image.load("resources/images/start/s2.png")
    i11.convert()

    i2 = pygame.image.load("resources/images/start/n2.png")
    i2.convert()
    i21 = pygame.image.load("resources/images/start/n1.png")
    i21.convert()

    i3 = pygame.image.load('resources/images/start/n2.png')
    i3.convert()
    i31 = pygame.image.load('resources/images/start/n1.png')
    i31.convert()

    bg = pygame.image.load('resources/images/start/bg.png')
    bg.convert()
    bg = pygame.transform.scale(bg, resolution)

    #  以下为选择开始界面鼠标检测结构。
    n1 = True
    x = 200
    y = 480
    x_1 = 200
    y_1 = 570
    while n1:
        clock.tick(30)
        start_ck.blit(bg, (0, 0))
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        if x1 >= x + 27 and x1 <= x + 355 and y1 >= y + 21 and y1 <= y + 87:
            start_ck.blit(i11, (x, y))
            if buttons[0]:
                n1 = False

        elif x1 >= x_1 + 27 and x1 <= x_1 + 355 and y1 >= y_1 + 21 and y1 <= y_1 + 87:
            start_ck.blit(i21, (x_1, y_1))
            if buttons[0]:
                pygame.quit()
                exit()

        else:
            start_ck.blit(i1, (x, y))
            start_ck.blit(i2, (x_1, y_1))

        ck.blit(start_ck, (0, 0))
        pygame.display.update()

        # 监听事件
        for event in pygame.event.get():

            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("游戏退出...")

                # quit 卸载所有的模块
                pygame.quit()

                # exit() 直接终止当前正在执行的程序
                exit()

def end_interface():
    global enemydie_numer
    print("enemydie_numer:",enemydie_numer)
    ck = pygame.display.set_mode(resolution)
    start_ck = pygame.Surface(ck.get_size())  # 充当开始界面的画布
    again_image =  pygame.image.load('resources/images/end/restart.png')
    again_image.convert()
    end_image =  pygame.image.load('resources/images/end/end.png')
    end_image.convert()
    victory_image = pygame.image.load('resources/images/end/victory.png')
    size1 = (victory_image.get_size()[0]//2,victory_image.get_size()[1]//2)
    victory_image = pygame.transform.scale(victory_image,size1)
    lose_image = pygame.image.load('resources/images/end/lose.png')
    lose_image.convert()
    size2 = (lose_image.get_size()[0]//2,lose_image.get_size()[1]//2)
    lose_image = pygame.transform.scale(lose_image,size2)
    print("123123123121231231231323:",enemydie_numer)
    x =50
    if(enemydie_numer>=victory_condition):
        ck.blit(victory_image,(x,100))               #胜利了
    else:               #失败了
        ck.blit(lose_image,(x,100))
    ck.blit(again_image, (200, 450))
    while True:     #使用了
        mouse_down = pygame.mouse.get_pressed()
        if mouse_down[0]:  # 如果按键的左键按下了
            pos = pygame.mouse.get_pos()  # 获取鼠标的坐标
            if 200 < pos[0] < 500 and 450 < pos[1] < 490:  # 如果是在重新开始的范围
                print("2")
                main()

        pygame.display.update()
        for event in pygame.event.get():

            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("游戏退出...")

                # quit 卸载所有的模块
                pygame.quit()

                # exit() 直接终止当前正在执行的程序
                exit()
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
#！！！！！游戏初始化 init_game()
    pygame.init() # 初始化pygame所有模块
    screen = pygame.display.set_mode(resolution) # 创建Surface对象
    pygame.display.set_caption("坦克大战") # 设置窗口标题
    # 加载图片

    background_image = pygame.image.load(r".\image\background.png") # 加载背景图
    home_image = pygame.image.load(r".\image\home1.png").convert_alpha() # 加载保护目标图
    home_destroyed_image = pygame.image.load(r".\image\home_destroyed.png").convert_alpha() # 加载保护目标被摧毁图
    score_image = pygame.image.load(r".\image\score.png").convert_alpha()
    score_image = pygame.transform.scale(score_image,(630,80))
    score = 0
    home_image.set_colorkey((255, 255, 255)) # 设置透明颜色键
    home_destroyed_image.set_colorkey((255, 255, 255)) # 设置透明颜色键
    # 加载音效

    start_sound = pygame.mixer.Sound(r".\music\start.wav") # 加载游戏场景音效
    start_sound.play() # 播放游戏场景音效

    fire_sound = pygame.mixer.Sound(r".\music\Gunfire.wav")  # 加载开火音效
    bang_sound = pygame.mixer.Sound(r".\music\bang.wav") # 加载中弹被毁音效
    # 定义精灵组:坦克，我方坦克，敌方坦克，敌方子弹
    allTankGroup = pygame.sprite.Group()
    mytankGroup = pygame.sprite.Group()
    allEnemyGroup = pygame.sprite.Group()
    redEnemyGroup = pygame.sprite.Group()
    sEnemyGroup = pygame.sprite.Group()
    otherEnemyGroup = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    # 创建地图
    bgMap = wall.Map()
    # 创建道具（但不显示）
    prop = food.Food()
    # 创建我方坦克
    myTank_T1 = myTank.MyTank(1)
    allTankGroup.add(myTank_T1)
    mytankGroup.add(myTank_T1)
    myTank_T2 = myTank.MyTank(2)
    allTankGroup.add(myTank_T2)
    mytankGroup.add(myTank_T2)
    # 创建敌方坦克
    for i in range(1, 4):
        enemy = enemyTank.EnemyTank()
        allTankGroup.add(enemy)
        allEnemyGroup.add(enemy)
        if enemy.isred == True:
            redEnemyGroup.add(enemy)
            continue
        if enemy.kind == 3:
            sEnemyGroup.add(enemy)
            continue
        otherEnemyGroup.add(enemy)
    # 加载敌军坦克出现动画
    appearance_image = pygame.image.load(r".\image\appear.png").convert_alpha()
    appearance = []
    appearance.append(appearance_image.subsurface((0, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((96, 0), (48, 48)))
    # 创建敌方坦克延迟200
    DELAYEVENT = pygame.constants.USEREVENT
    pygame.time.set_timer(DELAYEVENT, 200)
    # 创建敌方子弹延迟1000
    ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)

    # 创建 我方 子弹延迟200
    MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
    pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)

    # 敌方坦克 静止8000
    NOTMOVEEVENT = pygame.constants.USEREVENT + 3
    pygame.time.set_timer(NOTMOVEEVENT, 8000)
    global enemydie_numer
    life_num = 3
    enemydie_numer=0
    delay = 100
    moving = 0
    movdir = 0
    moving2 = 0
    movdir2 = 0
    enemyNumber = 3
    enemyCouldMove = True
    switch_R1_R2_image = True
    homeSurvive = True
    running_T1 = True
    running_T2 = True
    clock = pygame.time.Clock()
    #游戏循环
    start_interface()
    
    while True and enemydie_numer<victory_condition and life_num>=1 :
    #!!!!!!!显示信息 show_information()
        score = enemydie_numer * 100
        font1 = pygame.font.SysFont('SimHei', 30)  # 黑体24
        screen.blit(score_image, (0, 620))
        print_text(screen, font1, 95, 640, str(score))
        print_text(screen, font1, 370, 640,
                   str(victory_condition - enemydie_numer))
        print_text(screen, font1, 590, 640, str(life_num))


    #!!!!!!!检查状态 check_event()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # 我方子弹冷却事件
            if event.type == MYBULLETNOTCOOLINGEVENT:
                myTank_T1.bulletNotCooling = True

            # 敌方子弹冷却事件
            if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                for each in allEnemyGroup:
                    each.bulletNotCooling = True

            # 敌方坦克静止事件
            if event.type == NOTMOVEEVENT:
                enemyCouldMove = True

            # 创建敌方坦克延迟
            if event.type == DELAYEVENT:
                if enemyNumber < 4:
                    enemy = enemyTank.EnemyTank()
                    if pygame.sprite.spritecollide(enemy, allTankGroup, False, None):
                        break
                    allEnemyGroup.add(enemy)
                    allTankGroup.add(enemy)
                    enemyNumber += 1
                    enemydie_numer += 1
                    print("enemydie_numer:",enemydie_numer)
                    if enemy.isred == True:
                        redEnemyGroup.add(enemy)
                    elif enemy.kind == 3:
                        sEnemyGroup.add(enemy)
                    else:
                        otherEnemyGroup.add(enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_e:
                    myTank_T1.levelUp()
                if event.key == pygame.K_q:
                    myTank_T1.levelDown()
                if event.key == pygame.K_3:
                    myTank_T1.levelUp()
                    myTank_T1.levelUp()
                    myTank_T1.level = 3
                if event.key == pygame.K_2:
                    if myTank_T1.speed == 3:
                        myTank_T1.speed = 4
                    else:
                        myTank_T1.speed = 3
                if event.key == pygame.K_1:
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        bgMap.brick = wall.Brick()
                        bgMap.brick.rect.left, bgMap.brick.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.brickGroup.add(bgMap.brick)
                if event.key == pygame.K_4:
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        bgMap.iron = wall.Iron()
                        bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.ironGroup.add(bgMap.iron)

                        # 检查用户的键盘操作

    #！！！！！检查按键操作 check_keydown()
        key_pressed = pygame.key.get_pressed()
        # 玩家一的移动操作
        if moving:
            moving -= 1
            if movdir == 0:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 1:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 2:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 3:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True

        if not moving:
            if key_pressed[pygame.K_w]:
                moving = 7
                movdir = 0
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_s]:
                moving = 7
                movdir = 1
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_a]:
                moving = 7
                movdir = 2
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_d]:
                moving = 7
                movdir = 3
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                    moving = 0
                allTankGroup.add(myTank_T1)
        if key_pressed[pygame.K_j]:
            if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                fire_sound.play()
                myTank_T1.shoot()
                myTank_T1.bulletNotCooling = False

        # 玩家二的移动操作
        if moving2:
            moving2 -= 1
            if movdir2 == 0:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 1:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 2:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True
            if movdir2 == 3:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                running_T2 = True

        if not moving2:
            if key_pressed[pygame.K_UP]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 0
                running_T2 = True
            elif key_pressed[pygame.K_DOWN]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 1
                running_T2 = True
            elif key_pressed[pygame.K_LEFT]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 2
                running_T2 = True
            elif key_pressed[pygame.K_RIGHT]:
                allTankGroup.remove(myTank_T2)
                myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                allTankGroup.add(myTank_T2)
                moving2 = 7
                movdir2 = 3
                running_T2 = True
        if key_pressed[pygame.K_KP0]:
            if not myTank_T2.bullet.life:
                # fire_sound.play()
                myTank_T2.shoot()

        # 画背景
        screen.blit(background_image, (0, 0))
        # 画砖块
        for each in bgMap.brickGroup:
            screen.blit(each.image, each.rect)
            # 花石头
        for each in bgMap.ironGroup:
            screen.blit(each.image, each.rect)
            # 画home
        if homeSurvive:
            screen.blit(home_image, (3 + 12 * 24, 3 + 24 * 24))
        else:
            screen.blit(home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))
        # 画我方坦克1
        if not (delay % 5):
            switch_R1_R2_image = not switch_R1_R2_image
        if switch_R1_R2_image and running_T1:
            screen.blit(myTank_T1.tank_R0, (myTank_T1.rect.left, myTank_T1.rect.top))
            running_T1 = False
        else:
            screen.blit(myTank_T1.tank_R1, (myTank_T1.rect.left, myTank_T1.rect.top))
        # 画我方坦克2
        if switch_R1_R2_image and running_T2:
            screen.blit(myTank_T2.tank_R0, (myTank_T2.rect.left, myTank_T2.rect.top))
            running_T2 = False
        else:
            screen.blit(myTank_T2.tank_R1, (myTank_T2.rect.left, myTank_T2.rect.top))
            # 画敌方坦克
        for each in allEnemyGroup:
            # 判断5毛钱特效是否播放
            if each.flash:
                # 　判断画左动作还是右动作
                if switch_R1_R2_image:
                    screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(each)
                else:
                    screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(each)
            else:
                # 播放5毛钱特效
                if each.times > 0:
                    each.times -= 1
                    if each.times <= 10:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 20:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 30:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 40:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 50:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 60:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 70:
                        screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 80:
                        screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 90:
                        screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                if each.times == 0:
                    each.flash = True
    #！！！！！检查子弹碰撞 check_collide()
        # 绘制我方子弹1
        if myTank_T1.bullet.life:
            myTank_T1.bullet.move()
            screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)
            # 子弹 碰撞 子弹
            for each in enemyBulletGroup:
                if each.life:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        myTank_T1.bullet.life = False
                        each.life = False
                        pygame.sprite.spritecollide(myTank_T1.bullet, enemyBulletGroup, True, None)
            # 子弹 碰撞 敌方坦克
            if pygame.sprite.spritecollide(myTank_T1.bullet, redEnemyGroup, True, None):
                prop.change()
                bang_sound.play()
                enemyNumber -= 1
                myTank_T1.bullet.life = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet, sEnemyGroup, False, None):
                for each in sEnemyGroup:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(myTank_T1.bullet, sEnemyGroup, True, None)
                            bang_sound.play()
                            enemyNumber -= 1
                        elif each.life == 2:
                            each.life -= 1
                            each.tank = each.enemy_3_0
                        elif each.life == 3:
                            each.life -= 1
                            each.tank = each.enemy_3_2
                myTank_T1.bullet.life = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet, otherEnemyGroup, True, None):
                bang_sound.play()
                enemyNumber -= 1
                myTank_T1.bullet.life = False
            if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                myTank_T1.bullet.life = False
                myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 brickGroup
            if myTank_T1.bullet.strong:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, True, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

        # 绘制我方子弹2
        if myTank_T2.bullet.life:
            myTank_T2.bullet.move()
            screen.blit(myTank_T2.bullet.bullet, myTank_T2.bullet.rect)
            # 子弹 碰撞 敌方坦克
            if pygame.sprite.spritecollide(myTank_T2.bullet, allEnemyGroup, True, None):
                bang_sound.play()
                enemyNumber -= 1
                myTank_T2.bullet.life = False
            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.brickGroup, True, None):
                myTank_T2.bullet.life = False
                myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 brickGroup
            if myTank_T2.bullet.strong:
                if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, True, None):
                    myTank_T2.bullet.life = False
                    myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, False, None):
                    myTank_T2.bullet.life = False
                    myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

        # 绘制敌人子弹
        for each in allEnemyGroup:
            # 如果子弹没有生命，则赋予子弹生命
            if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                enemyBulletGroup.remove(each.bullet)
                each.shoot()
                enemyBulletGroup.add(each.bullet)
                each.bulletNotCooling = False
            # 如果5毛钱特效播放完毕 并且 子弹存活 则绘制敌方子弹
            if each.flash:
                if each.bullet.life:
                    # 如果敌人可以移动
                    if enemyCouldMove:
                        each.bullet.move()
                    screen.blit(each.bullet.bullet, each.bullet.rect)
                    # 子弹 碰撞 我方坦克

                    if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                        bang_sound.play()
                        myTank_T1.rect.left, myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
                        each.bullet.life = False
                        moving = 0  # 重置移动控制参数
                        for i in range(myTank_T1.level + 1):
                            myTank_T1.levelDown()
                        life_num -=1

                    if pygame.sprite.collide_rect(each.bullet, myTank_T2):
                        bang_sound.play()
                        myTank_T2.rect.left, myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24
                        each.bullet.life = False
                        life_num -= 1
                    # 子弹 碰撞 brickGroup
                    if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                        each.bullet.life = False
                    # 子弹 碰撞 ironGroup
                    if each.bullet.strong:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, True, None):
                            each.bullet.life = False
                    else:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                            each.bullet.life = False
    #！！！！！检查食物/道具 check_food()
        if prop.life:
            screen.blit(prop.image, prop.rect)
            # 我方坦克碰撞 食物/道具
            if pygame.sprite.collide_rect(myTank_T1, prop):
                if prop.kind == 1:  # 敌人全毁
                    for each in allEnemyGroup:
                        if pygame.sprite.spritecollide(each, allEnemyGroup, True, None):
                            bang_sound.play()
                            enemyNumber -= 1
                    prop.life = False
                if prop.kind == 2:  # 敌人静止
                    enemyCouldMove = False
                    prop.life = False
                if prop.kind == 3:  # 子弹增强
                    myTank_T1.bullet.strong = True
                    prop.life = False
                if prop.kind == 4:  # 家得到保护
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        bgMap.iron = wall.Iron()
                        bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.ironGroup.add(bgMap.iron)
                    prop.life = False
                if prop.kind == 5:  # 坦克无敌
                    prop.life = False
                    pass
                if prop.kind == 6:  # 坦克升级
                    myTank_T1.levelUp()
                    prop.life = False
                if prop.kind == 7:  # 坦克生命+1
                    myTank_T1.life += 1
                    prop.life = False
        # pygame.font.get_fonts('')
        # 延迟
        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

    end_interface()     #结束界面




if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()