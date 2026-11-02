# From Plan to Practice: Simulating Schedule Overrides

Simulation code for my Bachelor End Project (1BEPIE, Industrial Engineering, TU/e):
*From Plan to Practice: Simulating Schedule Overrides and Task Completion for Automated Personal Scheduling*.

The end goal is a simulation that reads a planned calendar (iCalendar `.ics`), generates override events that depend on the user persona, notifications, task context and simulation parameters, updates the plan accordingly, and returns the calendar as it was actually executed.

## Current status

The current version (`src/simulation.py`):

1. Loads all events (`VEVENT`) from an `.ics` file: start, end, duration, status, all-day flag.
2. Generates Poisson arrivals (exponential inter-arrival times, default rate 0.4 per hour, seed 42) over the period from the first to the last calendar event. These arrivals are the triggers for future override events.
3. Calculates summary metrics: number of events, total/average/shortest/longest duration, simulation horizon, configured vs. observed arrival rate, and occupancy (event-hours / simulation-hours).
4. Exports everything to an Excel workbook with three sheets: **Metrics**, **Tasks** and **Arrivals**.

Not yet implemented: persona-dependent override logic, plan updating, and exporting the executed calendar.

For a full explanation of how the simulation works, see the **[manual](MANUAL.md)**.
For the target design of the full simulation loop, see the **[conceptual model](docs/CONCEPTUAL_MODEL.md)**.

## Installation

Requires Python 3.9+.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/simulation.py path/to/calendar.ics
```

Without an argument, the script uses the default path set in `DEFAULT_ICS_FILE` at the top of `simulation.py`.

The output `calendar_simulation_metrics.xlsx` is saved in the same folder as the `.ics` file.

Simulation parameters (arrival rate, random seed) are set in `main()`.

## Repository structure

```
.
├── src/
│   └── simulation.py     # Simulation: load calendar, generate arrivals, metrics, Excel export
├── data/                 # Put input .ics files here (not tracked by git)
├── docs/
│   ├── CONCEPTUAL_MODEL.md  # Target design: event-driven override loop
│   └── images/              # Original hand-drawn sketch
├── requirements.txt
├── MANUAL.md             # How the simulation works
└── README.md
```

## Author

Gijs van Berlo, Eindhoven University of Technology.
Supervisor: Maani Beigy. Second assessor: Yaoxin Wu.
