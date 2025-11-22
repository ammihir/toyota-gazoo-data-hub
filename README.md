# toyota-gazoo-data-hub




To run -> python -m http.server 8000


RaceSim v1:

Gather Data:
Script: race_sim.ipynb - 
    JOIN endurance + telemetry data -> common.parquet
    
    Note: First join the data from endurance & telemetry to enrich the telemetry data.
    Endurance data doesnt have any records for cars -> 0, 16 and 78. Hence we will
    be discarding these from our application.

Data Processing
export_for_simulation.ipynb 

    Step 1
    Reads common.parquet -> fills missing data & writes -> common2.parquet

    Step 2:
    Reads common2.parquet -> (downsample if granular data) -> race_canvas.json 
    
Front End
Viewer2.html simulates the run

    Renders race_canvas.json to simulate the races at Barber circuit. 



RaceSim v2:
export_for_simulation_wind.ipynb - This script also takes into consideration the wind factor
to predict the target speed for the cars.
parquet = common3.parquet
race_canvas3.json
Viewer 3 is the html to simulate the run


