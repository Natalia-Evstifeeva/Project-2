#Сложили два ума над этой программкой
#Не ругайте сильно)

import random
from colorama import init, Fore# Для окрашивания в красный текста
import printing_intro# Модуль для вывода intro в начале игры
import exceptions #Модуль для обработки ошибок

init()# Инициализирую colorama
print(Fore.RED)# делаем весь текст красным

roles_list = ['Мафия', 'Доктор', 'Комиссар', 'Мирный житель', 'Мирный житель'] #Список ролей

#Писала Полина, исключения добавляли вместе
#Класс игрок, поля: имя, роль, статус (жив/мертв) изначально жив, цель
class Player:
    """
    Класс, отвечающий за игрока(родитель классов Мафия, Доктор и тд).
    """
    def __init__(self, name):
        """
        Инициализирует нового игрока.
        """
        if not isinstance(name, str):# Если переданное имя некорректно
            raise exceptions.InvalidPlayerNameError(name)
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
        if not isinstance(name, str):
            raise exceptions.InvalidPlayerNameError(name)# Если переданное имя некорректно
        super().__init__(name)
        if not isinstance(players, list) or not all(isinstance(i, Player) for i in players):# Если в список переданы непонятные объекты или передан не список
            raise TypeError('players должен быть списком объектов класса Player или его дочерних.')
        self.role = 'Мафия'
        self.goal = 'убить всех, кроме себя'

        self.players = players
        self.player_to_kill = None

    def kill(self, player_to_kill):
        """
        Убивает указанного(переданного) игрока.
        """
        player = next((i for i in self.players if i.name == player_to_kill), None)
        if player is None:
            raise exceptions.PlayerNotFoundError(player_to_kill)# Игрок не найден
        if not player.alive:
            raise exceptions.PlayerAlreadyDeadError(player_to_kill)# Игрок уже мертв(а Цой еще жив))
        player.alive = False


