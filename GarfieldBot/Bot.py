import time
import logging
import threading
from typing import Callable
from pprint import pformat

from slackclient import SlackClient
from jigsaw import PluginLoader

from .Plugin import GarfieldPlugin
from .DataClasses import EVENTS, SlackEvent, HelloEvent


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

        self.register_handler("hello", self._handle_hello)

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
                threading.Thread(
                    target=handler,
                    args=(event_instance, )
                ).start()

    def _handle_hello(self, event: HelloEvent) -> None:
        """
        Handles an incoming hello event, logging that the bot has successfully connected.

        :param event: The event instance.
        """
        self.logger.info("GarfieldBot successfully connected to Slack.")

    def register_handler(self, type: str, handler: Callable[[SlackEvent], None]) -> None:
        """
        Registers a handler for a certain event.

        :param type: The type of event to handle.
        :param handler: The function to be used to handle the event.
        """
        if type not in self._handlers:
            self._handlers[type] = [handler]
        else:
            self._handlers[type].append(handler)

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
