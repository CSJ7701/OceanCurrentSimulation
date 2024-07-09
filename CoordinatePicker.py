import matplotlib
from matplotlib import transforms
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button
import matplotlib.patches as patches
from decimal import Decimal

class CoordinatePicker:
        
    def Plot(self):
        self.fig=plt.figure(figsize=(20,10))
        self.ax=self.fig.add_subplot(1,1,1,projection=ccrs.Robinson())

        self.ax.set_global()
        self.ax.stock_img()
        self.ax.coastlines()

        self.rectangle_window=None

        self.selector=RectangleSelector(self.ax, self.HandleSelection, button=[1])

        return self.fig

    def HandleSelection(self, eclick, erelease):
        if not self.selector.extents[0]==self.selector.extents[1] or self.selector.extents[2]==self.selector.extents[3]:
            # self.extent=self.selector.extents
            x1=Decimal(self.selector.extents[0])
            x2=Decimal(self.selector.extents[1])
            y1=Decimal(self.selector.extents[2])
            y2=Decimal(self.selector.extents[3])
            self.extent=self.selector.extents
        if abs(x1 - x2) > 99999 and abs(y1 - y2) > 99999:
            plt.xlim(self.extent[0]+200, self.extent[1]+200)
            plt.ylim(self.extent[2]+200, self.extent[3]+200)
        else:

            print("Too Small")

            if self.rectangle_window:
                self.rectangle_window.remove()

            delta_x=(self.extent[0]-self.extent[1])/2
            delta_y=(self.extent[2]-self.extent[3])/2

            plt.xlim(delta_x - 50000, delta_x + 50000)
            plt.ylim(delta_y - 50000, delta_y + 50000)


            rect=patches.Rectangle((x1,y1), x2-x1, y2-y1, linewidth=1, edgecolor='r')
            self.rectangle_window=self.ax.add_patch(rect)
            
        print(self.extent)

    def ResetZoom(self):
        self.ax.set_global()
        plt.draw()

    def Show(self):
        plt.show()

if __name__ == "__main__":
    test=CoordinatePicker()
