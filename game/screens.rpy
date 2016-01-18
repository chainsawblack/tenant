##############################################################################
# The tenant v1.0 demo scriptcode
##############################################################################
# Набор экранов

##############################################################################
# Say
#
# Экран отображения ADV-диалога.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Умолчания для side_image и two_window
    default side_image = None
    default two_window = False

    # Решаем, нужен ли нам двухоконный или однооконный вариант.
    if not two_window:

        # Вариант с одним окном.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what" at text_transform # Появление текста с анимацией fade in

    else:

        # Вариант с двумя окнами.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"
                

    # Если есть изображение, отобразить его над текстом.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Использовать быстрое меню.
    use quick_menu

transform text_transform: # Появление текста с анимацией fade in, сама трансформация
    alpha 0.0
    linear 0.3 alpha 1.0
  
  
##############################################################################
# Choice - modificated for messages_system
#
# Экран для отображения внутриигровых меню.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:
    
    if reply_screen or draft_screen:
        # Меню выбора для ответа на письма
        frame:
            style_group "mailbox"

            vbox:
                if reply_screen:
                    label "Написать ответ"
                else:
                    label "Написать сообщение"
                if reply_screen:
                    text ("Кому: " + current_message.sender)                
                    text ("Тема: Re: " + current_message.subject)
                else:
                    text ("Кому: " + contact.name)
                    text ("Тема: " + message_title)
                null  height 30

                for caption, action, chosen in items:

                    if action:
                        button:
                            action action
                            style "menu_choice_button" xalign 0.5

                            text caption text_align 0.5

                    else:
                        text caption style "menu_caption"
                        
    else:
        # Дефолтное меню выбора
        window:
            style "menu_window"
            xalign 0.5
            yalign 0.5

            vbox:
                style "menu"
                spacing 2

                for caption, action, chosen in items:

                    if action:

                        button:
                            action action
                            style "menu_choice_button"

                            text caption style "menu_choice"

                    else:
                        text caption style "menu_caption"

init -2 python:
    config.narrator_menu = True

    style.menu_window.set_parent(style.default)
    style.menu_choice.set_parent(style.button_text)
    style.menu_choice.clear()
    style.menu_choice_button.set_parent(style.button)
    style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
    style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Экран для отображения renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Экран для NVL-диалога и меню.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Отображать диалог.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Отображать меню, если есть.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Main Menu
#
# Экран для отображения главного меню при запуске Ren'Py.
# http://www.renpy.org/doc/html/screen_special.html#main-menu
label main_menu:
    call screen main_menu
label restart:
    call screen yesno_prompt(message=u"Вы уверены, что хотите начать игру заново?", yes_action=Start(), no_action=Return()) 
return
label my_exit:
    call screen yesno_prompt(message=u"Вы сдались и бежите?", yes_action=Quit(confirm=False), no_action=Jump("main_menu"))
return
screen my_global_exit:
    tag menu
    #call screen yesno_prompt(message=u"Вы сдались и бежите?", yes_action=Quit(confirm=False), no_action=Jump('close_custom_global_exit'))
