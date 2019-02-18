import time
import logging
from pprint import pformat

from slackclient import SlackClient
from jigsaw import PluginLoader

from .Plugin import GarfieldPlugin
from .Events import EVENTS


class Bot(object):
    """
    Main bot class that handles all incoming RTM events, and the making of API calls.
    """

    def __init__(self, token: str) -> None:
        """
        Initializes a new instance of GarfieldBot.

        :param token: The token to use to authenticate with Slack.
        """

        self.logger = logging.getLogger("GarfieldBot")

        self.logger.debug("Creating Slack client...")
        self.client = SlackClient(token)

        self._handlers = {}

        # Discover and load all plugins from the plugins directory
        self.logger.debug("Loading plugins...")
        self.loader = PluginLoader(plugin_class=GarfieldPlugin)
        self.loader.load_manifests()
        self.loader.load_plugins(self)
        self.loader.enable_all_plugins()

    def _parse_event(self, data: dict):
        """
        Parses an incoming event, dispatching it to all listening plugins.

        :param data: The data from the RTM client.
        """
        if data["type"] not in EVENTS:
            self.logger.warning(f"Unknown event type '{data['type']}'.\nData:\n{pformat(data)}")
            event_class = EVENTS["unknown"]
        else:
            event_class = EVENTS[data["type"]]
        if data["type"] in self._handlers:
            event_instance = event_class(data)
            for handler in self._handlers[data["type"]]:
                handler(event_instance)

    def start(self) -> None:
        """
        Starts this instance of GarfieldBot.
        """

        if self.client.rtm_connect():
            while self.client.server.connected:
                events = self.client.rtm_read()
                if events != []:
                    for event in events:
                        self._parse_event(event)

                time.sleep(0.5)
