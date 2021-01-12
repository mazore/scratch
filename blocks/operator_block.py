from blocks.block import Block


class OperatorBlock(Block):
    def __init__(self, coding_area, x, y, min_width=0):
        width = 100
        points = [(0, 0), (width, 0), (width, 25), (0, 25)]

        geometry = []
        [geometry.extend(point) for point in points]
        super().__init__(coding_area, x, y, geometry, fill='lime green', bottom_notch_height=0)

        self.min_width = min_width
        self.snappable_top = self.snappable_bottom = False
        self.is_returning = True
