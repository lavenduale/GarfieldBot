from GarfieldBot import GarfieldPlugin, MessageEvent

class TestPlugin(GarfieldPlugin):
    """
    A basic test plugin used to test various features of the bot as they are added.
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)

        self.bot.register_handler("message", self.handle_message)
    
    def handle_message(self, event: MessageEvent) -> None:
        if event.text.lower() == "ping":
            self.bot.send_message(event.channel, "Pong!")