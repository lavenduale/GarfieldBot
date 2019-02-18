from typing import Dict, List, Union, Optional


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


class User(SlackDataClass):
    """
    Represents a Slack user.
    """
    id: str = None
    team_id: str = None
    name: str = None
    deleted: bool = None
    color: str = None
    real_name: str = None
    tz: str = None
    tz_label: str = None
    tz_offset: int = None
    profile: Dict[str, str] = None
    is_admin: bool = None
    is_owner: bool = None
    is_primary_owner: bool = None
    is_restricted: bool = None
    is_ultra_restricted: bool = None
    is_bot: bool = None
    updated: int = None
    is_app_user: bool = None
    has_2fa: bool = None


class Channel(SlackDataClass):
    """
    Represents a Slack channel.
    """
    id: str = None
    name: str = None
    is_channel: bool = None
    is_group: bool = None
    is_im: bool = None
    created: int = None
    creator: str = None
    is_archived: bool = None
    is_general: bool = None
    unlinked: int = None
    name_normalized: str = None
    is_read_only: bool = None
    is_shared: bool = None
    parent_conversation: Optional[str] = None
    is_ext_shared: bool = None
    is_org_shared: bool = None
    pending_shared: List[str] = None
    is_pending_ext_shared: bool = None
    is_member: bool = None
    is_private: bool = None
    is_mpim: bool = None
    last_read: str = None
    topic: Dict[str, Union[str, int]] = None
    purpose: Dict[str, Union[str, int]] = None
    previous_names: List[str] = None
    locale: str = None


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
    text: str = None


EVENTS = {
    "unknown": SlackEvent,
    "hello": HelloEvent,
    "user_typing": UserTypingEvent,
    "message": MessageEvent
}
