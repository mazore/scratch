from constants import BLOCK_BAR_WIDTH, CODING_AREA_WIDTH, CODING_AREA_HEIGHT, SNAP_RANGE
from helpers import constrain, distance
from math import inf
from snap_point import SnapPoint


class Block:
    def __init__(self, coding_area, x, y, geometry, bottom_notch_height=5, top_notch_height=0, **kwargs):
        self.coding_area = coding_area
        self.x = x
        self.y = self.start_y = y
        self.geometry = geometry

        self.min_width = 0
        self.bottom_notch_height, self.top_notch_height = bottom_notch_height, top_notch_height
        self.snappable_top = True
        self.snappable_bottom = True
        self.is_returning = False
        self.has_inside = False

        self.drag_info = None
        self.snap_point = None

        xs = [v for i, v in enumerate(self.geometry) if i % 2 == 0]
        ys = [v for i, v in enumerate(self.geometry) if i % 2 == 1]
        self.bare_width = self.width = max(xs) - min(xs)
        self.bare_height = self.height = max(ys) - min(ys) - bottom_notch_height - top_notch_height

        self.above = None
        self.below = None
        self.held_by_field = None
        self.inside_block = None

        self.children = []

        options = dict(fill='light gray', outline='black')
        for key, value in kwargs.items():
            options[key] = value
        self.id = coding_area.create_polygon(*geometry, **options)
        self.update_pos()

        self.coding_area.tag_bind(self.id, '<Button-3>', self.remove)
        self.make_draggable(self.id)

    def remove(self, _=None):
        self.coding_area.blocks.remove(self)
        self.coding_area.delete(self.id)
        for child in self.children:
            self.coding_area.delete(child.id)
            if hasattr(child, 'text_id'):
                self.coding_area.delete(child.text_id)
            if hasattr(child, 'entry_id') and child.entry_id is not None:
                self.coding_area.delete(child.entry_id)
            if hasattr(child, 'held_block') and child.held_block is not None:
                child.held_block.remove()
        if self.below is not None:
            self.below.remove()
        if hasattr(self, 'inside_block') and self.inside_block is not None:
            self.inside_block.remove()

    def children_config(self):
        x = 5
        for child in self.children:
            child.x_offset = x
            child.update_width()
            x += child.width
            child.setup()
            if child.is_draggable:
                self.make_draggable(child.id)
        self.update_dimensions()

    def make_draggable(self, id_):
        self.coding_area.tag_bind(id_, '<Button-1>', self.drag_start)
        self.coding_area.tag_bind(id_, '<Button1-Motion>', self.drag_motion)
        self.coding_area.tag_bind(id_, '<ButtonRelease-1>', self.drag_stop)

    def get_block_stack(self):
        if self.below is None:
            return [self]
        return [self] + self.below.get_block_stack()

    def get_top_block(self):
        if self.above is None:
            if self.held_by_field is None:
                return self
            return self.held_by_field.parent_block.get_top_block()
        return self.above.get_top_block()

    def update_pos(self):
        self.coding_area.tag_raise(self.id)
        [self.coding_area.tag_raise(child.id) for child in self.children]

        geometry = []
        for i, coord in enumerate(self.geometry):
            if i % 2 == 0:  # if is x
                geometry.append(coord + self.x)
            else:  # if is y
                geometry.append(coord + self.y)
        self.coding_area.coords(self.id, *geometry)

        [child.update_pos() for child in self.children]

        if self.below is not None:
            self.below.x = self.x
            self.below.y = self.y + self.height
            self.below.update_pos()

    def update_dimensions(self):
        width = 5
        for child in self.children:
            width += child.padding[0]
            child.x_offset = width
            child.update_width()
            if hasattr(child, 'held_block') and child.held_block is not None:
                width += child.held_block.width + child.padding[1]
            else:
                width += child.width + child.padding[1]
        width += 3
        width = constrain(width, min_val=self.min_width)

        for i in range(len(self.geometry)):
            if i % 2 == 0:  # if is x
                if self.geometry[i] == self.width:
                    self.geometry[i] = width
        self.width = width

        diffs = [0]
        for child in self.children:
            if child.held_block is not None:
                diffs.append(child.held_block.height - child.height)
        width = max(diffs)
        for i in range(len(self.geometry)):
            if i % 2 == 1:  # if is y
                if self.geometry[i] == self.height:
                    self.geometry[i] = self.bare_height + width
                if self.geometry[i] == self.height + self.bottom_notch_height:
                    self.geometry[i] = self.bare_height + width + self.bottom_notch_height
        self.height = self.bare_height + width

        if self.held_by_field is not None:
            self.held_by_field.parent_block.update_dimensions()

        self.update_pos()

    def drag_start(self, event):
        if self.x < BLOCK_BAR_WIDTH:  # add new block at current position
            from blocks import block_types
            for block_type in block_types:
                exec('from blocks import ' + block_type.__name__)
            block = eval(f'{type(self).__name__}(self.coding_area, self.x, self.start_y)')
            block.y += self.coding_area.scroll_y
            block.update_pos()
            self.coding_area.blocks.append(block)
            self.coding_area.tag_raise(self.id)

        self.coding_area.remove_all_entries()

        self.drag_info = {
            'block_start': (self.x, self.y),
            'screen_start': (event.x, event.y)
        }
        prev_top_block = self.get_top_block()
        if self.above is not None:
            if self.above.has_inside and self.above.inside_block is self:
                self.above.inside_block = None
            else:
                self.above.below = None
            self.above = None

        if self.snap_point is not None and self.snap_point.on_detach is not None:
            self.snap_point.on_detach(self.snap_point, self)
        self.snap_point = None

        for _ in range(5):
            prev_top_block.update_pos()

        self.update_pos()

    def drag_motion(self, event):
        block_start_x, block_start_y = self.drag_info['block_start']
        screen_start_x, screen_start_y = self.drag_info['screen_start']
        dx = event.x - screen_start_x
        dy = event.y - screen_start_y
        self.x = block_start_x + dx
        self.y = block_start_y + dy

        self.x = constrain(self.x, min_val=-self.width + 10, max_val=CODING_AREA_WIDTH - 10)
        self.y = constrain(self.y, min_val=-self.height + 10, max_val=CODING_AREA_HEIGHT - 10)

        self.update_pos()

    def drag_stop(self, _):
        self.drag_info = None

        self.snap_point = self.closest_snap_point()
        if self.snap_point is not None:
            self.snap_point.on_snap(self.snap_point, self)
            for _ in range(5):
                self.get_top_block().update_pos()

        self.update_pos()

        if self.x < BLOCK_BAR_WIDTH:
            self.remove()
            self.coding_area.refresh_var_blocks()

    def closest_snap_point(self):
        snap_points = []
        for block in self.coding_area.blocks:
            if block is self:
                continue
            snap_points.extend(block.get_snap_points(self))

        result = None
        closest_dist = inf
        for snap_point in snap_points:
            dist = distance(self.x, self.y, snap_point.x, snap_point.y)
            if dist > SNAP_RANGE:
                continue
            if dist < closest_dist:
                closest_dist = dist
                result = snap_point
        return result

    def get_snap_points(self, other):
        if self.x < BLOCK_BAR_WIDTH:
            return []

        result = []

        if self.above is None and self.snappable_top and other.get_block_stack()[-1].snappable_bottom:
            y_offset = sum([block.height for block in other.get_block_stack()])
            result.append(SnapPoint(self.x, self.y - y_offset, self.snapped_to_above))

        if self.below is None and self.snappable_bottom and other.snappable_top:
            result.append(SnapPoint(self.x, self.y + self.height, self.snapped_to_below))

        elif self.below is not None and self.snappable_bottom and other.snappable_top and other.snappable_bottom:
            result.append(SnapPoint(self.x, self.y + self.height, self.snapped_to_insert_below))

        for child in self.children:
            if hasattr(child, 'get_snap_points'):
                result.extend(child.get_snap_points(other))

        return result

    def snapped_to_above(self, snap_point, other):
        other.x, other.y = snap_point.pos
        self.above = other.get_block_stack()[-1]
        other.get_block_stack()[-1].below = self

    def snapped_to_below(self, snap_point, other):
        other.x, other.y = snap_point.pos
        self.below = other
        other.above = self

    def snapped_to_insert_below(self, snap_point, other):
        prev_below = self.below

        other.x, other.y = snap_point.pos
        self.below = other
        other.above = self

        prev_below.above = other.get_block_stack()[-1]
        other.get_block_stack()[-1].below = prev_below

    def after_run(self, run_number):
        if self.below is None:
            top_block = self.get_top_block()
            prev_block = self
            block = self.above
            while True:  # find closest loop up
                if block.has_inside and block.inside_block is prev_block:
                    break
                if block.above is None:
                    if hasattr(top_block, 'event_name') and top_block.event_name == 'run':
                        self.coding_area.root.chunk_finished()
                    return
                prev_block = block
                block = block.above
            block.contents_done(run_number)

    def encode(self):
        return {
            'type': type(self).__name__,
            'x': self.x,
            'y': self.start_y,
            'children': [child.encode() for child in self.children],
            'below': None if self.below is None else self.below.encode(),
            'inside_block': self.inside_block.encode() if self.has_inside and self.inside_block is not None else None
        }
