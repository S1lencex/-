import numpy as np
import pandas as pd
import os
import random
import math
import time


# макс, 3 важнейшие функции для переноса логики в Тг бота это: text_input(), messager(), buttons()

question_all = ['Вывести расписание кружков','Информация о кружке','Вывести все кружки и их преподавателей']
question_student = ['Приглашения на кружки','Записаться/Покинуть кружок','Предупредить об отсутствии','Написать Админу (тех поддержка)','Изменить данные своего аккаунта']
question_teacher = ['Редактировать свой кружок','Принять/исключить участника','Изменить логин (ФИО) ученика','Список участников своего кружка','Написать Админу (тех поддержка)','Изменить данные своего аккаунта']
question_admin = ['Редактировать любой кружок','Список учеников','Добавить/удалить кружок','Редактировавть любой аккаунт','Создать/удалить аккаунт','Просмотреть сообщения']
#question_admin_plus = []

#!!!!!!!!!!!!!!!!!! обновление даты там где надо
#!!!!!!!!!!!!!!!!!! слишком простой пароль
#!!!!!!!!!!!!!!!!!! фио не из 3х строк.
#!!!!!!!!!!!!!!!!!! особые символы для команд /1 например
#!!!!!!!!!!!!!!!!!! двойные пробелы в логине
#!!!!!!!!!!!!!!!!!! баг с классом (закоментированно) + проверка (есть еще баги(например с номером класса))
#!!!!!!!!!!!!!!!!!! оптимизация if заменить на elif там где можно
#!!!!!!!!!!!!!!!!!! отредачить текст (поиск ошибок там и тд)

#!!!!!!!!!!!!!!!!!! фичи: посик ошибок в создании акков, сортировка и вывод участников по полу классу и тд)

attempt = 7
data_circle=pd.read_csv('circle.csv')
data_students=pd.read_csv('students.csv')
data_acc=pd.read_csv('acc.csv')

def text_input(): # эта функция записывает в переменную сообщение, написанное тобой в ответ на какой-то вопрос.
  try:
    answer = str(input('сообщение: ')) # тут это и происходит
  except Exception:
    messager('какая-то ошибка ._. попробуйте заново') # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! переместить
    return ''
  return answer

def messager(text_message): # эта функция просто отправляет сообщение с текстом переменной text_message
  print(text_message)

def buttons(text_buttons): # эта функция создает кнопки, при нажатии на которых выполняются дальнейшие команды. переменная text_buttons - это список, длина которого это количество кнопок, а его элементы это текст кнопок (например text_buttons = ['добавить участников','записаться на кружок'], то есть будут 2 кнопки (текст первой: добавить участников, текст второй: записаться на кружок))
  for text_button in text_buttons: # тут цыкл, каждое исполнение которого создает кнопку (важно, кнопки не должны исчезать после конца цыкла и появиться их должно столько, сколько надо (например 2, если длина списка text_buttons равна 2), если с помощью цыкла сделать нельзя, то перепиши эту функцию)
    button = text_button # тут создается собственно кнопка с текстом text_button
    print(f'[{button}] ', end='') # тут эта кнопка выводится к остальным кнопкам (счетчик i лучше удали, он нужен только для тестовой версии логики, а еще он указывает на число, номер кнопки(так что тебе может приготиться))
  # если пользователь нажал на кнопку, то должно отправиться сообщение, текст которого номер нажатой кнопки (можешь новую функцию для этого создать, или в этой сделай)
  # пока эта функция только выводит текст кнопок. а должна создавать кнопки и при нажатии на какую-то из них отправлять сообщение с номером этой кнопки (номер начинается от 1 и т.д) (причем сообщение отправляется от имени пользователя.)

def autorisation(): # Функция авторизации. должна вызываться единожды, думаю после команды /start в Тг (типо на одном устройстве регаться нужно 1 раз, не каждый раз, когда заходишь в Тг!!)
  messager('\nКак вы хотите авторизоваться?\nВойти, используя логин и пароль или\nСоздать аккаунт с нуля (права "ученика")')
  buttons(['войти','создать аккаунт'])
  answ_autorisation = text_input()

  if answ_autorisation == '':
    return autorisation()

  if answ_autorisation == '1':
    return autorisation_input()
    
  elif answ_autorisation == '2':
    return autorisation_create()

  else:
    messager('\nПохоже вы ввели что-то не то или не нажали на какую-то из кнопок. Попробуйте заново')
    return autorisation()

