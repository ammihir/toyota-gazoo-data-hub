# toyota-gazoo-data-hub






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




STEPS TO RUN APPLICATION
To run -> python -m http.server 8000


RaceSim v1:

Gather Data:
Run race_sim.ipynb 

    JOIN endurance + telemetry data -> common.parquet
    
    Note: First join the data from endurance & telemetry to enrich the telemetry data.
    Endurance data doesnt have any records for cars -> 0, 16 and 78. Hence we will
    be discarding these from our application.

Data Processing
Run export_for_simulation.ipynb 

    Step 1
    Reads common.parquet -> fills missing data & writes -> common2.parquet

    Step 2:
    Reads common2.parquet -> (downsample if granular data) -> race_canvas.json 
    
Front End
Viewer2.html simulates the run

    Renders race_canvas.json to simulate the races at Barber circuit. 


STEPS FOR RUNNING APPLICATION

    Run the app -> python -m http.server 8000

    Open link: http://localhost:8000/viewer2.html 