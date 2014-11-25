#Plotters

Here are contained some of the plotteres we used to generate graphs for CoBiG² GBS and RAD data.
For now there is a SNP frequency plotter. More to come soon.

##freq_plotter.py
SNP frequency plotter. Requires Python 3, matplotlib and numpy.

Usage:

```
python3 freq_plotter frequencies_file.txt basename_for_plots
```

The basename for the plots needs a path too. It can be anything you like, but 2 files will be created: "your_prefix_freqs.png" and "your_prefix_cumul_freqs.png".
That means you don't need to specify an extension.
