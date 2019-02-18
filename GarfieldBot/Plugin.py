from jigsaw import JigsawPlugin


class GarfieldPlugin(JigsawPlugin):
    """
    Represents a plugin for GarfieldBot, dynamically loaded and instantiated by jigsaw.
    """

    def __init__(self, manifest, bot) -> None:
        """
        Instantiates a loaded plugin.

        :param manifest: The jigsaw plugin manifest for this plugin.
        :param bot: The GarfieldBot instance that loaded this plugin.
        """
        super().__init__(manifest)
        self.bot = bot
