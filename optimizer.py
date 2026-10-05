# ============================================================
# SORTLINK — PYTHON OPTIMIZER
# ============================================================

from collections import defaultdict


def optimize_parcels(parcels, vehicles):
    """
    Dynamic multi-zone / multi-vehicle optimization.

    Vehicles are supplied by the dashboard.
    No vehicle count, zone or capacity is hard-coded.
    """

    if not parcels:
        raise ValueError("No parcels were supplied.")

    if not vehicles:
        raise ValueError("No vehicles were supplied.")

    vehicle_state = {}

    for vehicle in vehicles:
        vehicle_state[vehicle["id"]] = {
            "id": vehicle["id"],
            "zone": vehicle["zone"],
            "capacity": float(vehicle["capacity"]),
            "load": 0.0,
            "parcels": []
        }

    assignments = []

    # Group vehicles by destination zone
    vehicles_by_zone = defaultdict(list)

    for vehicle in vehicle_state.values():
        vehicles_by_zone[vehicle["zone"]].append(vehicle)

    # Heaviest parcels first improves packing
    sorted_parcels = sorted(
        parcels,
        key=lambda p: float(p["weight"]),
        reverse=True
    )

    for parcel in sorted_parcels:

        parcel_id = parcel["id"]
        parcel_zone = parcel["zone"]
        parcel_weight = float(parcel["weight"])

        matching = vehicles_by_zone.get(parcel_zone, [])

        if not matching:
            raise ValueError(
                f"No vehicle is available for zone {parcel_zone} "
                f"for parcel {parcel_id}."
            )

        # A parcel must fit completely inside one vehicle.
        possible = [
            vehicle
            for vehicle in matching
            if vehicle["load"] + parcel_weight <= vehicle["capacity"]
        ]

        if not possible:
            raise ValueError(
                f"No available vehicle in zone {parcel_zone} "
                f"has enough remaining capacity for parcel {parcel_id} "
                f"({parcel_weight:g} kg)."
            )

        # Prefer vehicle with the smallest remaining capacity
        # after loading this parcel.
        selected = min(
            possible,
            key=lambda v: (
                v["capacity"] - (v["load"] + parcel_weight),
                v["load"]
            )
        )

        selected["load"] += parcel_weight
        selected["parcels"].append(parcel_id)

        assignments.append({
            "parcel_id": parcel_id,
            "weight": parcel_weight,
            "zone": parcel_zone,
            "vehicle_id": selected["id"]
        })

    vehicle_results = []

    for vehicle in vehicle_state.values():

        utilization = 0.0

        if vehicle["capacity"] > 0:
            utilization = (
                vehicle["load"] / vehicle["capacity"]
            ) * 100.0

        vehicle_results.append({
            "vehicle_id": vehicle["id"],
            "zone": vehicle["zone"],
            "capacity": vehicle["capacity"],
            "load": vehicle["load"],
            "remaining_capacity":
                vehicle["capacity"] - vehicle["load"],
            "utilization": round(utilization, 2),
            "parcel_count": len(vehicle["parcels"]),
            "parcels": vehicle["parcels"],
            "status":
                "Loaded" if vehicle["load"] > 0 else "Available"
        })

    active_vehicles = sum(
        1
        for vehicle in vehicle_results
        if vehicle["load"] > 0
    )

    total_capacity = sum(
        vehicle["capacity"]
        for vehicle in vehicle_results
    )

    total_load = sum(
        vehicle["load"]
        for vehicle in vehicle_results
    )

    overall_utilization = 0.0

    if total_capacity > 0:
        overall_utilization = (
            total_load / total_capacity
        ) * 100.0

    return {
        "assignments": assignments,
        "vehicles": vehicle_results,
        "summary": {
            "total_parcels": len(parcels),
            "total_vehicles": len(vehicles),
            "active_vehicles": active_vehicles,
            "total_capacity": total_capacity,
            "total_load": total_load,
            "overall_utilization":
                round(overall_utilization, 2)
        }
    }


# Compatibility function
def optimize_parcel(destination, weight, vehicles):
    """
    Single-parcel compatibility interface.
    """

    parcel = {
        "id": "P1",
        "weight": float(weight),
        "zone": destination
    }

    result = optimize_parcels(
        [parcel],
        vehicles
    )

    return result