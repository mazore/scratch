from blocks.block import Block


class VariableBlock(Block):
    def __init__(self, coding_area, x, y, is_action=False, min_width=0):
        width = 100
        if is_action:
            points = [(0, 0), (10, 0), (15, 5), (25, 5), (30, 0), (width, 0),
                      (width, 25), (30, 25), (25, 30), (15, 30), (10, 25), (0, 25)]
        else:
            points = [(0, 0), (width, 0), (width, 25), (0, 25)]

        geometry = []
        [geometry.extend(point) for point in points]
        super().__init__(coding_area, x, y, geometry, fill='maroon1', bottom_notch_height=5 if is_action else 0)

        self.min_width = min_width
        self.snappable_top = self.snappable_bottom = is_action
        self.is_returning = not is_action
