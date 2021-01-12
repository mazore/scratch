from blocks.block import Block
from constants import BLOCK_BAR_WIDTH
from snap_point import SnapPoint


class ControlBlock(Block):
    def __init__(self, coding_area, x, y, snappable_bottom=True,
                 top_part_height=25, bottom_part_height=15, empty_height=30, children_y_offset=0, min_width=0):
        self.inside_block = None
        self.children_y_offset = children_y_offset

        self.snappable_bottom = snappable_bottom
        self.bare_top_part_height = self.top_part_height = top_part_height
        self.bottom_part_height = bottom_part_height
        self.empty_height = empty_height

        super().__init__(coding_area, x, y, self.get_geometry(100, 50), fill='purple1')

        self.min_width = min_width
        self.snappable_bottom = snappable_bottom
        self.has_inside = True
        self.update_pos()

    def children_config(self):
        super().children_config()
        for child in self.children:
            child.y_offset = self.height / 2 - self.top_part_height/2 + self.children_y_offset
            child.update_pos()

    def get_geometry(self, width, height, flat_inside_bottom=False):
        w = width
        h = height - self.bottom_part_height
        b = self.bottom_part_height
        t = self.top_part_height
        points = [(0, 0), (10, 0), (15, 5), (25, 5), (30, 0), (w, 0),
                  (w, t), (40, t), (35, t + 5), (25, t + 5), (20, t), (10, t)]
        if flat_inside_bottom:
            points.extend([(10, h), (w, h)])
        else:
            points.extend([(10, h), (20, h), (25, h + 5), (35, h + 5), (40, h), (w, h)])
        if self.snappable_bottom:
            points.extend([(w, h + b), (30, h + b), (25, h + b + 5), (15, h + b + 5), (10, h + b), (0, h + b)])
        else:
            points.extend([(w, h + b), (w - 2, h + b + 2), (2, h + b + 2), (0, h + b)])
        geometry = []
        [geometry.extend(point) for point in points]
        return geometry

    def get_flat_inside_bottom(self):
        block = self.inside_block
        if block is None:
            return False
        while block.below is not None:
            block = block.below
        return not block.snappable_bottom

    def update_pos(self):
        self.height = self.get_height()
        self.geometry = self.get_geometry(self.width, self.height, flat_inside_bottom=self.get_flat_inside_bottom())

        for i, child in enumerate(self.children):
            child.y_offset = self.height/2 - self.top_part_height/2 + self.children_y_offset

        super().update_pos()

        if self.inside_block is not None:
            self.inside_block.x = self.x + 10
            self.inside_block.y = self.y + self.top_part_height
            self.inside_block.update_pos()

    def get_height(self):
        diffs = [0]
        for child in self.children:
            if child.held_block is not None:
                diffs.append(child.held_block.height - child.height)
        inc = max(diffs)
        for i in range(len(self.geometry)):
            if i % 2 == 1:  # if is y
                if self.geometry[i] == self.height:
                    self.geometry[i] = self.bare_height + inc
                if self.geometry[i] == self.height + self.bottom_notch_height:
                    self.geometry[i] = self.bare_height + inc + self.bottom_notch_height
        self.top_part_height = self.bare_top_part_height + inc
        for i, child in enumerate(self.children):
            child.y_offset = self.height / 2 - 15 + self.children_y_offset

        if self.inside_block is None:
            return self.top_part_height + self.empty_height
        height = self.top_part_height
        block = self.inside_block
        height += block.height
        while block.below is not None:
            height += block.below.height
            block = block.below
        return height + self.bottom_part_height

    def get_snap_points(self, other):
        if self.x < BLOCK_BAR_WIDTH:
            return []

        result = super().get_snap_points(other)

        if self.inside_block is None and other.snappable_top:
            result.append(SnapPoint(self.x + 10, self.y + self.top_part_height, self.snapped_to_inside))

        if self.inside_block is not None and other.snappable_top and other.snappable_bottom:
            result.append(SnapPoint(self.x + 10, self.y + self.top_part_height, self.snapped_to_inside_insert))

        return result

    def snapped_to_inside(self, snap_point, other):
        other.x, other.y = snap_point.pos
        other.above = self
        self.inside_block = other
        self.get_top_block().update_pos()

    def snapped_to_inside_insert(self, snap_point, other):
        prev_inside = self.inside_block

        other.x, other.y = snap_point.pos
        self.inside_block = other
        other.above = self

        prev_inside.above = other.get_block_stack()[-1]
        other.get_block_stack()[-1].below = prev_inside

        self.get_top_block().update_pos()