def autorisation_input(): # вход под своим акком
  global account, password, attempt

  if attempt <= 4 and attempt >= 0: # кол-во попыток ограниченно до 7
    messager(f'\nосталось {attempt} попыток до временной блокировки')

  if attempt <= 0: # кол-во попыток ограниченно до 7
    messager('\nпопытки закончились, зайдите чуть позже') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! установить тоянй таймер.
    return autorisation()

  messager('\nВведите логин (ФИО). (без дополнительных символов)\nПример: Брунов Максим Николаевич, Бондаренко Светлана Николаевна')
  buttons(['другой способ авторизации'])
  account = text_input()

  if account == '1':
    return autorisation()

  if account == '':
    return autorisation_input()

  messager('\nВведите пароль. (без дополнительных символов)\nПример: 111222333abc')
  buttons(['другой способ авторизации'])
  password = text_input()

  if password == '1':
    return autorisation()

  if password == '':
    return autorisation_input()

  if ((data_acc[data_acc['Account'].isin([account])])['Password'] == password).to_list() == [True]: # проверка, совпадает ли пароль с логином !!!!!!!!!!!!!!!!!!!!!!!         верноооооооо              !!!!!!!!!!!!!!
    return first_start()

  else:
    attempt -= 1
    if attempt == 1:
      messager('\nНеправильный логин или пароль')

    else:
      messager('\nНеправильный логин или пароль. Попробуйте заново')

    return autorisation_input()

def autorisation_create(): # создание акка, создание логина
  global account

  messager('\nСоздайте логин (ФИО). (без лишних пробелов между словами)\nПример: Брунов Максим Николаевич, Бондаренко Светлана Николаевна\nВажно! Вводите свое реальное ФИО, так как изменить его может только админ.')
  buttons(['другой способ авторизации'])
  account = text_input()
  account = account.strip()

  if account == '1':
    return autorisation()

  if account == '':
    return autorisation_create()

  if len(account) <= 3:
    messager('\nСлишком короткий логин. Попробуйте заново.')
    return autorisation_create()
  
  if ((data_acc[data_acc['Account'].isin([account])])['Account'] == account).to_list(): # проверка, есть ли в базе такой акк !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    messager('\nТакой логин уже имеется в Базе.')
    return autorisation_create()
 
  return autorisation_create_password()

def autorisation_create_password(): # создание пароль
  global password

  messager('\nСоздайте пароль. (без пробелов между частями пароля)\nПример: 112233abc')
  buttons(['Назад'])
  password = text_input()
  password = password.strip()

  if password == '1':
    return autorisation_create()

  if password == '':
    return autorisation_create_password()

  if len(password) <= 4:
    messager('\nСлишком короткий пароль. Придумайте новый.')
    return autorisation_create_password()

  if password == '112233abc':
    messager('\nтупой? Еще раз.')
    return autorisation_create_password()
  
  for str_passw in password:
    if str_passw == ' ':
      messager('\nПовторите попытку, в пароле присутствуют пробелы.')
      return autorisation_create_password()

    if str_passw not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789':
      messager('\nПовторите попытку, в пароле присутствуют непотребные символы. (составьте пароль на англ. языке, цыфрами и символами "_-")')
      return autorisation_create_password()
  return autorisation_confirm_password()

def autorisation_confirm_password(): # подтверждение пароля
  global password
  
  messager('\nПодтвердите пароль')
  buttons(['Назад'])
  new_password = text_input()

  if new_password == '1':
    return autorisation_create_password()
  if new_password == '':
    return autorisation_confirm_password()

  if new_password != password:
    messager('\nПароли не совпадают, повторите попытку или придумайте новый пароль')
    return autorisation_confirm_password()
  return autorisation_create_acc()

def autorisation_create_acc(): # 
  global account, password, school_class, gender

  messager(f'\nВы уверенны, что хотите создать аккаунт с такими данными?\nЛогин - {account}\nПароль - {password}') #\nКласс - {school_class}\nПол - {gender}
  buttons(['Нет, изменить данные','Да, все верно'])
  create_answer = text_input()

  if create_answer == '1':
    return autorisation_create()

  if create_answer == '2':
    data_acc = pd.read_csv('acc.csv') # обновление
    data_acc = data_acc.append({'Num acc': data_acc['Num acc'].max() + 1, 'Account': account, 'Password': password, 'law': 'Student'}, ignore_index=True) # создание акка, добавление его в дату (оффлайн)
    data_acc.to_csv('acc.csv', index=False) # добавление акка в дату (онлайн)
    messager('\nАккаунт успешно создан')
    return first_start()

  if create_answer == '':
    return autorisation_create_acc()