return
screen main_menu:

    # Это заменяет другие меню.
    tag menu

    

    # Фон главного меню.
    window:
        style "mm_root"
        # add SnowBlossom("data/face.png", count=15, xspeed=(-400, 400), yspeed=(-400, 400), start=10, fast=True)
        #add(Animation("source/images/house_mainscreen_10.png", 4.0)) # Анимация фона меню - здание игры        
        #add custom_cursor(cursorlist) # Кастомный курсор - не работает
        #image house_mainscreen_10 = "source/images/house_mainscreen_10.png"
        #show house_mainscreen_10 with zoomin
        add "animated_whitenoise"
        add "main_menu_animation"
        add "main_menu_title"
        #add "animated_whitenoise"
        #hide "animated_whitenoise"
        $ renpy.sound.set_volume(0.5) #....установить громкость звука на 50% 
        $ renpy.music.set_volume(0.5) #.....установить громкость музыки на 50%

    $ y=155
    imagebutton auto "source/images/gui/main_continue_%s.png" xpos 33 ypos y focus_mask True action Play ("test_one", "source/sound/clicksound1.mp3"), Jump("animated_whitenoise_label"), FileLoad(1, confirm=False, page="auto", newest=True) hovered [ Play ("test_one", "source/sound/hover_sound.wav") ]
    $ y+=64
    imagebutton auto "source/images/gui/main_start_%s.png" xpos 33 ypos y focus_mask True action Play ("test_two", "source/sound/clicksound1.mp3"), Start() hovered [ Play ("test_two", "source/sound/hover_sound.wav") ]
    $ y+=57
    imagebutton auto "source/images/gui/main_load_%s.png" xpos 33 ypos y focus_mask True action Play ("test_three", "source/sound/clicksound1.mp3"), Jump("animated_whitenoise_label"), ShowMenu("load") hovered [ Play ("test_three", "source/sound/hover_sound.wav") ]
    $ y+=59
    imagebutton auto "source/images/gui/main_settings_%s.png" xpos 33 ypos y focus_mask True action Play ("test_four", "source/sound/clicksound1.mp3"), Jump("animated_whitenoise_label"), ShowMenu("preferences") hovered [ Play ("test_four", "source/sound/hover_sound.wav") ] 
    $ y+=58
    imagebutton auto "source/images/gui/main_about_%s.png" xpos 33 ypos y focus_mask True action Play ("test_five", "source/sound/clicksound1.mp3"), Jump("animated_whitenoise_label"), ShowMenu("about") hovered [ Play ("test_five", "source/sound/hover_sound.wav") ]
    $ y+=54
    imagebutton auto "source/images/gui/main_exit_%s.png" xpos 33 ypos y focus_mask True action Play ("test_six", "source/sound/clicksound1.mp3"), Jump("animated_whitenoise_label"), Jump("my_exit") hovered [ Play ("test_six", "source/sound/hover_sound.wav") ]
    $ y+=59
        
        
    # Кнопки главного меню.
    #frame:
        #style_group "mm"
        #xalign .98
        #yalign .98

        #has vbox

        #textbutton _("Начать новую игру") action Jump("restart")
        #textbutton _("Продолжить игру") action FileLoad(1, confirm=False, page="auto", newest=True)
        #textbutton _("Загрузить игру") action ShowMenu("load")
        #textbutton _("Настройки") action ShowMenu("preferences")
        #textbutton _("Об игре") action ShowMenu("about")
        #textbutton _("Выход") action Jump("my_exit")

init -2 python:

    # Сделать все кнопки главного меню одноразмерными.
    style.mm_button.size_group = "mm"
    renpy.music.register_channel("test_one", "sfx", False)
    renpy.music.register_channel("test_two", "sfx", False)
    renpy.music.register_channel("test_three", "sfx", False)
    renpy.music.register_channel("test_four", "sfx", False)
    renpy.music.register_channel("test_five", "sfx", False)
    renpy.music.register_channel("test_six", "sfx", False)
    renpy.music.set_volume(0.5, delay=0, channel='test_one')
    renpy.music.set_volume(0.5, delay=0, channel='test_two')
    renpy.music.set_volume(0.5, delay=0, channel='test_three')
    renpy.music.set_volume(0.5, delay=0, channel='test_four')
    renpy.music.set_volume(0.5, delay=0, channel='test_five')
    renpy.music.set_volume(0.5, delay=0, channel='test_six')


##############################################################################
# Navigation
#
# Экран, включаемый в другие экраны для отображения навигации и фона.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # Фон игрового меню.
    window:
        style "gm_root"

    # Кнопки.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Продолжить игру") action Return()
        textbutton _("Настройки") action ShowMenu("preferences")
        textbutton _("Сохранить игру") action ShowMenu("save")
        textbutton _("Загрузить игру") action ShowMenu("load")
        textbutton _("Главное меню") action MainMenu()
        textbutton _("Об игре") action ShowMenu("about")
        textbutton _("Выход") action Jump("my_exit")

init -2 python:
    style.gm_nav_button.size_group = "gm_nav"
    
    
##############################################################################
# Кастомное меню паузы внутри игры - не используется
#    
screen game_menu:
    tag menu
    
    # Фон игрового меню.
    window:
        style "gm_root"

    # Кнопки.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Продолжить игру") action Return()
        textbutton _("Настройки") action ShowMenu("preferences")
        textbutton _("Сохранить игру") action ShowMenu("save")
        textbutton _("Загрузить игру") action ShowMenu("load")
        textbutton _("Главное меню") action MainMenu()
        textbutton _("Об игре") action ShowMenu("about")
        textbutton _("Выход") action Jump("my_exit")

