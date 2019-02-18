EVENTS = {}


class SlackEvent(object):
    """
    Represents an incoming event from Slack.
    """
    event_type = "unknown"

    def __init__(self, data: dict):
        """
        Initializes an incoming event.

        :param data: The incoming event data.
        """
        self.data = data