def first_start():
  global account

  data_acc=pd.read_csv('acc.csv')

  if ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Student').to_list() == [True]:
    messager(f'\nДобро пожаловать, {account}. В данный момент ваши права - Ученик.\nЕсли вы Преподаватель, то обратитесь к админу (для этого есть отдельная команда) для предоставления соответствующих прав.\n\nРекомендуем заполнить свои данные (')
    return main_question_student()
  elif ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Teacher').to_list() == [True]:
    messager(f'\nДобро пожаловать, {account}. В данный момент ваши права - Учитель.\nЕсли вы не являетесь преподавателем, то обратитесь к админу (для этого есть отдельная команда) для предоставления соответствующих прав.')
    return main_question_teacher()
  elif ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Admin').to_list() == [True]:
    messager(f'\nДобро пожаловать, {account}. В данный момент ваши права - Админ.')
    return main_question_admin()
  else:
    messager('\nСистема показывает, что у вас вообще нет никаких прав, либо права были не распозанны, а такого быть не должно.\nЗначит это баг, либо данные ващего аккаунта в Базе были изменены прользователем с более высокими правами. Попробуйте создать новый аккаунт и пожаловаться админу.')
    return autorisation()

def second_start():
  global account

  data_acc=pd.read_csv('acc.csv')

  if ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Student').to_list() == [True]:
    return main_question_student()
  elif ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Teacher').to_list() == [True]:
    return main_question_teacher()
  elif ((data_acc[data_acc['Account'].isin([account])])['law'] == 'Admin').to_list() == [True]:
    return main_question_admin()
  else:
    messager('\nСистема показывает, что у вас вообще нет никаких прав, либо права были не распозанны, а такого быть не должно.\nЗначит это баг, либо данные ващего аккаунта в Базе были изменены прользователем с более высокими правами. Попробуйте создать новый аккаунт и пожаловаться админу.')
    return autorisation()

def main_question_student():
  messager('\nОсновные команды:')
  buttons(question_all + question_student)

def main_question_teacher():
  messager('\nОсновные команды:')
  buttons(question_all + question_teacher)

def main_question_admin():
  messager('\nОсновные команды:')
  buttons(question_all + question_admin)
  answ_main_question = text_input()

  if answ_main_question == '':
    return main_question_admin()

  if answ_main_question == '1':
    return print_circle_timetable()
  elif answ_main_question == '2':
    return info_about_circle()
  elif answ_main_question == '3':
    return all_circle_and_teacher()
  elif answ_main_question == '4':
    return edit_any_circle()
  elif answ_main_question == '5':
    return list_of_students()
  elif answ_main_question == '6':
    return add_delete_circle()
  elif answ_main_question == '7':
    return edit_any_acc()
  elif answ_main_question == '8':
    return add_delete_acc()
  elif answ_main_question == '9':
    return look_message()

def print_circle_timetable():
  data_circle=pd.read_csv('circle.csv') #обновление даты

  list_circle_timetable = data_circle['Timetable'].to_list()
  list_circle_name = data_circle['Circle'].to_list()
  list_circle_name_and_timetable = []

  for list_id in range(len(data_circle)):
    list_circle_name_and_timetable.append(str(f'Расписание кружка <{list_circle_name[list_id]}> - {list_circle_timetable[list_id]}'))

  messager("\n".join(list_circle_name_and_timetable))
  return second_start()

def info_about_circle():
  data_circle=pd.read_csv('circle.csv') #обновление даты

  list_circle_name = data_circle['Circle'].to_list()
  list_circle_name_and_txt = []

  for list_id in range(len(data_circle)):
    list_circle_name_and_txt.append(str(f'Кружок <{list_circle_name[list_id]}> - {list_id + 1}'))

  messager("\n".join(list_circle_name_and_txt) + "\n\nОтправьте номер кружка, о котором хотите получить информацию (находится чуть правее названия кружка) следующим сообшением")

  buttons(['Вернуться на стадию назад'])
  nomber_of_circle = text_input()

  if nomber_of_circle == '':
    return info_about_circle()
  
  if nomber_of_circle == '1':
    return second_start()

  try:
    data_circle_row = data_circle[data_circle['Circle'].isin([list_circle_name[int(nomber_of_circle)-1]])]
    list_description = data_circle_row['Circle'].tolist() + data_circle_row['Description'].tolist() + data_circle_row['Equipment'].tolist() + ((data_acc[data_acc['Num acc'].isin([((data_circle_row['Num acc']).tolist())[0]])])['Account']).to_list() + data_circle_row['Timetable'].tolist()
    messager(f'Название кружка - {list_description[0]}\nОписание кружка - {list_description[1]}\nОборудование кружка - {list_description[2]}\nПреподаватель кружка - {list_description[3]}\nРасписание кружка - {list_description[4]}')
  except Exception:
    messager('\nПохоже вы ввели не число, либо число не в заданном диапазоне. Попробуйте заново')
    return info_about_circle()

  return second_start()

