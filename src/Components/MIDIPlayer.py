import subprocess
import threading
import time

from pathlib import Path
from enum import Enum

from mido import MidiFile


EXTRA_TIME_AFTER_MIDI_END = 0.1
TERMINATE_TIMEOUT = 1.0
NEXT_PLAY= 1


class PlaybackState(Enum):
    STOPPED = 0
    PLAYING = 1


class MIDIPlayer:

    def __init__(self):

        self.temp_midi_path = None

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

        self.playback_thread = None

        self.playback_id = 0

        self._validate_paths()

    ##################################################
    #                    Setup:
    ##################################################

    def _validate_paths(self):

        if not self.fluidsynth_path.exists():
            raise FileNotFoundError(
                f"FluidSynth não encontrado: {self.fluidsynth_path}"
            )

        if not self.soundfont_path.exists():
            raise FileNotFoundError(
                f"SoundFont não encontrado: {self.soundfont_path}"
            )

    ##################################################
    #               Playback control:
    ##################################################

    def play(self):

        if not self.temp_midi_path:
            raise RuntimeError("Nenhum MIDI carregado.")

        if self.is_playing():
            return

        self.playback_id += NEXT_PLAY

        current_playback_id = self.playback_id

        self.state = PlaybackState.PLAYING

        self.playback_thread = threading.Thread(
            target=self._playback_worker,
            args=(current_playback_id,),
            daemon=True
        )

        self.playback_thread.start()

    def stop(self):
        self.playback_id += NEXT_PLAY
        self.state = PlaybackState.STOPPED

        self._terminate_process()

    def restart(self):

        self.stop()
        self.play()

    ##################################################
    #                 Loop control:
    ##################################################

    def enable_loop(self):
        self.loop_enabled = True

    def disable_loop(self):
        self.loop_enabled = False

    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled

    def is_loop_enabled(self):
        return self.loop_enabled

    ##################################################
    #               Playback worker:
    ##################################################

    def _playback_worker(self, playback_id):

        while (
            self.state == PlaybackState.PLAYING
            and playback_id == self.playback_id
        ):

            self._start_process()

            duration = self._get_midi_duration()

            time.sleep(duration + EXTRA_TIME_AFTER_MIDI_END)

            if playback_id != self.playback_id:
                return

            self._terminate_process()

            if not self.loop_enabled:
                break

        if playback_id == self.playback_id:
            self.state = PlaybackState.STOPPED

    ##################################################
    #              Process management:
    ##################################################

    def _start_process(self):

        command = self._build_command()

        self.process = subprocess.Popen(
            command,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    def _terminate_process(self):

        if self.process and self.process.poll() is None:

            try:
                self.process.terminate()
                self.process.wait(timeout=TERMINATE_TIMEOUT)
            except Exception:
                pass

        self.process = None

    ##################################################
    #               MIDI information:
    ##################################################

    def _get_midi_duration(self):

        midi = MidiFile(self.temp_midi_path)
        return midi.length

    ##################################################
    #                Utility methods:
    ##################################################

    def _build_command(self):

        return [
            str(self.fluidsynth_path),
            "-i",
            "-a", "dsound",
            "-g", "1.0",
            str(self.soundfont_path),
            str(self.temp_midi_path)
        ]

    def is_playing(self) -> bool:

        if not self.process:
            return False

        return self.process.poll() is None

    def cleanup(self):

        self.stop()

    ##################################################
    #               Public setters:
    ##################################################

    def set_midi_temp(self, temp_midi_path: Path):

        temp_midi_path = Path(temp_midi_path)

        if not temp_midi_path.exists():
            raise FileNotFoundError(
                f"Arquivo MIDI temporário não encontrado: {temp_midi_path}"
            )

        self.temp_midi_path = temp_midi_path