import io #Import library of input output
from itertools import zip_longest #Import zip_longest from itertools to len many tuples at same time
from pathlib import Path #Import Path from pathlib to control files directories
from PIL import Image #Import image form Pillow
from rich_pixels import Pixels #Import Pixels from rich pixels to reduce an image
from textual.app import App, ComposeResult #Import app and compose result from textual.app to mount the app 
from textual.containers import Vertical, Horizontal #Import vertical and horizontal from textual.containers to stylice Menu
from textual.widgets import DataTable, Button, Footer #Import DataTable, button and footer from textual.widgets to use tables and buttons
from tinytag import TinyTag #Import TinyTag to get metadata
import audio_controls as ac #Import audio_controls file to control audio

class TableApp(App):
    
    def data_tables(self): #Start function to add default data to tables

        rows = [("Tree", "Title", "Duration", "Source")] #Initialize rows with header
        
        path = Path.home() / "Music" #Search the path "Music" in home

        if not path.exists(): #If the path dont exist

            path = Path.home() #Set path in home

            path.mkdir(parents=True, exist_ok=True) #Create the path

            print(f"Path created in: {path}") #Message to created path

        element = list(path.iterdir()) #Search in path

        audio_types = ['.mp3', '.wav', '.flac'] #Save the audio compatible types

        if not element: #If elements dont exist

            rows.append(("No folders found", "No files found", "", "")) #Print message error

        else: #Else

            folders = [] #List to store folder names
            audio_files = [] #List to store audio file name
            durations = [] #List to store durations of audio files
            sources = [] #List to store sources of files

            for item in element: #Start to search the elements

                if item.is_dir(): #If the element is a directory

                    folders.append(item.name) #Add folder to list

                elif item.is_file() and item.suffix.lower() in audio_types: #If element is a file and is compatible with audio_types

                    tag = TinyTag.get(item) #Create a object tag to get tags form element
                    duration_seconds = tag.duration or 0 #Save the duration
                    minutes = int(duration_seconds // 60) #Get the minutes
                    seconds = int(duration_seconds % 60) #Get the seconds
                    duration_str = f"{minutes:02d}:{seconds:02d}" #Make the duration format

                    audio_files.append(item.name) #Add file to list
                    durations.append(duration_str) #Add duration to list
                    sources.append("local") #Add sources to list

            #Add folders, audio files, durations, sources to rows
            rows = list(zip_longest(folders, audio_files, durations, sources, fillvalue=""))
        
        rows.insert(0, ("Tree", "Title", "Duration", "Source"))  #Add header in position 0

        return rows #Return rows to use in on_mount

    #End of function to add default data to tables

    def build_new_colums(self, folder): #Start function to build new colums

        audio_types = ['.mp3', '.wav', '.flac'] #Save the audio compatible types

        folders = [] #List to store folder names
        audio_files = [] #List to store audio file name
        durations = [] #List to store durations of audio files
        sources = [] #List to store sources of files

        if folder == "Back...": #If folder is Back option

            path = Path.home() / "Music" #Path is home

        else: #Else

            path = Path.home() / "Music" / folder #Create the new path
            folders.append("Back...") #Add back option to list

        element = list(path.iterdir()) #Search in path

        if not element: #If elements dont exist

            rows.append(("No folders found", "No files found", "", "")) #Print message error

        else: #Else

            for item in element: #Start to search the elements

                if item.is_dir(): #If the element is a directory

                    folders.append(item.name) #Add folder to list

                elif item.is_file() and item.suffix.lower() in audio_types: #If element is a file and is compatible with audio_types

                    tag = TinyTag.get(item) #Create a object tag to get tags form element
                    duration_seconds = tag.duration or 0 #Save the duration
                    minutes = int(duration_seconds // 60) #Get the minutes
                    seconds = int(duration_seconds % 60) #Get the seconds
                    duration_str = f"{minutes:02d}:{seconds:02d}" #Make the duration format

                    audio_files.append(item.name) #Add file to list
                    durations.append(duration_str) #Add duration to list
                    sources.append("local") #Add sources to list

            #Add folders, audio files, durations, sources to rows
            rows = list(zip_longest(folders, audio_files, durations, sources, fillvalue=""))
        
        rows.insert(0, ("Tree", "Title", "Duration", "Source"))  #Add header in position 0

        return rows #Return rows to use in update_table

    #End of function to build new colums

    def update_table(self, folder): #Start function to update the tables
        
        # keep track of current navigation folder
        if folder == "Back...":
      
            self.current_path = Path.home() / "Music" #Set home path
      
        else: #Else
      
            self.current_path = Path.home() / "Music" / str(folder) #Set new path

        rows = self.build_new_colums(folder) #get rows
        table = self.query_one("#main_menu_table", DataTable) #Create a table object

        table.clear() #Clear the table

        if not table.columns: #If the table dont have colums 

            #Add colums
            table.add_column(rows[0][0], key="tree")
            table.add_column(rows[0][1], key="title")
            table.add_column(rows[0][2], key="duration")
            table.add_column(rows[0][3], key="source")

        table.add_rows(rows[1:]) #Add rows

    #End function to update the tables

    def player_table_fill(self, folder, name): #Start funtcion to fill player menu

        table = self.query_one("#player_menu_table", DataTable) #Create a table object
        image_file = None #Create a image file container

        table.clear() #Clear the table

        # folder is the full path to the file, name is the filename
        # Use TinyTag to get the duration and format it as MM:SS
        try:

            tag = TinyTag.get(folder, image = True) #Create a tag object
            image_file = tag.get_image() #Get the image
            duration_seconds = tag.duration or 0 #Get the duration in sectonds

        except Exception: #Error

            duration_seconds = 0 #Return 0 seconds

        minutes = int(duration_seconds // 60) #Get minutes
        seconds = int(duration_seconds % 60) #Get seconds
        duration_str = f"{minutes:02d}:{seconds:02d}" #Build the format

        if image_file: #If image exist

            img_pil = Image.open(io.BytesIO(image_file)) #Open the image

            img_pil = img_pil.resize((50, 50)) #Resize the image

            render = Pixels.from_image(img_pil) #Render the image
        
        else: #Else
            
            render = "🎵" #Render show "🎵"

        row = (render, name, duration_str) #Build the rows

        if not table.columns: #If the table dont have colums 

            #Add colums to player menu
            table.add_column("Image")
            table.add_column("Name")
            table.add_column("Duration")

        # add a single row (as an iterable of rows)
        table.add_rows([row]) #Add rows

    #End of function to fill player menu

    def compose(self) -> ComposeResult: #Start function to compose App

        with Vertical(): #Put the tables in vertical

            yield DataTable(id = "main_menu_table") #Call data table to main menu table
            yield DataTable(id = "player_menu_table") #Call data table to player menu

            with Horizontal(): #Put the buttons in horizontal in a vertical container

                yield Button("⏮", id = "prev_button") #Call button to previus
                yield Button("⏸", id = "pause_button") #Call button to pause
                yield Button("▶", id = "play_button") #Call button to play
                yield Button("⏭", id = "next_button") #Call button to next
                yield Button("Clear Playlist", id = "clear") #Call button to clear

        yield Footer() #Call Footer

    #End function to compose app

    def on_mount(self) -> None: #Start funtion to mount app

        table = self.query_one("#main_menu_table", DataTable) #Create a object table
        table_2 = self.query_one("#player_menu_table", DataTable) #Create a second object table

        for button in self.query(Button): #Start loop to set any buttons

            button.styles.border = ("round", "white") #Put the border round and white
            button.styles.width = 7 #Put the width in 7 for seem a circle
            button.styles.height = 3 #Put height in 3 for seem a circle
            button.styles.background = "transparent" #Put transparent background

            button.styles.display = "none" #Hide the buttons

        table_2.styles.display = 'none' #Hides the second table

        ROWS = self.data_tables()  #Call data_tables to get rows

        # Initialize current path for resolving file selections
        self.current_path = Path.home() / "Music"
        # single audio controller for the app (prevents overlapping instances)
        self.audio_control = ac.AudioControl()
        # Set up the callback for when a song finishes
        self.audio_control.set_finished_callback(self._on_song_finished)
        # Initialize playlist and tracking
        self.playlist = []  #Playlist to store songs
        self.current_index = -1  #Index of current song
        self.is_paused = False  #Track if currently paused

        #Add colums to main menu table
        table.add_column(ROWS[0][0], key="tree")
        table.add_column(ROWS[0][1], key="title")
        table.add_column(ROWS[0][2], key="duration")
        table.add_column(ROWS[0][3], key="source")

        table.add_rows(ROWS[1:]) #Add rows

        #Add colums to player menu
        table_2.add_column("Image")
        table_2.add_column("Name")
        table_2.add_column("Duration")

    #End function to mount app

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None: #Start function to hear the selected cell

        table = self.query_one("#main_menu_table", DataTable) #Create a object table

        row_index = event.coordinate.row #Get the row index
        colum_index = event.coordinate.column #Get the colum index

        row_value = table.get_cell_at(event.coordinate) #Get the row value

        if colum_index == 0 and row_value != "No folders found": #If the colum index is 0 or folder

            self.update_table(row_value) #Call Update table metoth with the folder selected

        elif colum_index == 1 and row_value != "No files found": #If the colum index is 1 or audio file

            row_str = str(row_value) #Convert row_value in string
            
            # resolve full path using current navigation folder
            base = getattr(self, "current_path", Path.home() / "Music")
            full_path = base / row_str #Get the full path

            if full_path.exists() and full_path.is_file(): #If path exist and is a file

                # Add song to playlist if not already there
                full_path_str = str(full_path)

                if self.playlist == [] and full_path_str not in self.playlist: #If playlist is empty

                    player_table = self.query_one("#player_menu_table", DataTable) #Create a object table for the player

                    self.player_table_fill(str(full_path), row_str) #Fill the table

                    player_table.styles.display = 'block' #Show the player menu table                

                    self.query_one("#pause_button").styles.display = 'block' #Show the pause button
                    self.query_one("#next_button").styles.display = 'block' #Show the next button
                    self.query_one("#prev_button").styles.display = 'block' #Show the previuos button
                    self.query_one("#clear").styles.display = 'block' #Show clear button

                    self.playlist.append(full_path_str) #Add the song to the playlist

                    self.current_index = self.playlist.index(full_path_str) #Set current index
                    self.audio_control.play(full_path_str) #play the audio

                elif full_path_str not in self.playlist: #If the file isnt in the playlist

                    self.playlist.append(full_path_str) #Add to playlist

            else: #Else
           
                self.notify("Error to load") #Error notify

    #End of function to hear the selected cell

    def on_button_pressed(self, event: Button.Pressed) -> None: #Start press button event

        if event.button.id == "pause_button": #If the pause button was presing

            self.query_one("#pause_button").styles.display = "none" #Hide the buttons
            self.query_one("#play_button").styles.display = 'block' #Show the play button
            self.audio_control.pause() #Pause the audio
            self.is_paused = True #Mark as paused
        
        elif event.button.id == "play_button": #If the play button was presing

            self.query_one("#play_button").styles.display = "none" #Hide the buttons
            self.query_one("#pause_button").styles.display = 'block' #Show the pause button

            if self.is_paused: #If currently paused, resume

                self.audio_control.resume() #Resume from pause

            else: #If not paused, play from start

                if self.playlist and self.current_index >= 0: #If the playlist and the current index isnt 0

                    self.audio_control.play(self.playlist[self.current_index]) #Play from resume

            self.is_paused = False #Mark as not paused

        elif event.button.id == "next_button": #If the next button was presing

            self._play_next() #Play next song

        elif event.button.id == "prev_button": #If the prev button was presing

            self._play_previous() #Play previous song

        elif event.button.id == "clear": #If the clear button was presing

            self.playlist = [] #Clear playlist
            table = self.query_one("#player_menu_table", DataTable) #Create a object table

            if not self.is_paused: #If is audio playing

                self.audio_control.stop() #Stop the audio

            for button in self.query(Button): #Start loop to set any buttons

                button.styles.display = "none" #Hide the buttons

            self.player_table_fill("", "") #Delete player table
            table.styles.display = 'none' #Hides the second table

    #End press button event

    def _play_next(self) -> None: #Start play next song in playlist

        if not self.playlist: #If the playlist is empty

            self.notify("Playlist is empty") #Notify the playlist empty

            return #Return

        #Else
        self.current_index += 1 #Pass the next index

        if self.current_index >= len(self.playlist): #If the index is the final

            self.current_index = 0  #Loop to start

        self.is_paused = False #Reset paused state
        self._play_current_song() #Play the current index

    #End play next song event

    def _play_previous(self) -> None: #Play play previous song in playlist

        if not self.playlist: #If the playlist is empty

            self.notify("Playlist is empty") #Notify error

            return #Return

        self.current_index -= 1 #Get previus index
        
        if self.current_index < 0: #If the playlist index is 0

            self.current_index = len(self.playlist) - 1  #Loop to end
        
        self.is_paused = False #Reset paused state
        self._play_current_song() #Play the current index

    #End play previuos song event

    def _play_current_song(self) -> None: #Play the current song
        
        if 0 <= self.current_index < len(self.playlist): #If the index is minus of 0

            song_path = self.playlist[self.current_index] #Get the path
            filename = Path(song_path).name #Get file name
            
            self.player_table_fill(song_path, filename) #Update the player table menu
            self.audio_control.play(song_path) #Play current path
            
            self.query_one("#pause_button").styles.display = 'block' #Show pause button
            self.query_one("#play_button").styles.display = 'none' #Hide play button
            self.query_one("#player_menu_table").styles.display = 'block' #Show the player table menu

    #End play current song event

    def _on_song_finished(self) -> None: #Called when song finishes
        
        # Use call_later to schedule this on the main thread (callback is from audio thread)
        self.call_later(self._play_next)

    #End next call finish event

#End of TableApp class