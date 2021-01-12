class SnapPoint:
    def __init__(self, x, y, on_snap, on_detach=None):
        self.x, self.y = x, y
        self.on_snap = on_snap
        self.on_detach = on_detach

    @property
    def pos(self):
        return self.x, self.y
