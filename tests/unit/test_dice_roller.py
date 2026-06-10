import random
import pytest
from app.services.dice_roller import DiceRoller


@pytest.fixture
def roller():
    return DiceRoller()


class TestRollBasic:

    def test_roll_returns_integer(self, roller):
        result = roller.roll(sides=6)
        assert isinstance(result, int)

    def test_d6_always_in_range(self, roller):
        for _ in range(50):
            result = roller.roll(sides=6)
            assert 1 <= result <= 6

    def test_d20_always_in_range(self, roller):
        for _ in range(50):
            result = roller.roll(sides=20)
            assert 1 <= result <= 20

    def test_multiple_dice_sum(self, roller):
        for _ in range(50):
            result = roller.roll(sides=6, count=3)
            assert 3 <= result <= 18

    def test_invalid_sides_raises_error(self, roller):
        with pytest.raises(ValueError):
            roller.roll(sides=1)

    def test_invalid_count_raises_error(self, roller):
        with pytest.raises(ValueError):
            roller.roll(sides=6, count=0)


class TestRoll4d6DropLowest:

    def test_result_in_valid_range(self, roller):
        for _ in range(100):
            result = roller.roll_4d6_drop_lowest()
            assert 3 <= result <= 18

    def test_seeded_result_is_reproducible(self):
        random.seed(42)
        roller = DiceRoller()
        result_a = roller.roll_4d6_drop_lowest()

        random.seed(42)
        roller2 = DiceRoller()
        result_b = roller2.roll_4d6_drop_lowest()

        assert result_a == result_b


class TestRollStatArray:

    def test_returns_six_values(self, roller):
        stats = roller.roll_stat_array()
        assert len(stats) == 6

    def test_all_values_in_range(self, roller):
        stats = roller.roll_stat_array()
        for stat in stats:
            assert 3 <= stat <= 18

    def test_returns_list_of_ints(self, roller):
        stats = roller.roll_stat_array()
        assert all(isinstance(s, int) for s in stats)