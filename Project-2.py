#Сложили два ума над этой работой
#Не ругайте сильно)

import random
from colorama import init, Fore
import printing_intro# Модуль для вывода intro в начале игры

init()# Инициализирую colorama
print(Fore.RED)# делаю весь текст красным

roles_list = ['Мафия', 'Доктор', 'Комиссар', 'Мирный житель', 'Мирный житель'] #Список ролей

#Посала Полина
#Класс игрок, поля: имя, роль, статус (жив/мертв) изначально жив, цель
class Player:
    """
    Класс, отвечающий за игрока(родитель классов Мафия, Доктор и тд)
    """
    def __init__(self, name):
        """
        Инициализирует нового игрока.
        """
        self.name = name
        self.role = ''
        self.alive = True
        self.goal = ''

#Дочерние классы от Player под каждую роль
class Mafia(Player):
    """
    Класс, отвечающий за Мафию
    """
    def __init__(self, name, players):
        """
        Инициализирует Мафию.
        """
        super().__init__(name)
        self.role = 'Мафия'
        self.goal = 'убить всех, кроме себя'

        self.players = players
        self.player_to_kill = None

    def kill(self, player_to_kill):
        """
        Убивает указанного(переданного) игрока.
        """
        player = next((i for i in self.players if i.name == player_to_kill), None)
        player.alive = False



class Doctor(Player):
    """
    Класс, отвечающий за Доктора
    """
    def __init__(self, name):
        """
        Инициализирует Доктора.
        """
        super().__init__(name)
        self.role = 'Доктор'
        self.goal = 'предугадывая ходы мафии, лечить мирных жителей, находящихся под угрозой убийства'

        self.can_heal_myself = True


class Detective(Player):
    """
    Класс, отвечающий за Комиссара
    """
    def __init__(self, name):
        """
        Инициализирует Комиссара.
        """
        super().__init__(name)
        self.role = 'Комиссар'
        self.goal = 'проверяя игроков, найти мафию и указать на нее остальным участникам, не выдав свою роль'

        self.player_to_check = None
        self.text_to_say = ''


class Civilian(Player):
    """
    Класс, отвечающий за Мирных жителей
    """
    def __init__(self, name):
        """
        Инициализирует Мирного жителя.
        """
        super().__init__(name)
        self.role = 'Мирный житель'
        self.goal = 'вычислить мафию, выжить'

