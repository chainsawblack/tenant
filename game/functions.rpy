##############################################################################
# The tenant v1.0 demo scriptcode
##############################################################################
# Вынесенные функции

##############################################################################
# Изменение уровня морали
label moral_changed(val, couse):
    if val > 0:
        $ moral_text = moral_encrease
    else:
        $ moral_text = moral_decrease
    $ moral += val # Мораль изменилась на переданный параметр
    $ extreme_moral = ""
    if moral > 200:
        $ moral = 200
        $ extreme_moral = u"Ваш моральный облик совершенен. Повсюду за собой вы оставляете добрую славу и крутящих у виска пальцем людей. Еще немного, и у нашего мессии появятся последователи и ученики..."
    elif moral < 0:
        $ moral = 0
        $ extreme_moral = u"Вы достигли морального дна. Удивительно, как земля вообще носит такое чудовище. Люди откровенно боятся и ненавидят психопатов вроде вас, знаете ли..."
    $ val = str(abs(val))
    if couse:
        $ game_events = couse + "\n" + moral_text + val + " единиц.\n\n" + game_events # Запись в лог.
    else:
        $ game_events = moral_text + val + " единиц.\n\n" + game_events # Запись в лог.
    if extreme_moral:
        $ game_events = extreme_moral + "\n" + game_events # Запись в лог.
return

##############################################################################
# Добавление записи в лог событий
label log_update(text):
    $ game_events = text + "\n\n" + game_events
return



##############################################################################
# Браузер
#
init python:
    def browser(link):
        import webbrowser
        webbrowser.open_new(link)
label browser:
    $ browser('http://ya.ru')


# Персонаж получил новое сообщение v1 - не беру в работу
label new_message_received(messages_num):
    $ unread_messages += messages_num
    show screen gui_game_menu(unread_messages)
return




##############################################################################
# Кастомный курсор - не работает
#
init python:
    
    class custom_cursor(renpy.Displayable):
        
        def __init__(self, cursorlist, dark=False, **kwargs):
            super(custom_cursor, self).__init__(**kwargs)
            
            self.x = 0
            self.y = 0
            self.cursorlist = cursorlist
            
            self.child = None
            self.dark = dark
            if dark:
                self.fl = renpy.displayable("no_flashlight.png")
            renpy.timeout(1)
            return
            
        def render(self, width, height, at, st):
            if self.child:
                rc = renpy.render(self.child, width, height, at, st)
                r = renpy.Render(config.screen_width, config.screen_height)
                r.blit(rc, (self.x - self.xoff, self.y - self.yoff))
                if self.dark:
                    rd = renpy.render(self.fl, width, height, at, st)
                    r.blit(rd, (self.x - config.screen_width, self.y - config.screen_height))
            else:
                if self.dark:
                    r = renpy.Render(config.screen_width, config.screen_height)
                    rd = renpy.render(self.fl, width, height, at, st)
                    r.blit(rd, (0, 0))
                else:
                    r = renpy.Render(0, 0)
            return r
            
        def event(self, ev, x, y, st):
            self.child = None
            if 0 <= x <= config.screen_width and 0 <= y <= config.screen_height:
                if self.dark:
                    self.fl = renpy.displayable("flashlight.png")
                for c in self.cursorlist:
                    if c[1] == "default":
                        self.child = renpy.displayable(c[0])
                        self.xoff = c[2][0]
                        self.yoff = c[2][1]
                        break
                        
                for c in self.cursorlist:
                    if c[1] != "default":
                        if c[1][0] <= x <= c[1][2] + c[1][0] and c[1][1] <= y <= c[1][3] + c[1][1]:
                            self.child = renpy.displayable(c[0])
                            self.xoff = c[2][0]
                            self.yoff = c[2][1]
                self.x = x
                self.y = y
            elif self.dark:
                self.fl = renpy.displayable("no_flashlight.png")
            renpy.redraw(self, 0)
            return
                        
        def visit(self):
            if self.dark:
                return [self.child, self.fl]
            return [self.child]
            
            









# Закрытие глобального кастомного диалога закрытия
label close_custom_global_exit:
    hide screen my_global_exit
return




# Вычисление текстового описания состояния морали персонажа
label moral_title:
    # $ moral_title = 
return

