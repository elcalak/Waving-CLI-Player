import miniaudio as ma
import threading
import time

class AudioControl(): #Start AudioControl class

    def __init__(self): #Start constructor

        self._thread = None #Create a thread
        self._stop_event = threading.Event() #Create stop event
        self._device = None #Create device
        self._device_lock = threading.Lock() #Create lock device

    #End of constructor

    def _play_thread(self, file: str): #Start play event

        info = ma.get_file_info(file) #Get info of the file
        print(f"Playing: {info.nchannels} channels, {info.sample_rate} Hz, {info.duration:.1f}s") #Print info

        stream = ma.stream_file(file) #Save the file to play

        try: #Start try play

            with ma.PlaybackDevice() as device: #With the function playback device as Device

                with self._device_lock: #Include device lock event

                    self._device = device #Device event is playback function

                device.start(stream) #Start the song

                # Wait until either the track duration elapses or stop is requested
                duration = info.duration or 0
                start = time.time()

                while not self._stop_event.is_set() and (time.time() - start) < duration: #While not stop event is active and the song is end

                    time.sleep(0.1) #Sleep a moment

                try: #Start try to stop

                    device.stop() #Stop playing

                except Exception: #Except error

                    pass #Pass

                #End try to stop

        finally: #Finally

            with self._device_lock: #With the event device lock

                self._device = None #Unset device

        #End of try play

    #End of play event

    def play(self, file: str) -> None: #Start play function
        
        # If already playing, stop current and start new
        
        if self._thread and self._thread.is_alive():
        
            self.stop() #Stop the music

        self._stop_event.clear() #Clear stop event
        self._thread = threading.Thread(target=self._play_thread, args=(file,), daemon=True) #Use the event play
        self._thread.start() #Start play

    #End of play function

    def stop(self) -> None: #Start stop function
        
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