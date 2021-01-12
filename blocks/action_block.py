from blocks.block import Block


class ActionBlock(Block):
    def __init__(self, coding_area, x, y, flat_bottom=False, min_width=0):
        width = 100
        if flat_bottom:
            points = [(0, 0), (10, 0), (15, 5), (25, 5), (30, 0), (width, 0),
                      (width, 25), (0, 25)]
        else:
            points = [(0, 0), (10, 0), (15, 5), (25, 5), (30, 0), (width, 0),
                      (width, 25), (30, 25), (25, 30), (15, 30), (10, 25), (0, 25)]

        geometry = []
        [geometry.extend(point) for point in points]
        super().__init__(coding_area, x, y, geometry,
                         bottom_notch_height=0 if flat_bottom else 5,
                         fill='cornflower blue')

        self.min_width = min_width
        self.snappable_bottom = not flat_bottom
