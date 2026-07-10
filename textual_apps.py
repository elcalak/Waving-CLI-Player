from itertools import zip_longest
from pathlib import Path
from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import DataTable, Footer
from tinytag import TinyTag
import audio_controls as ac

class TableApp(App):
    
    def data_tables(self): #Start function to add default data to tables

        console = Console() #Create a object console to style prints and inputs
        console.clear() #Clear console with rich

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
      
            self.current_path = Path.home() / "Music"
      
        else:
      
            self.current_path = Path.home() / "Music" / str(folder)

        rows = self.build_new_colums(folder) #get rows
        table = self.query_one(DataTable) #Create a table object

        table.clear() #Limpia la tabla

        if not table.columns: #If the table dont have colums 

            #Add colums
            table.add_column(rows[0][0], key="tree")
            table.add_column(rows[0][1], key="title")
            table.add_column(rows[0][2], key="duration")
            table.add_column(rows[0][3], key="source")

        table.add_rows(rows[1:]) #Add rows

    #End function to update the tables

    def compose(self) -> ComposeResult: #Start function to compose App

        yield DataTable() #Call data table
        yield Footer() #Call Footer

    #End function to compose app

    def on_mount(self) -> None: #Start funtion to mount app

        table = self.query_one(DataTable) #Create a object table

        ROWS = self.data_tables()  #Call data_tables to get rows

        # Initialize current path for resolving file selections
        self.current_path = Path.home() / "Music"
        # single audio controller for the app (prevents overlapping instances)
        self.audio_control = ac.AudioControl()

        #Add colums
        table.add_column(ROWS[0][0], key="tree")
        table.add_column(ROWS[0][1], key="title")
        table.add_column(ROWS[0][2], key="duration")
        table.add_column(ROWS[0][3], key="source")

        table.add_rows(ROWS[1:]) #Add rows

    #End function to mount app

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None: #Start function to hear the selected cell

        table = self.query_one(DataTable) #Create a object table

        row_index = event.coordinate.row #Get the row index
        colum_index = event.coordinate.column #Get the colum index

        row_value = table.get_cell_at(event.coordinate) #Get the row value

        if colum_index == 0: #If the colum index is 0 or folder

            self.update_table(row_value) #Call Update table metoth with the folder selected

        elif colum_index == 1: #If the colum index is 1 or audio file

            row_str = str(row_value) #Convert row_value in string
            
            # resolve full path using current navigation folder
            base = getattr(self, "current_path", Path.home() / "Music")
            full_path = base / row_str #Get the full path

            if full_path.exists() and full_path.is_file(): #If path exist and is a file
                
                # use the single app-level audio controller so stop() works
                self.audio_control.play(str(full_path)) #play the audio
           
            else: #Else
           
                console = Console() #Create a console object
                console.print(f"[red]File not found:[/red] {full_path}") #Print error message

    #End of function to hear the selected cell

app = TableApp()

if __name__ == "__main__":


    app.run()