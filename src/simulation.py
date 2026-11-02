import sys
import random
import math
from pathlib import Path
from datetime import datetime, date, timedelta

from icalendar import Calendar
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ============================================================
# 1. FILE PATHS
# ============================================================

# Usage: python src/simulation.py [path/to/calendar.ics]
# Without an argument, the default calendar below is used.
DEFAULT_ICS_FILE = Path(
    r"C:\Users\20234396\OneDrive - TU Eindhoven\Industrial Engineering Year 4\BEP\Internal BEP Assignment\Icalendars\diligent_anxious_active_0000.ics"
)

ICS_FILE = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ICS_FILE

# Save the Excel file in the SAME folder as the ICS file
output_file = ICS_FILE.parent / "calendar_simulation_metrics.xlsx"


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def normalize_datetime(value):
    """Convert an ICS date or datetime into a Python datetime."""
    if isinstance(value, datetime):
        # Convert timezone-aware values to the computer's local time,
        # then remove timezone information for consistent calculations.
        if value.tzinfo is not None:
            value = value.astimezone().replace(tzinfo=None)
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    return None


def get_duration_hours(event):
    """Calculate event duration in hours."""
    start_raw = event.get("DTSTART")
    if start_raw is None:
        return None

    start = normalize_datetime(start_raw.dt)

    end_raw = event.get("DTEND")
    duration_raw = event.get("DURATION")

    if end_raw is not None:
        end = normalize_datetime(end_raw.dt)
        return max(0, (end - start).total_seconds() / 3600)

    if duration_raw is not None:
        return max(0, duration_raw.dt.total_seconds() / 3600)

    return None


# ============================================================
# 3. LOAD CALENDAR
# ============================================================

