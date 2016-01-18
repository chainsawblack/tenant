##############################################################################
# The tenant v1.0 demo scriptcode
##############################################################################
# Добро пожаловать в код игры "Арендатор".
# Раз вы уже здесь, то надеюсь, что что-то из говнокода ниже окажется для вас полезным.
# 
# Have a nice time, guys!
#
# Chainsaw
# Студия "R18+".
##############################################################################

init:
    
    # Настройки:
    #$ _remove_preference('Display') # Отключение полноэкранки # Не работает
    #$ cursorlist = ["source/images/my_cursor.png", "default", (0, 0)] # Кастомный курсор # Не работает
    
    # Переходы:
    $ whitenoise_changing_scene = ImageDissolve("source/images/white_noize.png", 1.5, 50, reverse=False) # Белый шум
    
    # Эффекты:
    image it_rains = SnowBlossom("source/images/rain_particle.png", count=900, border=6, xspeed=(0), yspeed=(600, 1000), start=0, fast=True, horizontal=False) # Дождь
    
    # Персонажи:
    $ storyteller = Character('Вы', color="#99A1FF")

    # Фоны:
    image splashscreen static = "source/images/splashscreen1.png" # R-18 warning
    image splashscreen glitch = Animation("source/images/splashscreen2.jpg", 0.05, "source/images/splashscreen3.jpg", 0.05, "source/images/splashscreen4.jpg", 0.05, "source/images/splashscreen5.jpg", 0.05, "source/images/splashscreen6.jpg", 0.05, "source/images/splashscreen7.jpg", 0.05, "source/images/splashscreen8.jpg", 0.05, "source/images/splashscreen9.jpg", 0.05, "source/images/splashscreen10.jpg", 0.05) # R-18 warning with glitch
    image animated_whitenoise = Animation("source/images/noise1.png", 0.05, "source/images/noise2.png", 0.05, "source/images/noise3.png", 0.05, "source/images/noise4.png", 0.05, "source/images/noise5.png", 0.05, "source/images/noise6.png", 0.05, "source/images/noise7.png", 0.05)
    image main_menu_animation:
        im.Scale("source/images/house_mainscreen_10.png", 800, 600)
        linear 9 zoom 1.1        
        zoom 1.0        
        im.Scale("source/images/house_mainscreen_1.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_2.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_8.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_4.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_3.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_9.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_5.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_6.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0
        im.Scale("source/images/house_mainscreen_7.png", 800, 600)
        linear 9 zoom 1.1
        zoom 1.0        
        repeat
    image bg uni = "source/images/main_menu_blank.png"
    image main_menu_title:
        "source/images/game_title.png"
    image bus_window = "source/images/bus_window.png"
    image bus_window_field = im.Scale("source/images/bus_window_field.png", 2801, 800)
    transform bus_moving:
        xalign 0.1
        yalign 0.65
        linear 28.0 xalign 0.9 yalign 0.0
        repeat
   
        

    # Звуки:
    $ splashglitch = "source/sound/glitch.wav"
    $ rainsounds = "source/sound/rain3.mp3"
    $ whitenoise = "source/sound/whitenoise.wav"

    # Переменные:
    # Общие:
    $ unread_messages = 0 # Число непрочитанных сообщений в ПДА
    $ money = 0
    $ cigs = 0
    $ game_events = "" # Лог игровых событий для вывода на экране статуса
    $ insane = 170 # Уровень рассудка изначально. От 0 до 200    
    # Языковые:
    $ moral_decrease = u"Ваш уровень рассудка понизился на "
    $ moral_encrease = u"Ваш уровень рассудка повысился на "
    $ cigs_decrease = u"Количество сигарет уменьшилось на "
    $ cigs_encrease = u"Количество сигарет увеличилось на "
    $ money_decrease = u"Вы потратили "
    $ money_encrease = u"Вы получили "
    $ money_title = u"рублей"   
 


# Splashscreen
label splashscreen:
    
    #jump start # Для отладки
    jump in_da_bus #для отладки
    
    scene black
    
    $ renpy.pause (1.5, hard=True)
    
    scene splashscreen static with whitenoise_changing_scene
    
    $ renpy.pause (0.8, hard=True)
    
    scene splashscreen glitch
    
    play sound splashglitch
    
    $ renpy.pause (1.0, hard=True)
    
    scene splashscreen static
    
    stop sound
    
    $ renpy.pause (1.0, hard=True)
    
    scene black with dissolve    
    
    $ renpy.pause (1, hard=True)

return


# Поехали
label start:
    play sound whitenoise fadein 1
    #jump animated_whitenoise_label
    # with vpunch # Для тряски, на будущее

    ##############################################################################
    # Для системы обмена сообщениями в ShadowNet
    $ mail = [] # Сообщения
    $ mail_queue = [] # Задержка доставки сообщений
    $ contacts = []
    ##############################################################################
    
    # $ add_message("Тема", "Sender_name", "Текст") # Для отладки
    # $ add_message("Тема отложенного сообщения", "Sender_name", "Текст отложенного сообщения", delay=True) # Для отладки
    # $ add_message("Тема сообщения с возможностью ответа", "Sender_name", "Текст сообщения с возможностью ответа ", "Sender_name_reply") # Для отладки

    $ money = renpy.random.randint(100, 400) # Кредитов изначально
    
    $ cigs = renpy.random.randint(2, 20) # Сигарет изначально   
       
    scene black
    
    $ renpy.pause (1.5, hard=True)
    
    
    ##############################################################################
    # Вступительная сцена

    scene bg uni with fade

    show animated_whitenoise with fade
    
    show it_rains with dissolve

    #show screen gui_game_menu(0) # Для отладки

    #call new_message_received(3) # Новое сообщение # Для отладки

    "{i}...{/i}"
    
    #hide it_rains with dissolve
    
    #scene black with dissolve
    
    $ renpy.pause (1.0, hard=True)
    jump in_da_bus #для отладки
    
    

return


label in_da_bus:
    scene bg uni with fade
    show bus_window_field at bus_moving
    show bus_window
    "{i}1111111111{/i}"
    
    
    
return




label animated_whitenoise_label:
    play sound whitenoise fadein 1
    show animated_whitenoise with fade
    stop sound fadeout 1
    hide animated_whitenoise with fade    
return































