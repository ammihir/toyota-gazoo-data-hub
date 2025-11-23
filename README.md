

<p align="center">
<img src="assets/logo-small.png" width="550" />
</p>


<h1 align="center">RaceSim v1</h1>

<p align="center" style="font-size:16px;">
  RaceSim is a telemetry-driven racing visualization tool that joins endurance + telemetry datasets, processes them for consistency, and renders a full lap-by-lap replay of cars around the Barber Motorsports Park circuit.
</p>




📦 **Data Preparation Pipeline**

    Step 1 - Package data for efficient processing
    Notebook: race_sim_prerequisites.ipynb

    Step 2 - Gather & Join Data (enriches telemetry with endurance metadata)
    Notebook: race_sim.ipynb
    JOIN endurance + telemetry data → produces common.parquet

*Note: Endurance data has no records for car IDs 0, 16, 78, so these cars are excluded from RaceSim*

⚙️ **Data Processing**

    Step 1 - Fill & Clean
    Notebook: export_for_simulation.ipynb
    Reads common.parquet → fills missing values → writes common2.parquet

    Step 2 - Export for Viewer
    Reads common2.parquet → optionally down-samples if telemetry is too granular → outputs race_canvas.json

*race_canvas JSON is consumed by the RaceSim front-end to simulate the race.*

🎥 **Front-End Race Simulator**

    File: viewer2.html

    Simulates the race by rendering race_canvas.json onto a high-performance canvas, visualizing 
    - car motion
    - lap progression 
    - live metrics
    - multi-car comparison

🚀 How to Run the Application

    From the root (the folder that contains `viewer2.html`):
    python -m http.server 8000

    Then open:
    http://localhost:8000/viewer2.html

*Car Selection*
*Use Ctrl + Click to select multiple cars in the viewer.*