from blocks.block import Block


class EventBlock(Block):
    def __init__(self, coding_area, x, y, event_name, min_width=0):
        width = 100
        points = [(0, 0), (20, -15), (60, -15), (80, 0), (width, 0),
                  (width, 25), (30, 25), (25, 30), (15, 30), (10, 25), (0, 25)]

        geometry = []
        [geometry.extend(point) for point in points]
        super().__init__(coding_area, x, y, geometry, top_notch_height=15, fill='goldenrod')

        self.min_width = min_width
        self.snappable_top = False

        self.event_name = event_name
        coding_area.root.event_manager.subscriptions[event_name].append(self)

    def remove(self, _=None):
        super().remove(_)

        self.coding_area.root.event_manager.subscriptions[self.event_name].remove(self)
