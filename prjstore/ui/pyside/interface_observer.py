class ObserverInterface:
    """Interface observer"""
    def update_data(self, store) -> None:
        ...
