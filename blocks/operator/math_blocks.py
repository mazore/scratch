from blocks.operator_block import OperatorBlock
from block_children import *


class MathBlock(OperatorBlock):
    def __init__(self, coding_area, x, y, symbol, display_symbol=None, blank=False):
        super().__init__(coding_area, x, y)

        self.symbol = symbol
        self.children = [Field(self, default='' if blank else '2'),
                         Text(self, symbol if display_symbol is None else display_symbol),
                         Field(self, default='' if blank else '2')]

        super().children_config()

    def run(self, _=None):
        left, right = self.children[0].val, self.children[2].val
        try:
            return eval(f'{float(left)} {self.symbol} {float(right)}')
        except (NameError, TypeError, ValueError):
            print(f'{type(self).__name__}: Input not valid')


class AddBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '+')


class SubtractBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '-')


class MultiplyBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '*')


class DivideBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '/')


class ModulusBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '%')


class GreaterThanBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '>')


class LessThanBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '<')


class EqualToBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, '==', display_symbol='=')


class AndBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, 'and', blank=True)


class OrBlock(MathBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, 'or', blank=True)