##############################################################################
# Save, Load
#
# Экраны для сохранения и загрузки игры.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Ибо сохранение и загрузка очень похожи, мы совмещаем их в один экран,
# file_picker. Потом мы используем его из экранов
# загрузки и сохранения.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # Кнопки сверху для выбора страницы.
        hbox:
            style_group "file_picker_nav"

            textbutton _("<<"):
                action FilePagePrevious()

            textbutton _("Авто"):
                action FilePage("auto")

            textbutton _("Быстро"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _(">>"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Отобразить сетку файловых слотов.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Отобразить 10 слотов, с номерами от 1 до 10.
            for i in range(1, columns * rows + 1):

                # Каждый из них - кнопка.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Добавить скриншот.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # Это заменяет другие меню.
    tag menu

    use navigation
    use file_picker

screen load:

    # Это заменяет другие меню.
    tag menu

    use navigation
    use file_picker

init -2 python:
    style.file_picker_frame = Style(style.menu_frame)

    style.file_picker_nav_button = Style(style.small_button)
    style.file_picker_nav_button_text = Style(style.small_button_text)

    style.file_picker_button = Style(style.large_button)
    style.file_picker_text = Style(style.large_button_text)



##############################################################################
# Preferences
#
# Экран, позволяющий пользователю изменять настройки.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # Включить навигацию.
    use navigation

    # Разместить навигационные колонки в сетку шириной 3.
    grid 3 1:
        style_group "prefs"
        xfill True

        # Левая колонка.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Отображение")
                textbutton _("Окно") action Preference("display", "window")
                textbutton _("Полный экран") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Переходы")
                textbutton _("Все") action Preference("transitions", "all")
                textbutton _("Никаких") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Скорость текста")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Джойстик...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Пропуск")
                textbutton _("Прочтенных сообщений") action Preference("skip", "seen")
                textbutton _("Всех сообщений") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Начать пропуск") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("После выборов")
                textbutton _("Остановить пропуск") action Preference("after choices", "stop")
                textbutton _("Продолжить пропуск") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Ускорить время")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Ждать голос") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Громкость музыки")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Громкость звука")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Тест"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Громкость голоса")
                    bar value Preference("voice volume")

                    textbutton _("Оставлять голос") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Тест"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2 python:
    style.pref_frame.xfill = True
    style.pref_frame.xmargin = 5
    style.pref_frame.top_margin = 5

    style.pref_vbox.xfill = True

    style.pref_button.size_group = "pref"
    style.pref_button.xalign = 1.0

    style.pref_slider.xmaximum = 192
    style.pref_slider.xalign = 1.0

    style.soundtest_button.xalign = 1.0


##############################################################################
# Yes/No Prompt
#
# Экран, спрашивающий у пользователя вопрос да/нет.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Да") action yes_action
            textbutton _("Нет") action no_action

    # Правый щелчок и escape отвечают "нет".
    key "game_menu" action no_action

init -2 python:
    style.yesno_button.size_group = "yesno"
    style.yesno_label_text.text_align = 0.5
    style.yesno_label_text.layout = "subtitle"


##############################################################################
# Quick Menu
#
# Экран, входящий в экран save и дающий некоторые полезные функции
screen quick_menu:

    # Быстрое внутриигровое меню.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Назад") action Rollback()
        # textbutton _("Сохранить") action ShowMenu('save')
        textbutton _("Быстрое сохранение") action QuickSave()
        textbutton _("Быстрая загрузка") action QuickLoad()
        # textbutton _("Пропуск") action Skip()
        # textbutton _("Б.Пропуск") action Skip(fast=True, confirm=True)
        # textbutton _("Статус") action ShowMenu("about")
        # textbutton _("Настр") action ShowMenu('preferences')
    #if start_telling:    
        #hbox:
            #style_group "status"
            #textbutton _("Статус") action ShowMenu("status") style style.button["status"]
            #imagebutton auto "source/images/pda_%s.png" action ShowMenu('status') # Кнопка ПДА (статус)
            #xalign 1.0
            #yalign 0.0

init -2 python:
    style.quick_button.set_parent('default')
    style.quick_button.background = None
    style.quick_button.xpadding = 5

    style.quick_button_text.set_parent('default')
    style.quick_button_text.size = 12
    style.quick_button_text.idle_color = "#8888"
    style.quick_button_text.hover_color = "#ccc"
    style.quick_button_text.selected_idle_color = "#cc08"
    style.quick_button_text.selected_hover_color = "#cc0"
    style.quick_button_text.insensitive_color = "#4448"  
    
    #style.status_button_text.size = 11
    #style.button['status'].set_parent('default')
    #style.button['status'].background = "#68cccc"
    #style.button['status'].size = 13
    #style.button['status'].idle_color = "#b2cccc"
    #style.button['status'].hover_color = "#fff"
    #style.button['status'].xpadding = 3
    #style.button['status'].ypadding = 3
    #style.button['status'].selected_idle_color = "#fff"
    #style.button['status'].selected_hover_color = "#fff"
    #style.button['status'].insensitive_color = "#fff"

