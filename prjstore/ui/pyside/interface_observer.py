class ObserverInterface:
    need_update: bool
    """Interface observer"""
    def update_data(self) -> None:
        ...
