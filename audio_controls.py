"""

This file controls the audio files using miniaudio

Develovment by: Calak de Astora

"""

import threading #import threading to control the status
import time #Import time
import miniaudio as ma #Import miniaudio as ma to control audio and metadata

class AudioControl(): #Start AudioControl class

    """

    Control audio playback using a background thread and miniaudio.

    Supports playing, pausing, resuming, and stopping audio files while tracking
    playback progress and invoking a completion callback when a track finishes.

    """

    def __init__(self): #Start constructor

        """

        Initialize playback state and synchronization primitives.

        """

        self._thread = None #Create a thread
        self._stop_event = threading.Event() #Create stop event
        self._pause_event = threading.Event() #Create pause event
        self._device = None #Create device
        self._device_lock = threading.Lock() #Create lock device
        self._on_finished_callback = None #Create callback for when song finishes
        self._elapsed_time = 0 #Track elapsed time for pause/resume
        self._pause_time = 0 #Track when pause started

    #End of constructor

    def _play_thread(self, file: str): #Start play event

        """

        Run playback in a dedicated thread for the given audio file.

        Manages miniaudio device lifecycle, handles pause/resume state, and
        signals completion with the configured callback when playback ends.

        """

        info = ma.get_file_info(file) #Get info of the file
        stream = ma.stream_file(file) #Save the file to play

        try: #Start try play

            with ma.PlaybackDevice() as device: #With the function playback device as Device

                with self._device_lock: #Include device lock event

                    self._device = device #Device event is playback function

                device.start(stream) #Start the song

                # Wait until either the track duration elapses or stop is requested
                duration = info.duration or 0
                start = time.time()

                while not self._stop_event.is_set() and (time.time() - start + self._elapsed_time) < duration: #While not stop event is active and the song is end

                    if self._pause_event.is_set(): #If pause is requested

                        try:

                            device.stop() #Stop device while paused

                        except Exception:

                            pass

                        self._pause_time = time.time()

                        while self._pause_event.is_set() and not self._stop_event.is_set(): #While paused

                            time.sleep(0.1)

                        if not self._stop_event.is_set(): #If not stopped, resume

                            self._elapsed_time += time.time() - self._pause_time

                            try:

                                device.start(stream) #Restart playback

                            except Exception:

                                pass

                    time.sleep(0.1) #Sleep a moment

                try: #Start try to stop

                    device.stop() #Stop playing

                except Exception: #Except error

                    pass #Pass

                #End try to stop

                # Call the callback when song finishes (only if not manually stopped)
                if not self._stop_event.is_set() and self._on_finished_callback:
                    self._on_finished_callback()

        finally: #Finally

            with self._device_lock: #With the event device lock

                self._device = None #Unset device

        #End of try play

    #End of play event

    def play(self, file: str) -> None: #Start play function

        """

        Start playback of the specified audio file.

        Stops any currently playing track, resets pause state, and launches the
        playback thread for the new file.

        """

        # If already playing, stop current and start new
        if self._thread and self._thread.is_alive():

            self.stop() #Stop the music

        self._stop_event.clear() #Clear stop event
        self._pause_event.clear() #Clear pause event
        self._elapsed_time = 0 #Reset elapsed time
        #Use the event play
        self._thread = threading.Thread(target=self._play_thread, args=(file,), daemon=True)
        self._thread.start() #Start play

    #End of play function

    def stop(self) -> None: #Start stop function

        """

        Stop playback and wait for the playback thread to terminate.

        """

        if self._thread and self._thread.is_alive(): #If the events is play

            # signal the thread to stop
            self._stop_event.set()

            # attempt to stop the playback device directly for faster termination
            with self._device_lock:

                if self._device is not None: #If the device isnt none

                    try: #Start try to stop

                        self._device.stop() #Stop device

                    except Exception: #Except

                        pass #Pass the error

            # wait for thread to exit
            self._thread.join(timeout=3.0)

        self._thread = None #Event is none

    #End of stop function

    def pause(self) -> None: #Pause the audio

        """

        Pause the currently playing audio track.

        """

        self._pause_event.set() #Set pause event

    #End pause function

    def resume(self) -> None: #Resume the audio

        """
        
        Resume playback after a pause.
        
        """

        self._pause_event.clear() #Clear pause event

    #End resume function

    def set_finished_callback(self, callback): #Set callback for when song finishes

        """

        Register a callback to be invoked when playback finishes.

        """

        self._on_finished_callback = callback #Store the callback

    #End set callback

#End of AudioControl class
