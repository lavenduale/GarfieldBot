from GarfieldBot import GarfieldPlugin, MessageEvent

class TestPlugin(GarfieldPlugin):
    """
    A basic test plugin used to test various features of the bot as they are added.
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)

        self.bot.register_command("test", self.handle_command)

    def handle_command(self, event: MessageEvent, *args) -> None:
        self.bot.send_message(event.channel, ", ".join(args))