##############################################################################
# Окно дополнительного игрового интерфейса
#
screen gui_game_menu:
    modal False
    tag menu 
    hbox:
        xalign 0.98
        yalign 0.01
        style_group "quick"
        if new_message_count() == 0:
            imagebutton auto "source/images/pda_%s.png" action ShowMenu('status') # Кнопка ПДА (статус) без новых сообщений
        else:
            imagebutton idle "source/images/pda_mail.png"  hover "source/images/pda_mail_hover.png" action ShowMenu('status') # Кнопка ПДА (статус) с новым сообщением
       
        
##############################################################################
# Окно статуса (открытый ПДА)
#
#test styles
#init python:
    #style.lcd_text.color = "#f00"
    #style.lcd_text.size = 20
screen status:
    modal True
    tag menu 
    add "source/images/mainmenu_ingame_bg.png" 
    key "mouseup_3" action Return()
    frame:  
        area (0,0,800,300)  
        viewport mousewheel True scrollbars "vertical": 
            has vbox 
            # style "lcd"
            text "Статус персонажа:"  
            null height 5  
            text "Известное имя: [storyteller_known_as]"
            text "Возраст: [storyteller_age]"
            text "Род занятий: [storyteller_job]"
            
            if moral == 100:
                $ moral_title="без выраженных особенностей."
            elif moral >= 190:
                $ moral_title="чрезвычайно высокий. Просто ангел и душка, чьи помыслы чисты настолько, что некоторых от него воротит."
            elif moral >= 180:
                $ moral_title="если твоя душа темна, а замыслы полны коварства - лучше не попадайся ему на пути. Для всех же прочих он - лучший друг, всегда безусловно готовый прийти на помощь."
            elif moral >= 170:
                $ moral_title="истинный рыцарь, надежда и защита всех обездоленных и обманутых."
            elif moral >= 160:
                $ moral_title="добряк. Способен на бескорыстные поступки и в целом настроен помогать окружающим."
            elif moral >= 150:
                $ moral_title="славный малый, каких не часто встретишь в наши дни."
            elif moral >= 140:
                $ moral_title="от него можно не ожидать подлости. "
            elif moral >= 130:
                $ moral_title="не рейнджер, конечно, но несправедливость ему претит."
            elif moral >= 120:
                $ moral_title="в целом, доброжелательный парень, при случае к нему можно обратиться за помощью."
            elif moral >= 110:
                $ moral_title="мирный человек, сам без дела шума не подымет. Не склонен к насилию."
            elif moral >= 100:
                $ moral_title="неплохой парень."
            elif moral >= 90:
                $ moral_title="неплохой парень, хотя местами и проныра."
            elif moral >= 80:
                $ moral_title="тот еще хитрец, себе на уме."
            elif moral >= 70:
                $ moral_title="мрачноватый тип, и шуточки соответствующие."
            elif moral >= 60:
                $ moral_title="не тот, с кем стоит встречаться в тёмном переулке."
            elif moral >= 50:
                $ moral_title="если вам нужен напарник в сомнительном предприятии, стоит серьезно обдумать его кандидатуру. Едва ли он откажется."
            elif moral >= 40:
                $ moral_title="не обременён моралью настолько, что это иногда пугает. Всех пугает."
            elif moral >= 30:
                $ moral_title="жестокий мизантроп, каких поискать. О нём ходят весьма мрачные слухи."
            elif moral >= 20:
                $ moral_title="опасный психопат, от которого всем лучше держаться подальше."
            elif moral >= 10:
                $ moral_title="настоящий маньяк. Если встретите его на улице - бегите и не оглядывайтесь. Серьёзно."
            else:
                $ moral_title="предельно низок. Отвратительное, гнусное и беспринцыпное чудовище. Одни поговаривают, что он убил собственных родителей. Другие - что убил {i}и съел{/i}."
            #text "Уровень морали: {b}[moral]{/b} единиц"
            text "Уровень морали: [moral_title]"
                
            null height 5
            text "Известные факты биографии: [storyteller_bio]"
            
    frame:  
        area (0,310,395,230)  
        viewport mousewheel True scrollbars "vertical": 
            has vbox 
            text "Последние события:"  
            null height 5 
            if not game_events:
                text "нет записей"
            else:
                text "[game_events]" 
    frame:  
        area (405,310,395,230)  
        viewport mousewheel True scrollbars "vertical": 
            has vbox 
            text "Содержимое карманов:"  
            null height 5 
            text "Количество кредитов: {size=+4}{font=source/fonts/SFDigitalReadoutMediumOblique.ttf}[money]{/font}{/size} ¥"
            text "Сигарет осталось: {b}[cigs]{/b} штук"
            # text "{b}[money]{/b}" font "source/fonts/SFDigitalReadoutMediumOblique.ttf"
    #Здесь создается ссылка на главное меню 
    frame: 
        #style_group "mm" 
        xalign .98 
        yalign .98 
        has vbox 
        textbutton "OK" action Return()
    frame: 
        #style_group "mm" 
        style_group "messages_box"
        xalign .00 
        yalign .98 
        has hbox 
        if new_message_count() > 0:
            if new_message_count() == 1:
                $ message_notice = u"У вас одно новое сообщение"
            elif new_message_count() > 1 and new_message_count() < 4:
                $ message_notice = u"У вас " + str(new_message_count()) + " новых сообщения"
            else:
                $ message_notice = u"У вас " + str(new_message_count()) + " новых сообщений"
            text "[message_notice]"
        else:
            text "Новых сообщений нет."
        textbutton "Открыть почту" action ShowMenu("mailbox") #action ui.callsinnewcontext("mailbox_screen_label", open_tab="inbox") #передаем параметр
    hbox:
        xalign 0.98 
        yalign 0.01
        style_group "quick"
        if new_message_count() == 0:
            imagebutton idle "source/images/pda_hover.png" hover "source/images/pda_off.png" action Return() # Кнопка ПДА (статус) - есть новые сообщения
        else:
            imagebutton idle "source/images/pda_mail_hover.png" hover "source/images/pda_off.png" action Return() # Кнопка ПДА (статус) - нет новых сообщений
        
