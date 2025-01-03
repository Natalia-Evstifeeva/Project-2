import random

import printing_intro

roles_list = ['Мафия', 'Доктор', 'Комиссар', 'Мирный житель', 'Мирный житель'] #Список ролей

#Класс игрок, поля: имя, роль, статус (жив/мертв) изначально жив, цель
class Player:
    def __init__(self, name):
        self.name = name
        self.role = ''
        self.alive = True
        self.goal = ''

    def vote(self, player_to_vote_for):
        pass

#Дочерние классы от Player под каждую роль
class Mafia(Player):
    def __init__(self, name, players):
        super().__init__(name)
        self.role = 'Мафия'
        self.goal = 'убить всех, кроме себя'

        self.players = players
        self.player_to_kill = None

    def kill(self, player_to_kill):
        player = next((i for i in self.players if i.name == player_to_kill), None)
        player.alive = False



class Doctor(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Доктор'
        self.goal = 'предугадывая ходы мафии, лечить мирных жителей, находящихся под угрозой убийства'

        self.can_heal_myself = True

    def heal(self, player_to_heal):
       pass

class Detective(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Комиссар'
        self.goal = 'проверяя игроков, найти мафию и указать на нее остальным участникам, не выдав свою роль'

        self.player_to_check = None
        self.text_to_say = ''

    def check(self, player_to_check):
        pass

class Civilian(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Мирный житель'
        self.goal = 'вычислить мафию, выжить'

class Game:
    def __init__(self, roles_list):
        self.players = []  # Список игроков
        self.roles_list = roles_list.copy()
        self.user_role = None

        self.mafia = None
        self.doctor = None
        self.detective = None
        self.civilian1 = None
        self.civilian2 = None


    def randomize_players(self):  # Создает игроков и рандомит их роли, Игрок 1 - пользователь. Записывает всех игроков в список players
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

        self.user_role = self.players[0].role #роль юзера

    def print_players(self):
        for i in self.players:
            print(f'{i.name}: {i.role}, {i.alive}')

    def print_all_intro(self):#выводит вступление к игре
        printing_intro.print_intro(self, roles_list)

    def print_players_for_choosing(self, skip_Player_1):# выводит игроков которых пользователь может выбрать для дальнейших манипуляций
        if skip_Player_1:
            for i in self.players[1:]:
                print(i.name)
        else:
            for i in self.players:
                print(i.name)

    def player_chooser(self, player_not_to_choose):# выбирает и возвращает из списка рандомного игрока, не учитывая игрока переданного как аргумент
        tmp_list_of_players = self.players.copy()
        tmp_list_of_players = [i for i in tmp_list_of_players if i.name != player_not_to_choose]
        return (random.choice(tmp_list_of_players)).name


    def night(self):
        print('Город засыпает\nПросыпается Мафия, решает кого убить')

        # Обрабатываю роль мафии
        if self.user_role == 'Мафия':
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
        if self.user_role == 'Доктор':
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
        if self.user_role == 'Комиссар':
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

        if self.user_role == 'Комиссар':
            print(self.detective.text_to_say)

        print(f'Комиссар выбрал {self.detective.player_to_check}')  # Удалить потом

        print('Информация поступила Комиссару прямо в руки')
        print('Комиссар засыпает')


    def putting_decisions_to_reality_phase(self):# В этой функции решения, принятые ночью приводятся в действие
        if self.mafia.player_to_kill != self.doctor.player_to_heal:
            self.mafia.kill(self.mafia.player_to_kill)
            print(f'Этой ночью был убит {self.mafia.player_to_kill}, его роль: {next((i for i in self.players if i.name == self.mafia.player_to_kill), None).role}')
        else:
            print('Этой ночью никого не убили')

        print('Также поступила информация о том, что', self.detective.text_to_say, '\nЭтой информации можно доверять.')


game1 = Game(roles_list)
game1.randomize_players()
game1.print_players()
game1.print_all_intro()

print('\nИгра начинается')

game1.night()

print('\nПросыпается город')

game1.putting_decisions_to_reality_phase()
game1.print_players()