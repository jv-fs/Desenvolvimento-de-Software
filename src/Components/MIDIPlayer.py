import subprocess
import tempfile
import threading
import time
from pathlib import Path
from enum import Enum
from mido import MidiFile

class PlaybackState(Enum):
    STOPPED = 0
    PLAYING = 1


class MIDIPlayer:

    def __init__(self, midi_file: MidiFile):
        if not isinstance(midi_file, MidiFile):
            raise ValueError(
                "midi_file deve ser uma instância de mido.MidiFile"
            )

        self.midi_file = midi_file

        self.soundfont_path = (
            Path(__file__).parent.parent.parent
            / "soundfont"
            / "GeneralUser GS v1.472.sf2"
        )

        self.fluidsynth_path = (
            Path(__file__).parent.parent.parent
            / "fluidsynth"
            / "bin"
            / "fluidsynth.exe"
        )
        
        self.state = PlaybackState.STOPPED
        self.process = None
        self.loop_enabled = False
        self.loop_thread = None
        self.temp_midi_path = None

        self._validate_paths()
        self._create_temp_midi_file()

    def _validate_paths(self):
        if not self.fluidsynth_path.exists():
            raise FileNotFoundError(
                f"FluidSynth não encontrado: {self.fluidsynth_path}"
            )

        if not self.soundfont_path.exists():
            raise FileNotFoundError(
                f"SoundFont não encontrado: {self.soundfont_path}"
            )

    def _create_temp_midi_file(self):
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".mid",
            delete=False
        )

        self.temp_midi_path = Path(temp_file.name)

        self.midi_file.save(str(self.temp_midi_path))

        temp_file.close()

    def _build_command(self):
        return [
            str(self.fluidsynth_path),
            "-i",
            "-a", "dsound",
            "-g", "1.0",
            str(self.soundfont_path),
            str(self.temp_midi_path)
        ]

    def play(self, loop: bool = False):
        if self.state == PlaybackState.PLAYING:
            return

        self.loop_enabled = loop

        if loop:
            self.loop_thread = threading.Thread(target=self._loop_playback, daemon=True)
            self.loop_thread.start()
        else:
            self._start_process()

    def _start_process(self):
        command = self._build_command()

        self.process = subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        self.state = PlaybackState.PLAYING

    def _loop_playback(self):
        while self.loop_enabled:
            self._start_process()
            self.process.wait() #Bloqueia a thread até o processo terminar

            if not self.loop_enabled:
                break

            time.sleep(0.05)

        self.state = PlaybackState.STOPPED

    def stop(self):
        self.loop_enabled = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except Exception:
                pass

        self.process = None
        self.state = PlaybackState.STOPPED

    def restart(self):
        current_loop = self.loop_enabled

        self.stop()
        self.play(loop=current_loop)

    def is_playing(self) -> bool:
        if not self.process:
            return False

        return self.process.poll() is None

    def cleanup(self):
        self.stop()

        if self.temp_midi_path:
            try:
                self.temp_midi_path.unlink(missing_ok=True)
            except Exception:
                pass

    def __del__(self):
        self.cleanup()