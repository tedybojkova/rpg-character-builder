import random
import logging
from typing import List


logger = logging.getLogger(__name__)


class DiceRoller:

    def roll(self, sides: int, count: int = 1) -> int:
        if sides < 2:
            raise ValueError(f"A die must have at least 2 sides, got {sides}.")
        if count < 1:
            raise ValueError(f"Must roll at least 1 die, got {count}.")

        results = [random.randint(1, sides) for _ in range(count)]
        total = sum(results)

        logger.debug("Rolled %dd%d: results=%s, total=%d", count, sides, results, total)
        return total

    def roll_4d6_drop_lowest(self) -> int:
        rolls = sorted([random.randint(1, 6) for _ in range(4)])
        total = sum(rolls[1:])
        logger.debug("Rolled 4d6 drop lowest: rolls=%s, total=%d", rolls, total)
        return total

    def roll_stat_array(self) -> List[int]:
        stats = [self.roll_4d6_drop_lowest() for _ in range(6)]
        logger.info("Rolled stat array: %s", stats)
        return stats