# ============================================================
# SORTLINK — DYNAMIC DATA MODELS
# ============================================================

ZONES = ["A", "B", "C", "D"]


def normalize_zone(value):
    """
    Converts common dashboard zone representations into A/B/C/D.
    """
    if value is None:
        return None

    value = str(value).strip().upper()

    aliases = {
        "ZONE A": "A",
        "ZONE B": "B",
        "ZONE C": "C",
        "ZONE D": "D",
        "A": "A",
        "B": "B",
        "C": "C",
        "D": "D",
    }

    return aliases.get(value)


def validate_vehicle(vehicle):
    required = ["id", "zone", "capacity"]

    for field in required:
        if field not in vehicle:
            raise ValueError(f"Vehicle field '{field}' is required.")

    vehicle_id = str(vehicle["id"]).strip()
    zone = normalize_zone(vehicle["zone"])

    try:
        capacity = float(vehicle["capacity"])
    except (TypeError, ValueError):
        raise ValueError(f"Invalid capacity for vehicle {vehicle_id}.")

    if not vehicle_id:
        raise ValueError("Vehicle ID cannot be empty.")

    if zone is None:
        raise ValueError(
            f"Invalid zone for vehicle {vehicle_id}. "
            f"Use A, B, C or D."
        )

    if capacity <= 0:
        raise ValueError(
            f"Capacity for vehicle {vehicle_id} must be greater than zero."
        )

    return {
        "id": vehicle_id,
        "zone": zone,
        "capacity": capacity
    }


def validate_parcel(parcel):
    required = ["id", "weight", "zone"]

    for field in required:
        if field not in parcel:
            raise ValueError(f"Parcel field '{field}' is required.")

    parcel_id = str(parcel["id"]).strip()
    zone = normalize_zone(parcel["zone"])

    try:
        weight = float(parcel["weight"])
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid weight for parcel {parcel_id}."
        )

    if not parcel_id:
        raise ValueError("Parcel ID cannot be empty.")

    if zone is None:
        raise ValueError(
            f"Invalid destination for parcel {parcel_id}. "
            f"Use A, B, C or D."
        )

    if weight <= 0:
        raise ValueError(
            f"Weight for parcel {parcel_id} must be greater than zero."
        )

    return {
        "id": parcel_id,
        "weight": weight,
        "zone": zone
    }