import os
from datetime import datetime


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

import copernicusmarine
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
import cartopy

from config import Config

class VectorMap:
    def __init__(self, config: Config):
        self.conf: Config = config
        self.Dataset_Dir: str = 'copernicus-data'
        self.Dataset_File: str ='test_data.nc'
        self.Dataset_Path: str = os.path.join(self.Dataset_Dir, self.Dataset_File)
        self.Dataset_Expiration: int = 60 # Days

        if not self.ValidDateset_p():
            self.FetchDataset()

        self.LoadDataset()

    def ValidDateset_p(self) -> bool:
        """
        Checks whether the specified file is a valid dataset.


        ---
        # Returns:
        - bool: True if file exists and was last updated in the last *self.Dataset_Expiration* days.
        """
        dataset_exists=0
        if os.path.exists(self.Dataset_Path):
            dataset_exists=1
            LastUpdated=self.conf.get("Dataset", "LastUpdated")
            LastUpdated=datetime.strptime(LastUpdated, '%Y-%m-%dT%H:%M:%S')
            Now=datetime.now()
            diff=Now-LastUpdated
            days=diff.days
        if dataset_exists == 0 or days > self.Dataset_Expiration:
            return False
        else:
            return True

    def FetchDataset(self) -> None:
        """
        Fetches a dataset and updates the conf file with current timestamp.

        ---
        # Returns:
        - None
        """
        if os.path.exists(self.Dataset_Path):
            os.remove(self.Dataset_Path)
        dataset_start=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
        dataset_end=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        copernicusmarine.subset(
            username="cjohnson4",
            password="Chri$7701",
            dataset_id="cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m",
            variables=["uo", "vo"],
            minimum_depth=0,
            maximum_depth=1,
            start_datetime=dataset_start,
            end_datetime=dataset_end,
            output_filename="test_data.nc",
            output_directory="copernicus-data"
            )
        self.conf.set("Dataset", "LastUpdated", datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        
            
    def LoadDataset(self) -> None:
        """
        Loads the dataset from the specified path and extract the surface velocity data.

        ---
        # Returns:
        - None
        """
        self.Data=xr.open_dataset(os.path.abspath(self.Dataset_Path))
        now=datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        # Selects the data for surface depth at the nearest available time to 'now'
        self.SurfaceData=self.Data.sel(time=now, depth=0, method='nearest')

        self.Surface_Velocity_East=self.SurfaceData.uo.values
        self.Surface_Velocity_North=self.SurfaceData.vo.values

        self.Surface_Vector_Intensity = np.sqrt(self.Surface_Velocity_East**2 + self.Surface_Velocity_North**2)

    def Plot(self, limits:tuple[float, float, float, float]=(-180.0,180.0,-90.0,90.0)) -> Figure:
        """
        This method creates a plot showing the intensity and direction of ocean currents using pcolormesh and quiver plots. The plot includes coastlines, borders, gridlines, and a color scale for current intensity.

        ---        
        # Returns:
        - None
        """

        # Plot Details
        self.plot_width=18 # Inches
        self.plot_height=8
        self.plot_scale_factor = 0.05 # This can change
        x_min=limits[0]
        x_max=limits[1]
        y_min=limits[2]
        y_max=limits[3]

        
        # Create a new figure with a cartopy projection
        fig,ax = plt.subplots(figsize=(self.plot_width, self.plot_height), subplot_kw={'projection': cartopy.crs.PlateCarree()})

        # Convert coordinates to a grid
        lon, lat = np.meshgrid(self.SurfaceData.longitude.values, self.SurfaceData.latitude.values)

        # Use pcolormesh to display current intensity as a background
        im = ax.pcolormesh(lon, lat, self.Surface_Vector_Intensity, shading='auto', cmap='Blues')

        # Adjust the length and width of the arrows based on intensity

        u_scaled = self.Surface_Velocity_East * self.plot_scale_factor
        v_scaled = self.Surface_Velocity_North * self.plot_scale_factor

        # Define a slice to skip drawing some "quiver" arrows to reduce clutter
        skip = (slice(None, None, 10), slice(None, None, 10))

        # Use the quiver function to display current vectors with their direction and intensity
        ax.quiver(lon[skip], lat[skip], u_scaled[skip], v_scaled[skip], color='black', scale=2, width=0.003, headwidth=4)

        # Draw coastlines, continents, and gridlines
        ax.coastlines()
        ax.add_feature(cartopy.feature.BORDERS, linestyle=":")
        ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='dotted')

        # Add a color scale for ocean current intensity
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1, shrink=0.6)
        cbar.set_label("Ocean Current Intensity [m/s]")
        print(f"ORIGINAL: {plt.xlim()}")
        print(f"ORIGINAL: {plt.ylim()}")

        # Scale the map to the selected coordinates
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        
        # Finish Up
        plt.title("Intensity and Direction of Currents off the African Coast")

        return fig

    def Show(self, limits: tuple[float, float, float, float]=(-180, 180, -90,90)) -> None:
        window=tk.Tk()
        frame=tk.Frame(master=window)
        fig=self.Plot(limits)
        plot=FigureCanvasTkAgg(fig, master=frame)
        frame.pack()
        plot.get_tk_widget().pack(expand=True, fill="both")
        # plt.show()
        window.mainloop()

if __name__ == "__main__":
    config=Config()
    test=VectorMap(config)
    # test.Show((-100, -50, 50, 70))
    coords=(-8597539.91030498, -6585298.74991039, 1162787.9276851565, 3175029.088079747)
    coords=[int(elem) for elem in coords]
    print(coords)
    test.Show(coords)
