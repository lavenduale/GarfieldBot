
class SlackDataClass(object):
    """
    Represents a generic data class referring to a Slack object.
    """

    def __init__(self, data: dict):
        """
        Initializes the data class.

        :param data: The dictionary of data returned by Slack.
        """
        self.unprocessed_data = data
        self.__dict__.update(data)


class SlackEvent(SlackDataClass):
    """
    Represents an incoming event from Slack.
    """
    type: str = "unknown"


class HelloEvent(SlackEvent):
    """
    Represents a 'hello' event.
    Dispatched when the Slack client is connected.
    """
    pass


class UserTypingEvent(SlackEvent):
    """
    Represents a 'user_typing' event.
    Dispatched when a user begins typing.
    """
    channel: str = None
    user: str = None


class MessageEvent(SlackEvent):
    """
    Represents a 'message' event.
    Dispatched when a message is sent in a channel the bot can read from.
    """
    channel: str = None
    client_msg_id: str = None
    event_ts: str = None
    team: str = None
    ts: str = None
    user: str = None


EVENTS = {
    "unknown": SlackEvent,
    "hello": HelloEvent,
    "user_typing": UserTypingEvent,
    "message": MessageEvent
}