def all_circle_and_teacher():
  data_circle=pd.read_csv('circle.csv') #обновление даты

  list_circle_name = data_circle['Circle'].to_list()
  list_circle_teacher = []
  list_circle_name_and_teacher = []

  for nomber_of_circle in range(len(list_circle_name)):
    list_circle_teacher.append(((data_acc[data_acc['Num acc'].isin([(((data_circle[data_circle['Circle'].isin([list_circle_name[nomber_of_circle]])])['Num acc']).tolist())[0]])])['Account']).to_list())

  for list_id in range(len(data_circle)):
    list_circle_name_and_teacher.append(str(f'Учитель кружка <{list_circle_name[list_id]}> - {list_circle_teacher[list_id][0]}'))

  messager("\n".join(list_circle_name_and_teacher))
  return second_start()

def edit_any_circle():
  global list_description
  data_circle=pd.read_csv('circle.csv') #обновление даты

  list_circle_name = data_circle['Circle'].to_list()
  list_circle_name_and_txt = []

  for list_id in range(len(data_circle)):
    list_circle_name_and_txt.append(str(f'Кружок <{list_circle_name[list_id]}> - {list_id + 1}'))

  messager("\n".join(list_circle_name_and_txt) + "\n\nОтправьте номер кружка, который хотите изменить (находится чуть правее названия кружка) следующим сообшением")

  buttons(['Вернуться на стадию назад'])
  nomber_of_circle = text_input()

  if nomber_of_circle == '':
    return edit_any_circle()
  
  if nomber_of_circle == '1':
    return second_start()

  try:
    data_circle_row = data_circle[data_circle['Circle'].isin([list_circle_name[int(nomber_of_circle)-1]])]
    list_description = data_circle_row['Circle'].tolist() + data_circle_row['Description'].tolist() + data_circle_row['Equipment'].tolist() + ((data_acc[data_acc['Num acc'].isin([((data_circle_row['Num acc']).tolist())[0]])])['Account']).to_list() + data_circle_row['Timetable'].tolist()
    messager(f'Текущее название - {list_description[0]}\nТекущее описание - {list_description[1]}\nТекущее оборудование - {list_description[2]}\nТекущий преподаватель - {list_description[3]}\nТекущее расписание - {list_description[4]}')
  except Exception:
    messager('\nПохоже вы ввели не число, либо число не в заданном диапазоне. Попробуйте заново')
    return edit_any_circle()

  messager("\nУкажите, что хотите отредактировать в кружке")
  buttons(['Вернуться на стадию назад','Название','Описание','Оборудование','Преподавателя','Расписание'])
  what_change = text_input()

  if what_change == '':
    return edit_any_circle()
  
  if what_change == '1':
    return edit_any_circle()
  elif what_change == '2':
    return edit_any_circle_name()
  elif what_change == '3':
    return edit_any_circle_description()
  elif what_change == '4':
    return edit_any_circle_equipment()
  elif what_change == '5':
    return edit_any_circle_teacher()
  elif what_change == '6':
    return edit_any_circle_timetable()

def edit_any_circle_name():
  global list_description
  messager(f'\nТекущее название - {list_description[0]}\nУкажите, новое название кружка')
  buttons(['Вернуться на стадию назад'])
  new_name = text_input()

  if new_name == '':
    return edit_any_circle()
  
  if new_name == '1':
    return edit_any_circle()

  messager("\nВы уверены, что хотите изменить название кружка?")
  buttons(['Нет','Да'])
  yes_no = text_input()

  if yes_no == '':
    return edit_any_circle()
  
  if yes_no == '1':
    return edit_any_circle()
  elif yes_no == '2':

    messager("\nУспешно изменено")
    return second_start()



def edit_any_circle_description():
  pass

def edit_any_circle_equipment():
  pass

def edit_any_circle_teacher():
  pass

def edit_any_circle_timetable():
  pass






def list_of_students():
  pass

def add_delete_circle():
  pass

def edit_any_acc():
  pass

def add_delete_acc():
  pass

def look_message():
  pass










def main():
  global account
  #account = 'админ 1'
  autorisation()
  #first_start()

def passer():
  pass

main()