def load_calendar(file_path):
    """Read calendar events from an ICS file."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Calendar file not found:\n{file_path}\n\n"
            "Check that the filename and folder are correct."
        )

    with file_path.open("rb") as file:
        calendar = Calendar.from_ical(file.read())

    tasks = []

    for event in calendar.walk("VEVENT"):
        start_raw = event.get("DTSTART")
        if start_raw is None:
            continue

        start = normalize_datetime(start_raw.dt)

        end_raw = event.get("DTEND")
        duration_raw = event.get("DURATION")

        if end_raw is not None:
            end = normalize_datetime(end_raw.dt)
            duration_hours = max(
                0, (end - start).total_seconds() / 3600
            )
        elif duration_raw is not None:
            duration_hours = max(
                0, duration_raw.dt.total_seconds() / 3600
            )
            end = start + timedelta(hours=duration_hours)
        else:
            end = None
            duration_hours = None

        tasks.append({
            "uid": str(event.get("UID", "")),
            "summary": str(event.get("SUMMARY", "Untitled event")),
            "start": start,
            "end": end,
            "duration_hours": duration_hours,
            "status": str(event.get("STATUS", "")),
            "all_day": isinstance(start_raw.dt, date)
                        and not isinstance(start_raw.dt, datetime),
        })

    tasks.sort(key=lambda task: task["start"])
    return tasks


# ============================================================
# 4. GENERATE POISSON ARRIVALS
# ============================================================

def generate_triggers(tasks, rate_per_hour=0.4, seed=42):
    """
    Generate Poisson arrivals over the period from the earliest
    calendar event to the latest calendar event.

    rate_per_hour = expected number of arrivals per hour.
    """
    if rate_per_hour <= 0:
        raise ValueError("rate_per_hour must be greater than zero.")

    valid_starts = [task["start"] for task in tasks if task["start"]]
    valid_ends = [task["end"] for task in tasks if task["end"]]

    if not valid_starts or not valid_ends:
        return [], None, None

    simulation_start = min(valid_starts)
    simulation_end = max(valid_ends)

    if simulation_end <= simulation_start:
        return [], simulation_start, simulation_end

    random.seed(seed)

    triggers = []
    current_time = simulation_start

    while True:
        # Exponential inter-arrival time for a Poisson process
        interarrival_hours = random.expovariate(rate_per_hour)
        current_time += timedelta(hours=interarrival_hours)

        if current_time >= simulation_end:
            break

        triggers.append({
            "time": current_time,
            "type": "POISSON_ARRIVAL",
            "summary": "Calendar-wide arrival",
        })

    return triggers, simulation_start, simulation_end


# ============================================================
# 5. CALCULATE METRICS
# ============================================================

def calculate_metrics(tasks, triggers, simulation_start,
                      simulation_end, rate_per_hour):
    """Calculate summary metrics for the calendar and simulation."""

    durations = [
        task["duration_hours"]
        for task in tasks
        if task["duration_hours"] is not None
    ]

    total_task_hours = sum(durations)
    number_of_events = len(tasks)
    events_with_duration = len(durations)

    if simulation_start and simulation_end:
        simulation_hours = max(
            0, (simulation_end - simulation_start).total_seconds() / 3600
        )
    else:
        simulation_hours = 0

    observed_rate = (
        len(triggers) / simulation_hours
        if simulation_hours > 0 else 0
    )

    average_interarrival = (
        simulation_hours / len(triggers)
        if triggers else None
    )

    average_duration = (
        total_task_hours / events_with_duration
        if events_with_duration else None
    )

    shortest_task = min(
        (task for task in tasks
         if task["duration_hours"] is not None),
        key=lambda task: task["duration_hours"],
        default=None,
    )

    longest_task = max(
        (task for task in tasks
         if task["duration_hours"] is not None),
        key=lambda task: task["duration_hours"],
        default=None,
    )

    occupancy_ratio = (
        total_task_hours / simulation_hours
        if simulation_hours > 0 else None
    )

    metrics = [
        ("Total calendar events", number_of_events),
        ("Events with known duration", events_with_duration),
        ("Total event duration (hours)", total_task_hours),
        ("Total event duration (days)", total_task_hours / 24),
        ("Average event duration (hours)", average_duration),
        (
            "Shortest event",
            shortest_task["summary"] if shortest_task else None,
        ),
        (
            "Shortest event duration (hours)",
            shortest_task["duration_hours"] if shortest_task else None,
        ),
        (
            "Longest event",
            longest_task["summary"] if longest_task else None,
        ),
        (
            "Longest event duration (hours)",
            longest_task["duration_hours"] if longest_task else None,
        ),
        ("Simulation start", simulation_start),
        ("Simulation end", simulation_end),
        ("Simulation duration (hours)", simulation_hours),
        ("Simulation duration (days)", simulation_hours / 24),
        ("Configured arrival rate (per hour)", rate_per_hour),
        ("Number of Poisson arrivals", len(triggers)),
        ("Observed arrival rate (per hour)", observed_rate),
        ("Average time between arrivals (hours)", average_interarrival),
        ("Total event-hours / simulation-hours", occupancy_ratio),
    ]

    return metrics


# ============================================================
# 6. EXPORT TO EXCEL
# ============================================================

def export_to_excel(tasks, triggers, metrics, output_path):
    """Create an Excel workbook with Metrics, Tasks and Arrivals sheets."""

    workbook = Workbook()

    # ---- Metrics sheet ----
    ws_metrics = workbook.active
    ws_metrics.title = "Metrics"
    ws_metrics.append(["Metric", "Value"])

    for metric, value in metrics:
        ws_metrics.append([metric, value])

    # ---- Tasks sheet ----
    ws_tasks = workbook.create_sheet("Tasks")
    ws_tasks.append([
        "UID",
        "Summary",
        "Start",
        "End",
        "Duration (hours)",
        "Status",
        "All-day event",
    ])

    for task in tasks:
        ws_tasks.append([
            task["uid"],
            task["summary"],
            task["start"],
            task["end"],
            task["duration_hours"],
            task["status"],
            task["all_day"],
        ])

    # ---- Arrivals sheet ----
    ws_arrivals = workbook.create_sheet("Arrivals")
    ws_arrivals.append([
        "Arrival number",
        "Arrival time",
        "Arrival type",
        "Description",
    ])

    for index, trigger in enumerate(triggers, start=1):
        ws_arrivals.append([
            index,
            trigger["time"],
            trigger["type"],
            trigger["summary"],
        ])

    # ---- Format all sheets ----
    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78",
    )

    for worksheet in workbook.worksheets:
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = header_fill
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )

        # Adjust column widths to fit content
        for column_cells in worksheet.columns:
            max_length = 0
            column_letter = get_column_letter(column_cells[0].column)

            for cell in column_cells:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value)),
                    )

            worksheet.column_dimensions[column_letter].width = min(
                max_length + 2, 45
            )

    # Format datetime columns in Tasks and Arrivals
    for row in ws_tasks.iter_rows(min_row=2):
        for column_index in (3, 4):
            cell = row[column_index - 1]
            if isinstance(cell.value, datetime):
                cell.number_format = "yyyy-mm-dd hh:mm:ss"

    for row in ws_arrivals.iter_rows(min_row=2):
        ws_arrivals.cell(row=row[0].row, column=2).number_format = (
            "yyyy-mm-dd hh:mm:ss"
        )

    # Save to the specified folder
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)

    # Verify that the file exists and is not empty
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(
            f"Excel export failed. Expected file:\n{output_path}"
        )

    return output_path


# ============================================================
# 7. RUN THE SIMULATION AND EXPORT
# ============================================================

def main():
    rate_per_hour = 0.4

    print("Loading calendar...")
    print(f"ICS file: {ICS_FILE}")

    tasks = load_calendar(ICS_FILE)
    print(f"Calendar events loaded: {len(tasks)}")

    if not tasks:
        raise ValueError(
            "No calendar events were found in the ICS file."
        )

    print("Generating Poisson arrivals...")
    triggers, simulation_start, simulation_end = generate_triggers(
        tasks,
        rate_per_hour=rate_per_hour,
        seed=42,
    )

    print(f"Poisson arrivals generated: {len(triggers)}")

    metrics = calculate_metrics(
        tasks,
        triggers,
        simulation_start,
        simulation_end,
        rate_per_hour,
    )

    print("Exporting results to Excel...")

    saved_path = export_to_excel(
        tasks,
        triggers,
        metrics,
        output_file,
    )

    print("\nExcel file successfully saved!")
    print(f"Full path: {saved_path.resolve()}")
    print(f"File size: {saved_path.stat().st_size:,} bytes")

    print("\nKey metrics:")
    for metric, value in metrics:
        print(f"{metric}: {value}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nERROR: The script could not complete.")
        print(f"{type(error).__name__}: {error}")
        raise
