# ============================================================
# SORTLINK — FLASK APPLICATION
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from data import (
    validate_parcel,
    validate_vehicle
)

from optimizer import optimize_parcels

from simulation import run_simulation

from matlab_bridge import optimize_with_matlab


app = Flask(__name__)


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ------------------------------------------------------------
# OPTIMIZE
# ------------------------------------------------------------

@app.route("/optimize", methods=["POST"])
def optimize():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received."
            }), 400

        raw_parcels = data.get("parcels", [])
        raw_vehicles = data.get("vehicles", [])

        if not raw_parcels:
            return jsonify({
                "success": False,
                "error": "At least one parcel is required."
            }), 400

        if not raw_vehicles:
            return jsonify({
                "success": False,
                "error": "At least one vehicle is required."
            }), 400

        # ----------------------------------------------------
        # VALIDATE PARCELS
        # ----------------------------------------------------

        parcels = []

        for index, parcel in enumerate(raw_parcels):

            try:

                parcels.append(
                    validate_parcel(parcel)
                )

            except ValueError as error:

                return jsonify({
                    "success": False,
                    "error":
                        f"Parcel {index + 1}: {error}"
                }), 400

        # ----------------------------------------------------
        # VALIDATE VEHICLES
        # ----------------------------------------------------

        vehicles = []

        for index, vehicle in enumerate(raw_vehicles):

            try:

                vehicles.append(
                    validate_vehicle(vehicle)
                )

            except ValueError as error:

                return jsonify({
                    "success": False,
                    "error":
                        f"Vehicle {index + 1}: {error}"
                }), 400

        # ----------------------------------------------------
        # PREPARE DATA FOR MATLAB
        # ----------------------------------------------------

        parcel_ids = [
            parcel["id"]
            for parcel in parcels
        ]

        weights = [
            float(parcel["weight"])
            for parcel in parcels
        ]

        parcel_zones = [
            parcel["zone"]
            for parcel in parcels
        ]

        vehicle_ids = [
            vehicle["id"]
            for vehicle in vehicles
        ]

        vehicle_zones = [
            vehicle["zone"]
            for vehicle in vehicles
        ]

        vehicle_capacities = [
            float(vehicle["capacity"])
            for vehicle in vehicles
        ]

        # ----------------------------------------------------
        # MATLAB OPTIMIZATION
        # ----------------------------------------------------
        #
        # MATLAB is the primary optimization engine.
        #
        # If MATLAB is installed and configured correctly,
        # the dashboard uses sortlink_optimization.m.
        #
        # If MATLAB is unavailable, Python optimization is
        # automatically used as a deployment fallback.
        # ----------------------------------------------------

        try:

            result = optimize_with_matlab(
                parcel_ids,
                weights,
                parcel_zones,
                vehicle_ids,
                vehicle_zones,
                vehicle_capacities
            )

            result["optimization_engine"] = "MATLAB"

        except Exception as matlab_error:

            print(
                "MATLAB optimization unavailable:"
            )

            print(matlab_error)

            result = optimize_parcels(
                parcels,
                vehicles
            )

            result["optimization_engine"] = (
                "Python Fallback"
            )

        # ----------------------------------------------------
        # KPI CALCULATION
        # ----------------------------------------------------

        kpis = run_simulation(result)

        result["kpis"] = kpis

        result["success"] = True

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "system": "SORTLINK"
    })


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )