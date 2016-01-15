##############################################################################
# The tenant v1.0 demo scriptcode
##############################################################################
# Система для обмена текстовыми сообщениями в ShadowNet
# Экраны находятся в screens.rpy
# Инструкция по использованию:
# 
# $ add_message("Тема", "Sender_name", "Текст")
# $ add_message("Тема отложенного сообщения", "Sender_name", "Текст отложенного сообщения", delay=True)
# $ add_message("Тема сообщения с возможностью ответа", "Sender_name", "Текст сообщения с возможностью ответа ", "Sender_name_reply")
# 
# Для каждого сообщения с возможностью ответа требуется отдельная метка:
# label Sender_name_reply(current_message):
#     menu:
#         "Вариант ответа":
#             # Результат
#             $ current_message.can_reply = False
#         "Вариант ответа":
#             # Результат
#             $ current_message.can_reply = False
#         "Вариант ответа":
#             pass # Ничего не делаем
#     return
# 
# Отправка отложенных сообщений:
# $ deliver_next() 
# $ deliver_all()
# 
# Проверка прочтения сообщения по его теме:
# if check("Тема"):
#        e "Прочтено"
#    else:
#        e "Не прочтено" 
# 
# Добавление нового контакта, которому можно написать сообщение:
# $ some_name = Contact("Name", "name_draft")
# 
# Удаление:
# $ some_name.delete()
# 
# Потребуется отдельная метка:
# label name_draft(contact, message_title="Тема"):
#     menu:
#         "Вариант письма":
#             # Результат
#             $ contact.draft_label = None # Эту строку надо оставить, чтобы нельзя было отправить сообщение повторно 
#             $ add_message("Тема ответа", "Name", "Текст ответа")   
#         "Вариант письма":
#             # Результат
#             $ contact.draft_label = None
#             $ add_message("Тема ответа", "Name", "Текст ответа")            
#         "Вариант письма":
#             pass # Ничего не делаем
#     return



init python:
    import renpy.store as store
    
    reply_screen = False
    draft_screen = False

    class Mail(store.object):
        def __init__(self, subject, sender, body, reply_label=False, delay=False, view=True, read=False):
            self.subject = subject
            self.sender = sender
            self.body = body
            self.reply_label = reply_label
            self.delay = delay
            self.view = view
            self.read = read
            if delay:
                self.queued()
            else:            
                self.deliver()  
                
        def delete(self):
            self.view = False
            renpy.restart_interaction()
            
        def deliver(self):
            if self in mail_queue:
                mail_queue.remove(self)
            mail.insert(0, self)
            
        def mark_read(self):
            self.read = True 
            renpy.restart_interaction()         
            
        def queued(self):
            mail_queue.append(self)           
            
        def reply(self):
            global reply_screen
            reply_screen = True
            renpy.call_in_new_context(self.reply_label, current_message=self)                
            reply_screen = False            
            
        def restore(self):
            self.view = True  
            renpy.restart_interaction()            

    class Contact(store.object):
        def __init__(self, name, draft_label):
            self.name = name
            self.draft_label = draft_label  
            self.add_contact()
            
        def add_contact(self):
            contacts.append(self)

        def draft(self):
            global draft_screen
            draft_screen = True
            renpy.call_in_new_context(self.draft_label, contact=self)            
            draft_screen = False
            
        def delete(self):
            contacts.remove(self)

    def add_message(subject, sender, body, reply_label=False, delay=False):
        message = Mail(subject, sender, body, reply_label, delay)
        
    def check(subject):
        for item in mail:
            if item.subject == subject:
                if item.read:
                    return True
                else:
                    return False
                    
    def deliver_all(): 
        mail.extend(mail_queue)
        mail_queue = list()          
        
    def deliver_next():
        if mail_queue:
            mail_queue[0].deliver()

    def mark_all_read():
        unread_messages = [x for x in mail if not x.read]
        for x in unread_messages:
            x.mark_read()                

    def message_count():
        visible_messages = [x for x in mail if x.view]
        return len(visible_messages)
        
    def new_message_count():
        unread_messages = [ x for x in mail if not x.read]
        return len(unread_messages)
            
    def restore_all():
        deleted_messages = [x for x in mail if not x.view]
        for x in deleted_messages:
            x.restore()
        renpy.restart_interaction()