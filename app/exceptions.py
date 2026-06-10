class RPGBaseException(Exception):
    pass


class CharacterNotFoundException(RPGBaseException):
    def __init__(self, character_id: int) -> None:
        self.character_id = character_id
        super().__init__(f"Character with ID {character_id} was not found.")


class ClassNotFoundException(RPGBaseException):
    def __init__(self, class_name: str) -> None:
        self.class_name = class_name
        super().__init__(f"Character class '{class_name}' was not found.")


class RaceNotFoundException(RPGBaseException):
    def __init__(self, race_name: str) -> None:
        self.race_name = race_name
        super().__init__(f"Race '{race_name}' was not found.")


class InvalidStatValueError(RPGBaseException):
    def __init__(self, stat_name: str, value: int) -> None:
        self.stat_name = stat_name
        self.value = value
        super().__init__(
            f"Invalid value {value} for '{stat_name}'. Must be between 1 and 20."
        )


class InvalidCharacterNameError(RPGBaseException):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(
            f"Invalid name '{name}'. Must be 1 to 50 characters."
        )


class InvalidLevelError(RPGBaseException):
    def __init__(self, level: int) -> None:
        self.level = level
        super().__init__(
            f"Invalid level {level}. Must be between 1 and 20."
        )