class Doctor(Player):
    """
    Класс, отвечающий за Доктора
    """
    def __init__(self, name):
        """
        Инициализирует Доктора.
        """
        if not isinstance(name, str):
            raise exceptions.InvalidPlayerNameError(name)# Если переданное имя некорректно
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
        if not isinstance(name, str):
            raise exceptions.InvalidPlayerNameError(name)# Если переданное имя некорректно
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
        if not isinstance(name, str):
            raise exceptions.InvalidPlayerNameError(name)# Если переданное имя некорректно
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
        if not isinstance(roles_list, list):# Если передан не список
            raise TypeError('roles_list должен быть списком')
        for i in roles_list:
            if i not in ['Мафия', 'Доктор', 'Комиссар', 'Мирный житель']:
                raise exceptions.InvalidRoleError(i)# Некорректная роль (такой роли не может быть в списке)
        self.players = [] # Список всех игроков
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
        Выводит список всех игроков и их роль.
        """
        for i in self.players:
            print(f'{i.name}: {i.role}')

    def print_all_intro(self):
        """
        Выводит вступление к игре.
        """
        printing_intro.print_intro(self, roles_list)

    def print_players_for_choosing(self, skip_Player_1):# передаваемый параметр отвечает за вывод первого элемента aka самого пользлвателя
        """
        Выводит игроков, которых пользователь может выбрать для дальнейших манипуляций.
        """
        if not isinstance(skip_Player_1, bool):
            raise TypeError('skip_Player_1 должно принимать значение True или False') # Проверка на корректный тип данных
        for i in self.players:
            if i.alive:
                if skip_Player_1 and i.name != 'Игрок 1':
                    print(i.name)
                elif skip_Player_1 == False:
                    print(i.name)

    #Писала Полина
    def player_chooser(self, player_not_to_choose):
        """
        Выбирает и возвращает из списка рандомного игрока, не учитывая игрока переданного как аргумент
        """
        if not isinstance(player_not_to_choose, str):
            raise TypeError('player_not_to_choose должно принимать значение типа str') # Проверка на корректный тип данных
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
        if self.user_role.role == 'Мафия' and self.user_role.alive:
            print('Ваши варианты:')
            self.print_players_for_choosing(False)

            while True:
                try:
                    self.mafia.player_to_kill = input('Введите имя игрока, которого вы хотите убить: ')
                    if not self.mafia.player_to_kill:
                        raise ValueError("Имя игрока не может быть пустым.")
                    if not any(i.name == self.mafia.player_to_kill for i in self.in_game_players):
                        raise ValueError(f"Игрока с именем '{self.mafia.player_to_kill}' не существует.")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e}. Пожалуйста, попробуйте еще раз.")

        else: # это рандомный выбор игрока для убийства, если роль юзера не Мафия
            self.mafia.player_to_kill = self.player_chooser('')

        print('Мафия сделала свой безжалостный выбор')
        print('Мафия засыпает')

        # Обрабатываю роль доктора
        print('\nПросыпается доктор, решает кого исцелить')
        if self.user_role.role == 'Доктор' and self.user_role.alive:
            print('Ваши варианты:')
            if self.doctor.can_heal_myself:
                self.print_players_for_choosing(False)
                self.doctor.can_heal_myself = False
            else:
                self.print_players_for_choosing(True)

            while True:
                try:
                    self.doctor.player_to_heal = input('Введите имя игрока, которого вы хотите исцелить: ')
                    if not self.doctor.player_to_heal:
                        raise ValueError("Имя игрока не может быть пустым")
                    if not any(i.name == self.doctor.player_to_heal for i in self.in_game_players):
                        raise ValueError(f"Игрока с именем '{ self.doctor.player_to_heal}' не существует")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e}. Пожалуйста, попробуйте еще раз.")

        else:  # это рандомный выбор игрока для исцеления, если роль юзера не Доктор
            if self.doctor.can_heal_myself:
                self.doctor.player_to_heal = self.player_chooser('')
                self.doctor.can_heal_myself = False
            else:
                self.doctor.player_to_heal = self.player_chooser(f'{self.doctor.name}')

        print('Доктор сделал свой выбор')
        print('Доктор засыпает')

        # Обрабатываю роль Комиссара
        print('\nПросыпается комиссара, решает кого проверить')
        if self.user_role.role == 'Комиссар' and self.user_role.alive:
            print('Ваши варианты:')
            self.print_players_for_choosing(True)

            while True:
                try:
                    self.detective.player_to_check = input('Введите имя игрока, которого вы хотите проверить: ')
                    if not self.detective.player_to_check:
                        raise ValueError("Имя игрока не может быть пустым")
                    if not any(i.name == self.detective.player_to_check for i in self.in_game_players):
                        raise ValueError(f"Игрока с именем '{self.detective.player_to_check}' не существует")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e}. Пожалуйста, попробуйте еще раз.")
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
        if self.mafia.player_to_kill == 'Игрок 1':

            print('Вас убили, к сожалению, для вас игра окончена')
    #Привет от Наташи
    def voting_phase(self):
        """
        Осуществляет процесс голосования, как пользователя, так и рандомит голоса за системных игроков
        """
        self.find_players_in_game()# Удаляем из списка in_game_players игроков, которые ум$рли
        print('\nПроведем голосование')
        cur_player_while_choosing = ''
        if self.players[0].alive:
            print('Ваши варианты:')
            self.print_players_for_choosing(False)
            while True:
                try:
                    cur_player_while_choosing = input('Введите имя игрока, которого вы считаете мафией: ')
                    if not cur_player_while_choosing:
                        raise ValueError("Имя игрока не может быть пустым")
                    if not any(i.name == cur_player_while_choosing for i in self.in_game_players):
                        raise ValueError(f"Игрока с именем '{cur_player_while_choosing}' не существует")
                    break
                except ValueError as e:
                    print(f"Ошибка: {e} Пожалуйста, попробуйте еще раз.")

            self.players_chosen_during_voting.append(cur_player_while_choosing)
            for i in self.in_game_players[1:]: #обрезаем первого игрока тк он уже проголосовал
                self.players_chosen_during_voting.append(random.choice(self.in_game_players).name)
        else: #голосуют все, кто жив
            for i in self.in_game_players:
                    self.players_chosen_during_voting.append(random.choice(self.in_game_players).name)

        # находим наиболее часто упомянутого игрока, соответствующую ему роль и выводим информацию на экран
        player_chosen_by_voting = max(set(self.players_chosen_during_voting), key = self.players_chosen_during_voting.count)
        chosen_player = next((i for i in self.in_game_players if i.name == player_chosen_by_voting), None)
        print(f'По результатам голосования был выбран {chosen_player.name}, его роль была: {chosen_player.role}')
        if chosen_player.name == 'Игрок 1':
            print('За вас проголосовало большинство, к сожалению, ваша игра окончена')
        self.mafia.kill(player_chosen_by_voting)
        self.find_players_in_game()

#Думали вместе
game1 = Game(roles_list)
game1.randomize_players()
game1.print_all_intro()
# Фазы игры
while game1.mafia.alive and len(game1.in_game_players) > 2:
    game1.night()
    print('\nПросыпается город')
    game1.putting_decisions_to_reality_phase()
    if game1.user_role.alive and game1.mafia.alive and len(game1.in_game_players) > 2:
        game1.voting_phase()
print('Игра окончена!')
if game1.mafia.alive and len(game1.in_game_players) <= 2:
    print('Мафия победила!')
else:
    print('Мирные жители победили!')

print(game1.print_players())#выводим всех игроков и их роли, вскрываем карты)

