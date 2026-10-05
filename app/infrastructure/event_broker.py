from collections import defaultdict, deque
from typing import Callable

from app.common.events import Event
from app.common.observability import log_event


class EventBroker:

    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queues = defaultdict(deque)
        self.dead_letter_queue = deque()

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], None]
    ):
        self.subscribers[event_type].append(handler)

    def publish(self, event: Event):
        self.queues[event.event_type].append(event)

        log_event(
            f"Event published: {event.event_type}",
            event.correlation_id
        )

        self._deliver(event)

    def _deliver(self, event: Event):

        handlers = self.subscribers.get(
            event.event_type,
            []
        )

        if not handlers:
            log_event(
                f"No subscribers for {event.event_type}",
                event.correlation_id
            )
            return

        for handler in handlers:
            try:
                handler(event)

            except Exception as error:

                log_event(
                    f"Event processing failed: {error}",
                    event.correlation_id
                )

                self.dead_letter_queue.append(event)

    def get_dead_letters(self):
        return list(self.dead_letter_queue)
