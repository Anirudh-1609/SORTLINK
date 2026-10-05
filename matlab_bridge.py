# ============================================================
# SORTLINK — MATLAB BRIDGE
# ============================================================

import os
import shutil
import subprocess
import tempfile
import json


def matlab_available():
    """
    Checks whether MATLAB executable is available.
    """

    matlab_command = shutil.which("matlab")

    return matlab_command is not None


def optimize_with_matlab(
    parcel_ids,
    weights,
    parcel_zones,
    vehicle_ids,
    vehicle_zones,
    vehicle_capacities
):
    """
    Attempts MATLAB optimization.

    The dashboard remains functional even if MATLAB is not
    installed by raising a controlled exception so that Flask
    can use the Python fallback.
    """

    if not matlab_available():
        raise RuntimeError(
            "MATLAB executable was not found."
        )

    matlab_path = os.environ.get(
        "SORTLINK_MATLAB_PATH",
        ""
    )

    if not matlab_path:
        raise RuntimeError(
            "SORTLINK_MATLAB_PATH is not configured."
        )

    input_data = {
        "parcel_ids": parcel_ids,
        "weights": weights,
        "parcel_zones": parcel_zones,
        "vehicle_ids": vehicle_ids,
        "vehicle_zones": vehicle_zones,
        "vehicle_capacities": vehicle_capacities
    }

    with tempfile.TemporaryDirectory() as temp_dir:

        input_file = os.path.join(
            temp_dir,
            "sortlink_input.json"
        )

        output_file = os.path.join(
            temp_dir,
            "sortlink_output.json"
        )

        with open(
            input_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                input_data,
                file
            )

        matlab_script = f"""
        addpath('{matlab_path.replace("'", "''")}');

        data = jsondecode(fileread('{input_file.replace("'", "''")}'));

        result = sortlink_optimization( ...
            string(data.parcel_ids), ...
            double(data.weights), ...
            double(data.parcel_zones), ...
            string(data.vehicle_ids), ...
            string(data.vehicle_zones), ...
            double(data.vehicle_capacities));

        fid = fopen('{output_file.replace("'", "''")}', 'w');
        fprintf(fid, '%s', jsonencode(result));
        fclose(fid);
        """

        command = [
            "matlab",
            "-batch",
            matlab_script
        ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(
                process.stderr or
                "MATLAB optimization failed."
            )

        if not os.path.exists(output_file):
            raise RuntimeError(
                "MATLAB did not generate an output file."
            )

        with open(
            output_file,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)