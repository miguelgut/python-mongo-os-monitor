## Classe de plotagem de gráficos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import pandas as pd

from datetime import datetime
from database import Mongo

class Graphs(object):
    
    def generateTable(self, tableData):
        print(pd.DataFrame(tableData))

    def generatePlot(self, plotData):      
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        years_fmt = mdates.DateFormatter('%Y')
        
        # with cbook.get_sample_data('goog.npz') as datafile:
        #    plotData = np.load(datafile)['price_data']
        # print(plotData)
        fig, ax = plt.subplots()
        ax.plot('date', 'adj_close', data=plotData)

        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

        
        datemin = np.datetime64(plotData['date'][0], 'Y')
        datemax = np.datetime64(plotData['date'][-1], 'Y') + np.timedelta64(1, 'Y')
        ax.set_xlim(datemin, datemax)

        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
        ax.grid(True)

        fig.autofmt_xdate()
        plt.show()

#Graphs.generatePlot({},{})