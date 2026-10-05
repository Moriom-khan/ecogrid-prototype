class EventProcessingError(Exception):
    """Raised when an event cannot be processed."""
    pass


class DuplicateEventError(Exception):
    """Raised when an already processed event is received."""
    pass


class SettlementError(Exception):
    """Raised when settlement processing fails."""
    pass