init -2 python:
    style.messages_box_frame.xpadding = 11
    style.messages_box_frame.ypadding = 11
    style.messages_box_frame.xmaximum = int(395)
    style.messages_box_frame.xminimum = int(395)
    style.messages_box_text.size = 12
    style.messages_box_button_text.size = 12
    style.messages_box_button.xalign = 0.38

##############################################################################
# Почтовый клиет на ПДА, v2, для обмена текстовыми сообщениями в ShadowNet
#
screen mailbox:
    tag menu
    modal True
    add "source/images/house_mainscreen_ingame.png" 
    key "mouseup_3" action Return(None)
    default current_message = None
    $ available_drafts = [i for i in contacts if i.draft_label]    
    frame:
        style_group "mailbox"
        vbox:
            label "Входящие"
            if new_message_count() > 0:
                text ("Сообщений: %d (непрочитанных: %d)") % (message_count(), new_message_count())
            else:
                text ("Сообщений: %d") % message_count()
            null height 5 
            side "c r":
                area (0,0,800,93)
                viewport id "message_list":
                    draggable True mousewheel True
                    vbox:
                        for i in mail:
                            if i.view:
                                if not i.read:
                                    textbutton ("*новое* " + i.sender + ": " + i.subject) action [SetScreenVariable("current_message",i), i.mark_read] xfill True
                                else:
                                    textbutton (i.sender + ": " + i.subject) action SetScreenVariable("current_message",i) xfill True
                vbar value YScrollValue("message_list")
            hbox:
                null height 20
            side "c r":
                area (0,0,800,380)
                viewport id "view_message":
                    draggable True mousewheel True
                    vbox:
                        if current_message:
                            text ("От кого: " + current_message.sender)
                            null height 5 
                            text ("Тема: " + current_message.subject)
                            null height 10 
                            text current_message.body
                vbar value YScrollValue("view_message")
            use mailbox_commands

screen mailbox_commands:
    hbox:
        if current_message and current_message.reply_label:
            textbutton "Ответить" action current_message.reply
        elif current_message and not current_message.reply_label:
            textbutton "Ответить" action None
        if current_message:
            textbutton "Удалить" action [current_message.delete, SetScreenVariable("current_message", None)]
    hbox:
        if available_drafts:
            textbutton "Написать сообщение" action Show("contacts")
        else:
            textbutton "Написать сообщение" action None
       
        if new_message_count() > 0:
            textbutton "Отметить всё как прочитанное" action mark_all_read
        else:
            textbutton "Отметить всё как прочитанное" action None
        textbutton "Восстановить всё" action restore_all
        textbutton "Назад" action Return(False)
    
        
        
