"""Custom exception classes for the Grand Line Character Builder API.

All exceptions inherit from RPGBaseException so callers can catch
either specific errors or all application errors with one handler.
"""


class RPGBaseException(Exception):
    """Base exception class for all Grand Line Character Builder errors.

    All custom exceptions in this application inherit from this class,
    allowing routes to catch any application error with a single except.
    """
    pass


class CharacterNotFoundException(RPGBaseException):
    """Raised when a character cannot be found in the database.

    Attributes:
        character_id: The ID that was not found.
    """

    def __init__(self, character_id: int) -> None:
        """Initialise with the missing character ID.

        Args:
            character_id: The ID of the character that was not found.
        """
        self.character_id = character_id
        super().__init__(f"Character with ID {character_id} was not found.")


class ClassNotFoundException(RPGBaseException):
    """Raised when a character class name does not exist in the database.

    Attributes:
        class_name: The class name that was not found.
    """

    def __init__(self, class_name: str) -> None:
        """Initialise with the missing class name.

        Args:
            class_name: The name of the class that was not found.
        """
        self.class_name = class_name
        super().__init__(f"Character class '{class_name}' was not found.")


class RaceNotFoundException(RPGBaseException):
    """Raised when a race name does not exist in the database.

    Attributes:
        race_name: The race name that was not found.
    """

    def __init__(self, race_name: str) -> None:
        """Initialise with the missing race name.

        Args:
            race_name: The name of the race that was not found.
        """
        self.race_name = race_name
        super().__init__(f"Race '{race_name}' was not found.")


class InvalidStatValueError(RPGBaseException):
    """Raised when a stat value is outside the allowed range of 1 to 20.

    Attributes:
        stat_name: The name of the invalid stat.
        value: The invalid value that was provided.
    """

    def __init__(self, stat_name: str, value: int) -> None:
        """Initialise with the stat name and invalid value.

        Args:
            stat_name: The name of the stat that failed validation.
            value: The value that was out of range.
        """
        self.stat_name = stat_name
        self.value = value
        super().__init__(f"Invalid value {value} for '{stat_name}'. Must be between 1 and 20.")


class InvalidCharacterNameError(RPGBaseException):
    """Raised when a character name is empty or exceeds 50 characters.

    Attributes:
        name: The invalid name that was provided.
    """

    def __init__(self, name: str) -> None:
        """Initialise with the invalid name.

        Args:
            name: The name that failed validation.
        """
        self.name = name
        super().__init__(f"Invalid name '{name}'. Must be 1 to 50 characters.")


class InvalidLevelError(RPGBaseException):
    """Raised when a character level is outside the allowed range of 1 to 20.

    Attributes:
        level: The invalid level that was provided.
    """

    def __init__(self, level: int) -> None:
        """Initialise with the invalid level.

        Args:
            level: The level value that was out of range.
        """
        self.level = level
        super().__init__(f"Invalid level {level}. Must be between 1 and 20.")