#Писала Наташа
class Game:
    """
    Класс, отвечающий за процесс игры
    """
    def __init__(self, roles_list):
        """
        Инициализирует игру, в нашем случае game1.
        """
        self.players = []  # Список всех игроков
        self.in_game_players = [] # Список игроков со статусом alive = True
        self.roles_list = roles_list.copy()
        self.user_role = None

        self.mafia = None
        self.doctor = None
        self.detective = None
        self.civilian1 = None
        self.civilian2 = None

        self.players_chosen_during_voting = []

    def randomize_players(self):  # Создает игроков и рандомит их роли, Игрок 1 - пользователь. Записывает всех игроков в список players
        """
        Создает игроков и рандомит их роли, более подробно в коментарие выше
        """
        player_number = 1
        while len(self.roles_list) > 0:
            cur_player_role = random.choice(self.roles_list)

            if cur_player_role == 'Мафия':
                self.mafia = Mafia(f'Игрок {player_number}', self.players)
                self.players.append(self.mafia)
            elif cur_player_role == 'Доктор':
                self.doctor = Doctor(f'Игрок {player_number}')
                self.players.append(self.doctor)
            elif cur_player_role == 'Комиссар':
                self.detective = Detective(f'Игрок {player_number}')
                self.players.append(self.detective)
            elif cur_player_role == 'Мирный житель':
                if self.civilian1 not in self.players:
                    self.civilian1 = Civilian(f'Игрок {player_number}')
                    self.players.append(self.civilian1)
                else:
                    self.civilian2 = Civilian(f'Игрок {player_number}')
                    self.players.append(self.civilian2)

            player_number += 1
            self.roles_list.remove(cur_player_role)

        self.user_role = self.players[0] #роль юзера
        self.in_game_players = self.players.copy() #заполняю всеми игроками из players

    def print_players(self):
        """
        Выводит список всех игроков и их статус.
        """
        for i in self.players:
            print(f'{i.name}: {i.role}, {i.alive}')

    def print_all_intro(self):
        """
        Выводит вступление к игре.
        """
        printing_intro.print_intro(self, roles_list)

    def print_players_for_choosing(self, skip_Player_1):# передаваемый параметр отвечает за вывод первого элемента aka самого пользлвателя
        """
        Выводит игроков, которых пользователь может выбрать для дальнейших манипуляций.
        """
        for i in self.players:
            if i.alive:
                if skip_Player_1 and i.name != 'Игрок 1':
                    print(i.name)
                elif skip_Player_1 == False:
                    print(i.name)

    #Писала Полина
    def player_chooser(self, player_not_to_choose):
        """
        Выбирает и возвращает из списка рандомного игрока, не учитывая игрока переданного как аргумент.
        """
        tmp_list_of_players = self.players.copy()
        tmp_list_of_players = [i for i in tmp_list_of_players if i.name != player_not_to_choose]
        return (random.choice(tmp_list_of_players)).name


    def find_players_in_game(self):#Заполняет список in_game_players игроками, которые не ум$рли
        """
        Выполняет роль модератора игры, записывая в список только игроков со статусом alive = True
        """
        self.in_game_players = [i for i in self.players if i.alive]


    #Над этой функцией страдала и Полина и Наташа
    def night(self):
        """
        Описывает все процессы происходящие в фазу игры "Ночь"
        """
        print('Город засыпает\nПросыпается Мафия, решает кого убить')

        # Обрабатываю роль мафии
        if self.user_role.role == 'Мафия':
            print('Ваши варианты:')
            self.print_players_for_choosing(False)
            self.mafia.player_to_kill = input('Введите имя игрока, которого вы хотите убить: ')
        else: # это рандомный выбор игрока для убийства, если роль юзера не Мафия
            self.mafia.player_to_kill = self.player_chooser('')

        print(f'Мафия выбрала {self.mafia.player_to_kill}') #Удалить потом

        print('Мафия сделала свой безжалостный выбор')
        print('Мафия засыпает')

        # Обрабатываю роль доктора
        print('\nПросыпается доктор, решает кого исцелить')
        if self.user_role.role == 'Доктор':
            print('Ваши варианты:')
            if self.doctor.can_heal_myself:
                self.print_players_for_choosing(False)
                self.doctor.can_heal_myself = False
            else:
                self.print_players_for_choosing(True)

            self.doctor.player_to_heal = input('Введите имя игрока, которого вы хотите исцелить: ')
        else:  # это рандомный выбор игрока для исцеления, если роль юзера не Доктор
            if self.doctor.can_heal_myself:
                self.doctor.player_to_heal = self.player_chooser('')
                self.doctor.can_heal_myself = False
            else:
                self.doctor.player_to_heal = self.player_chooser(f'{self.doctor.name}')

        print(f'Доктор выбрал {self.doctor.player_to_heal}')  # Удалить потом

        print('Доктор сделал свой выбор')
        print('Доктор засыпает')

        # Обрабатываю роль Комиссара
        print('\nПросыпается комиссара, решает кого проверить')
        if self.user_role.role == 'Комиссар':
            print('Ваши варианты:')
            self.print_players_for_choosing(True)

            self.detective.player_to_check = input('Введите имя игрока, которого вы хотите проверить: ')
            the_one_to_check = next((i for i in self.players if i.name == self.detective.player_to_check), None)


        else:  # это рандомный выбор игрока для проверки, если роль юзера не Комиссар
            self.detective.player_to_check = self.player_chooser(f'{self.detective.name}')
            the_one_to_check = next((i for i in self.players if i.name == self.detective.player_to_check), None)

        if the_one_to_check.role == 'Мафия':
            self.detective.text_to_say = f'{self.detective.player_to_check} - Мафия'
        else:
            self.detective.text_to_say = f'{self.detective.player_to_check} - не Мафия'

        if self.user_role.role == 'Комиссар':
            print(self.detective.text_to_say)

        print(f'Комиссар выбрал {self.detective.player_to_check}')  # Удалить потом

        print('Информация поступила Комиссару прямо в руки')
        print('Комиссар засыпает')

    #Привет от Полины
    def putting_decisions_to_reality_phase(self):# В этой функции решения, принятые ночью приводятся в действие
        """
        Обрабатывает все ходы игроков за ночь и приводит их в действие
        """
        if self.mafia.player_to_kill != self.doctor.player_to_heal:
            self.mafia.kill(self.mafia.player_to_kill)
            print(f'Этой ночью был убит {self.mafia.player_to_kill}, его роль: {next((i for i in self.players if i.name == self.mafia.player_to_kill), None).role}')
        else:
            print('Этой ночью никого не убили')

        print('Также поступила информация о том, что', self.detective.text_to_say, '\nЭтой информации можно доверять.')

    #Привет от Наташи
    def voting_phase(self):
        """
        Осуществляет процесс голосования, как пользователя, так и рандомит голоса за системных игроков
        """
        self.find_players_in_game()# Удаляем из списка in_game_players игроков, которые ум$рли
        print('\nПроведем голосование')
        if self.players[0].alive:
            print('Ваши варианты:')
            self.print_players_for_choosing(False)
            self.players_chosen_during_voting.append(input('Введите имя игрока, которого вы считаете мафией: '))
            for i in self.in_game_players[1:]: #обрезаем первого игрока тк он уже проголосовал
                self.players_chosen_during_voting.append(random.choice(self.in_game_players).name)
        else: #голосуют все, кто жив
            for i in self.in_game_players:
                    self.players_chosen_during_voting.append(random.choice(self.in_game_players).name)

        # находим наиболее часто упомянутого игрока, соответствующую ему роль и выводим информацию на экран
        player_chosen_by_voting = max(set(self.players_chosen_during_voting), key = self.players_chosen_during_voting.count)
        chosen_player = next((i for i in self.in_game_players if i.name == player_chosen_by_voting), None)
        print(f'По результатам голосования был выбран {chosen_player.name}, его роль была: {chosen_player.role}')
        self.mafia.kill(player_chosen_by_voting)
        self.print_players()

#Думали вместе
game1 = Game(roles_list)
game1.randomize_players()
game1.print_players()
game1.print_all_intro()
# Фазы игры
while game1.user_role.alive:
    game1.night()
    print('\nПросыпается город')
    game1.putting_decisions_to_reality_phase()
    game1.print_players()
    game1.voting_phase()


# while True:
#     # Проверяю условия для продолжения игры
#     if not any(i.role == 'Мафия' for i in game1.players) or len(game1.players) < 3:
#         print("Игра завершена: либо нет мафии, либо недостаточно игроков.")
#         break
#     # Проверка на смерть пользователя
#     if not any(i.name == 'Игрок 1' and not i.alive for i in game1.players):
#         print("Игрок 1 (пользователь) мертв. Игра завершена.")
#         break
# print('\nИгра начинается')
#
# #while game1.mafia.alive and len(game1.in_game_players) >= 3:
#     game1.night()
#     game1.putting_decisions_to_reality_phase()
# #if not game1.user_role.alive:
#     print('Для вас игра окончена')