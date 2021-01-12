class EventManager:
    def __init__(self, root):
        self.root = root
        self.subscriptions = {
            'run': [],
            'clicked': []
        }

    def run_event(self, event):
        for block in self.subscriptions[event]:
            block.run(self.root.sprite_manager.root.run_number)
