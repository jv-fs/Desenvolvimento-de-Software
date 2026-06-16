class ActionsController:

    def __init__(
        self,
        playback,
        text,
        compilation,
        export,
        instrument
    ):
        self.playback = playback
        self.text = text
        self.compilation = compilation
        self.export = export
        self.instrument = instrument