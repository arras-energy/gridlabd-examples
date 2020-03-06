# ELECTRIFICATION STUDY 

## Configuration 
To configure the model use file `config/simulation_configuration.csv`.
The types of variables defined in the file are: 
- Number of houses per phase (for a 3 phase circuit)
- Start time of the simulation
- Stop time of the simulation 
- Weather location
- The rest of the file defines the gas fraction: This is done by defining the name of the run and percent electrification (ie percent number of houses that have all electric appliances versus all gas appliances)

Appliances that can defined as gas are: Clothes Dryer, Waterheater, Heating, Stove/Range. If the house is defined to use gas as fuel, the model assumes all the aforementioned appliances are gas.

## Running the model 
To run the model: 
~~~
sh main.sh
~~~

## Output
The output from all the defined run in configuration will appear in `output/` folder.
