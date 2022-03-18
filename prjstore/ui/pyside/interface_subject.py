class SubjectInterface:
    """Interface subject, who notifying the observer"""

    def register_observer(self, observer):
        ...

    def remove_observer(self, observer) -> None:
        ...

    def notify_observer(self, this_observer) -> None:
        """notifying the observer"""
        ...
