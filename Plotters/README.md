#Plotters

Here are contained some of the plotteres we used to generate graphs for CoBiG² GBS and RAD data.
For now there is a SNP frequency plotter. More to come soon.

##freq_plotter.py
SNP frequency plotter. Requires Python 3, matplotlib and numpy.

Usage:

```
python3 freq_plotter frequencies_file.txt plot_type
```

Where plot type can be either "c" for cumulative graph or "f" for frequency graph.

###Warning:
The program is interactive - uses plt.show(), since I couldn't find a "one size fits all" setting for plt.savefig()

