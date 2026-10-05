# ============================================================
# SORTLINK — SIMULATION / KPI CALCULATIONS
# ============================================================

SORTING_TIME_PER_PARCEL = 5.0
POSITIONING_TIME = 2.0
HANDOFF_TIME = 1.5
DECISION_TO_ACTUATION = 0.08


def run_simulation(result):
    """
    Calculates SORTLINK KPI values from optimization output.
    """

    summary = result["summary"]

    parcel_count = summary["total_parcels"]

    sorting_time = SORTING_TIME_PER_PARCEL

    throughput = 0

    if sorting_time > 0:
        throughput = 3600 / sorting_time

    dwell_time = (
        POSITIONING_TIME +
        HANDOFF_TIME
    )

    return {
        "sorting_time_per_parcel":
            round(sorting_time, 2),

        "throughput_parcels_per_hour":
            round(throughput, 2),

        "vehicle_utilization":
            round(
                summary["overall_utilization"],
                2
            ),

        "dwell_time":
            round(dwell_time, 2),

        "mis_sort_rate":
            0.0,

        "decision_to_actuation_latency":
            round(DECISION_TO_ACTUATION, 2),

        "total_parcels":
            parcel_count,

        "active_vehicles":
            summary["active_vehicles"]
    }