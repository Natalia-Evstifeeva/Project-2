"""
Этот модуль реализует ряд классов для обработки потенциальных ошибок
"""
#Писали вместе
class GameError(Exception):
    """
    Базовый класс для исключений всей игры(наследуем от Exception).
    """
    pass

class InvalidPlayerNameError(GameError):#уже наследуем от GameError
    """
    Обработка ошибки, если имя игрока некорректно
    """
    def __init__(self, name):
        super().__init__(f'Некорректное имя игрока: {name}')

class InvalidRoleError(GameError):#уже наследуем от GameError
    """
    Обработка ошибки, если роль игрока некорректна
    """
    def __init__(self, role):
        super().__init__(f'Некорректная роль: {role}')


class PlayerNotFoundError(GameError):#уже наследуем от GameError
    """
    Обработка ошибки, если вместо игрока получено None(игрок отсутствует)
    """

    def __init__(self, player_name):
        super().__init__(f'Игрок с именем {player_name} не найден.')


class PlayerAlreadyDeadError(GameError):#уже наследуем от GameError
    """
    Обработка ошибки, если происходит попытка действий с мертвым игроком
    """

    def __init__(self, player_name):
        super().__init__(f'Игрок {player_name} уже мертв.')

