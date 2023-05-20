# PhenologyGermany

The German National Meteorological Service (DWD) collects annual phenological data, i.e. the seasonal life cycles of plants. In phenology, a subset of these plants is used to mark the beginning of the seasons. For example, the blossoming of apple trees marks the beginning of 'full spring'.  

Here you may use this data to plot the changes of seasonal starting times in Germany from the 1950's up until now.

Below you find an example to create a plot. First import the moduls from src:
```python
from src.plots import * 
from src.core import *
from src.hypothesis_test import *

phenology = PhenologicalData()
```

To download all available data run:
```python
phenology.download_data()
```

Once it has been downloaded you can load it:
```python
phenology.load_data()
```

To make a Bar Plot run:
```python
mean = phenology.aggregate_data('mean')
make_horizontal_bar_plot(mean)
```

![alt text](https://github.com/kgeoffrey/GermanPhenology/blob/main/img/example.png "Bar Plot")