screen contacts:
    modal True
    frame:
        style_group "mailbox"
        xsize 200
        vbox:
            label "Contacts"
            for name in contacts:
                if name.draft_label:
                    textbutton name.name action [name.draft, Hide("contacts")]
                else:
                    textbutton name.name action None
            textbutton "Close" action Hide("contacts")

init -2 python:
    style.mailbox = Style(style.default)
    style.mailbox_vbox.xalign = 0.5
    style.mailbox_vbox.xfill = True
    style.mailbox_hbox.xalign = 0.5
    style.mailbox_label_text.size = 30
    style.mailbox_label_text.xalign = 0.5
    style.mailbox_label.xfill = True
    style.mailbox_frame.xalign = 0.5
    style.mailbox_frame.yalign = 0.5
    style.mailbox_button.set_parent(style.button)  
    style.mailbox_button_text.size = 15
    style.mailbox_text.size = 16
    
##############################################################################
# Почтовый клиет, v1
#
#label mailbox_screen_label(open_tab):
#    $ screen_name = "mailbox_screen_" + open_tab
#    #call screen screen_name
#    renpy.showscreen("mailbox_screen_inbox")
#    return
#screen mailbox_screen_inbox:
#    textbutton "Входящие сообщения" xalign .0 yalign .01 style style.button["activetab"]
#    textbutton "Исходящие сообщения" xalign .55 yalign .01 action Return() style style.button["non_activetab"]
#    textbutton "Новое сообщение" xalign 1.0 yalign .01 action Return() style style.button["non_activetab"]
#    frame:  
#        area (0,40,800,510)  
#        viewport mousewheel True scrollbars "vertical": 
#            has vbox 
#            #text "Входящие сообщения:"  
#            null height 5 
#            text "test"
#    textbutton "Назад" xalign .98 yalign .98 action Return()

#style activetab is text:
    #size 10

#init -2 python:
#    style.button["activetab"].background = "#ffffdd"
#    style.button["non_activetab"].size = 11
    #style.activetab = Style(style.default)
    #style.activetab.size = 11
    #style.activetab.color = "#f00"
    
    
    
    
##############################################################################
# Об игре
#
screen about:
    tag menu 
    add "source/images/house_mainscreen_ingame.png" 
    frame:  
        area (0,0,800,540)  
        viewport mousewheel True scrollbars "vertical": 
            has vbox 
            text "Краткая информация о данной игре:"  
            null height 5 
            text "Очень короткая повествовательная история в декорациях мира киберпанка, с сюжетом, ветвящимся в зависимости от избранной вами линии поведения. Просто один случай, произошедший в не столь уж далеком и не столь уж светлом будущем под лозунгом \"High tech, low life\". \n\nЕсли вы будете вести себя неосмотрительно - последствия не заставят себя ждать. Некоторую роль в игре играет и всемогущий рандом. У персонажа есть условный уровень морали, изменяющийся в зависимости от ваших действий. Мораль открывает и закрывает те или иные возможности действия и фразы в диалогах. \nПросмотреть состояние персонажа вы можете, нажав на \"ПДА\" в правом-верхнем углу в процессе игры.\n\nЭто - демка для дальнейшей рботы, первая моя попытка изобразить что-то вроде визуальной новеллы, скорее даже просто проба движка. Пафос и нуар в сценарии присутствуют, но прошу извинить за полное отсутствие оригинальной визуальной части - я один, и я не художник.\n\nВ игре есть обсценная лексика и сцены насилия, что может показаться кому-то неприятным. Рейтинг - R-18 \n\nДля связи: {a=mailto:fuckoff@chainsaw.su}fuckoff@chainsaw.su{/a} \n\nHave a nice time." 
    frame: 
        style_group "mm" 
        xalign .98 
        yalign .98 
        has vbox 
        textbutton "Главное меню" action ShowMenu("main_menu") 


##############################################################################
# Анимированный текст - трансформация уплывания - на будущее
# show screen fading_text("text", 3.0, 400, 300, 600, 600, color="#fff", size=24)
screen fading_text(text, t, x, y, move_x, move_y, color, size):
        add Text(text) at fade_move_with_pars(t, x, y, move_x, move_y, color, size)
transform fade_move_with_pars(t, x, y, move_x, move_y, color, size):
    parallel:
        alpha 1.0
        linear t alpha 0
    parallel:
        pos (x, y)
        linear t pos (move_x, move_y)