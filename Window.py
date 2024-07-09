import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CoordinatePicker import CoordinatePicker
from VectorMap import VectorMap
from config import Config
import inspect

class MapWindow:
    def __init__(self, config: Config):
        self.master=tk.Tk()
        self.Picker=CoordinatePicker()
        self.Plot=self.Picker.Plot()
        self.V_Map=VectorMap(config)

        self.Canvas_Frame=tk.Frame(master=self.master)
        self.Coord_Canvas=FigureCanvasTkAgg(self.Plot, master=self.Canvas_Frame)
        self.Canvas_Button_Frame=tk.Frame(master=self.master)
        self.reset_button=tk.Button(self.Canvas_Button_Frame, text="Reset Zoom", command=self.Picker.ResetZoom)
        self.return_button=tk.Button(self.Canvas_Button_Frame, text="Get Coords.", command=self.GetCoords_Button_Event)

        self.Vector_Frame=tk.Frame(master=self.master)

        self.Vector_Button_Frame=tk.Frame(master=self.master)
        self.Coord_Button=tk.Button(self.Vector_Button_Frame, text="Choose New Coords.", command=self.ChooseCoord_Button_Event)

        self.DisplayCoordPicker()
        self.master.mainloop()

    def UpdateCoords(self, event):
        self.log("Updated Plot")
        self.Coord_Canvas.draw()

    def GetCoords(self) -> tuple[float, float, float, float]:
        Coords=self.Picker.extent
        return Coords

    def DisplayVectorMap(self, Coords: tuple[float, float, float, float]):
        self.Vector_Frame.pack(side="top")
        self.log(f"Coords: {Coords}")
        self.Vector_Canvas=FigureCanvasTkAgg(self.V_Map.Plot(Coords), master=self.Vector_Frame)

        self.Vector_Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.Vector_Button_Frame.pack(side="bottom", expand=True, fill="both")
        # self.Coord_Button.pack(expand=True, fill="both", padx=10, pady=10)
        
    def DisplayCoordPicker(self):
        self.Canvas_Frame.pack(side="top")

        self.Coord_Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.Picker.selector.connect_event('button_release_event', self.UpdateCoords)
        self.Canvas_Button_Frame.pack(side="bottom", expand=True, fill="both")
        self.reset_button.pack(side="left", expand=True, fill="both")
        self.return_button.pack(side="right", expand=True, fill="both")

    def ChooseCoord_Button_Event(self):
        for child in self.master.winfo_children():
            child.destroy()
        self.DisplayCoordPicker()
        self.UpdateCoords(None)

    def GetCoords_Button_Event(self):
        Coords=self.GetCoords()
        for child in self.master.winfo_children():
            child.pack_forget()
        self.DisplayVectorMap(Coords)

    def log(self,text:str):
        print(f" [LOG] -- {text}")
        
        
        
if __name__ == "__main__":
    test=MapWindow(Config())
        
