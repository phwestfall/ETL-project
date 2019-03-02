# ETL-project

This project's purpose is to work with a partner to find multiple datasets or data sources and load them together for future analysis. We (Sarah & Paul) adiscovered a shared interest in understanding health patterns across the US, so this interest guided our search. 

## Load Mortality Data

We found data on Mortality Rates in the United States from CDC.gov: https://wonder.cdc.gov/controller/datarequest/D140 We decided to export this dataset based on:

* County code
* ICD Chapter (type of death)
* Death count
* Population of county
The data exported as a txt file. We read the txt file into pandas like it is a csv, using "\t" to indicate the tab delimited separations between the data cells.

## 