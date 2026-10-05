// ============================================================
// SORTLINK — DYNAMIC BATCH OPTIMIZATION DASHBOARD
// ============================================================


// ------------------------------------------------------------
// DOM ELEMENTS
// ------------------------------------------------------------

const parcelContainer =
    document.getElementById("parcelContainer");

const vehicleContainer =
    document.getElementById("vehicleContainer");

const addParcelBtn =
    document.getElementById("addParcelBtn");

const addVehicleBtn =
    document.getElementById("addVehicleBtn");

const optimizeBtn =
    document.getElementById("optimizeBtn");

const clearBtn =
    document.getElementById("clearBtn");

const messageBox =
    document.getElementById("message");


// ------------------------------------------------------------
// STATE
// ------------------------------------------------------------

let parcelCounter = 0;
let vehicleCounter = 0;


// ------------------------------------------------------------
// ZONE OPTIONS
// ------------------------------------------------------------

function zoneOptions() {

    return `
        <option value="">Select Zone</option>
        <option value="A">Zone A</option>
        <option value="B">Zone B</option>
        <option value="C">Zone C</option>
        <option value="D">Zone D</option>
    `;
}


// ------------------------------------------------------------
// ADD PARCEL
// ------------------------------------------------------------

function addParcel(
    id = "",
    weight = "",
    zone = ""
) {

    parcelCounter++;

    const row =
        document.createElement("div");

    row.className =
        "dynamic-row parcel-row";

    row.dataset.index =
        parcelCounter;

    row.innerHTML = `

        <input
            class="input-field parcel-id"
            type="text"
            placeholder="Parcel ID"
            value="${id}"
        >

        <input
            class="input-field parcel-weight"
            type="number"
            min="0.01"
            step="0.01"
            placeholder="Weight (kg)"
            value="${weight}"
        >

        <select
            class="input-field parcel-zone"
        >
            ${zoneOptions()}
        </select>

        <button
            type="button"
            class="remove-button remove-parcel"
        >
            Remove
        </button>
    `;

    parcelContainer.appendChild(row);

    if (zone) {
        row.querySelector(".parcel-zone").value =
            zone;
    }
}


// ------------------------------------------------------------
// ADD VEHICLE
// ------------------------------------------------------------

function addVehicle(
    id = "",
    zone = "",
    capacity = ""
) {

    vehicleCounter++;

    const row =
        document.createElement("div");

    row.className =
        "dynamic-row vehicle-row";

    row.dataset.index =
        vehicleCounter;

    row.innerHTML = `

        <input
            class="input-field vehicle-id"
            type="text"
            placeholder="Vehicle ID"
            value="${id}"
        >

        <select
            class="input-field vehicle-zone"
        >
            ${zoneOptions()}
        </select>

        <input
            class="input-field vehicle-capacity"
            type="number"
            min="0.01"
            step="0.01"
            placeholder="Capacity (kg)"
            value="${capacity}"
        >

        <button
            type="button"
            class="remove-button remove-vehicle"
        >
            Remove
        </button>
    `;

    vehicleContainer.appendChild(row);

    if (zone) {
        row.querySelector(".vehicle-zone").value =
            zone;
    }
}


// ------------------------------------------------------------
// COLLECT PARCELS
// ------------------------------------------------------------

function collectParcels() {

    const rows =
        document.querySelectorAll(".parcel-row");

    const parcels = [];

    rows.forEach((row) => {

        const id =
            row.querySelector(".parcel-id")
                .value
                .trim();

        const weight =
            row.querySelector(".parcel-weight")
                .value;

        const zone =
            row.querySelector(".parcel-zone")
                .value;

        parcels.push({
            id: id,
            weight: Number(weight),
            zone: zone
        });
    });

    return parcels;
}


// ------------------------------------------------------------
// COLLECT VEHICLES
// ------------------------------------------------------------

function collectVehicles() {

    const rows =
        document.querySelectorAll(".vehicle-row");

    const vehicles = [];

    rows.forEach((row) => {

        const id =
            row.querySelector(".vehicle-id")
                .value
                .trim();

        const zone =
            row.querySelector(".vehicle-zone")
                .value;

        const capacity =
            row.querySelector(".vehicle-capacity")
                .value;

        vehicles.push({
            id: id,
            zone: zone,
            capacity: Number(capacity)
        });
    });

    return vehicles;
}


// ------------------------------------------------------------
// VALIDATE INPUT
// ------------------------------------------------------------

function validateInput(
    parcels,
    vehicles
) {

    if (parcels.length === 0) {
        return "Add at least one parcel.";
    }

    if (vehicles.length === 0) {
        return "Add at least one vehicle.";
    }


    const parcelIds =
        new Set();


    for (let i = 0; i < parcels.length; i++) {

        const parcel =
            parcels[i];

        if (!parcel.id) {
            return `Parcel ${i + 1}: ID is required.`;
        }

        if (parcelIds.has(parcel.id)) {
            return `Duplicate parcel ID: ${parcel.id}.`;
        }

        parcelIds.add(parcel.id);

        if (
            !Number.isFinite(parcel.weight) ||
            parcel.weight <= 0
        ) {
            return (
                `Parcel ${parcel.id}: `
                + "valid weight is required."
            );
        }

        if (!parcel.zone) {
            return (
                `Parcel ${parcel.id}: `
                + "destination/zone is required."
            );
        }
    }


    const vehicleIds =
        new Set();


    for (let i = 0; i < vehicles.length; i++) {

        const vehicle =
            vehicles[i];

        if (!vehicle.id) {
            return `Vehicle ${i + 1}: ID is required.`;
        }

        if (vehicleIds.has(vehicle.id)) {
            return `Duplicate vehicle ID: ${vehicle.id}.`;
        }

        vehicleIds.add(vehicle.id);

        if (!vehicle.zone) {
            return (
                `Vehicle ${vehicle.id}: `
                + "zone is required."
            );
        }

        if (
            !Number.isFinite(vehicle.capacity) ||
            vehicle.capacity <= 0
        ) {
            return (
                `Vehicle ${vehicle.id}: `
                + "valid capacity is required."
            );
        }
    }

    return null;
}


// ------------------------------------------------------------
// MESSAGE
// ------------------------------------------------------------

function showMessage(
    text,
    type = "error"
) {

    messageBox.textContent =
        text;

    messageBox.className =
        `message ${type}`;
}


function hideMessage() {

    messageBox.textContent = "";

    messageBox.className =
        "message hidden";
}


// ------------------------------------------------------------
// SHOW SECTIONS
// ------------------------------------------------------------

function showResults() {

    document
        .getElementById("summarySection")
        .classList.remove("hidden");

    document
        .getElementById("allocationSection")
        .classList.remove("hidden");

    document
        .getElementById("assignmentSection")
        .classList.remove("hidden");

    document
        .getElementById("kpiSection")
        .classList.remove("hidden");
}


// ------------------------------------------------------------
// RENDER SUMMARY
// ------------------------------------------------------------

function renderSummary(summary) {

    document.getElementById(
        "totalParcels"
    ).textContent =
        summary.total_parcels;

    document.getElementById(
        "totalVehicles"
    ).textContent =
        summary.total_vehicles;

    document.getElementById(
        "activeVehicles"
    ).textContent =
        summary.active_vehicles;

    document.getElementById(
        "overallUtilization"
    ).textContent =
        `${summary.overall_utilization}%`;
}


// ------------------------------------------------------------
// RENDER VEHICLES
// ------------------------------------------------------------

function renderVehicles(vehicles) {

    const tbody =
        document.getElementById(
            "vehicleResults"
        );

    tbody.innerHTML = "";

    vehicles.forEach((vehicle) => {

        const row =
            document.createElement("tr");

        const statusClass =
            vehicle.load > 0
                ? "status-loaded"
                : "status-available";

        row.innerHTML = `

            <td>
                ${escapeHtml(vehicle.vehicle_id)}
            </td>

            <td>
                Zone ${escapeHtml(vehicle.zone)}
            </td>

            <td>
                ${formatNumber(vehicle.capacity)} kg
            </td>

            <td>
                ${formatNumber(vehicle.load)} kg
            </td>

            <td>
                ${formatNumber(
                    vehicle.remaining_capacity
                )} kg
            </td>

            <td>
                ${formatNumber(
                    vehicle.utilization
                )}%
            </td>

            <td class="${statusClass}">
                ${escapeHtml(vehicle.status)}
            </td>
        `;

        tbody.appendChild(row);
    });
}


// ------------------------------------------------------------
// RENDER ASSIGNMENTS
// ------------------------------------------------------------

function renderAssignments(assignments) {

    const tbody =
        document.getElementById(
            "assignmentResults"
        );

    tbody.innerHTML = "";

    assignments.forEach((assignment) => {

        const row =
            document.createElement("tr");

        row.innerHTML = `

            <td>
                ${escapeHtml(
                    assignment.parcel_id
                )}
            </td>

            <td>
                ${formatNumber(
                    assignment.weight
                )} kg
            </td>

            <td>
                Zone ${escapeHtml(
                    assignment.zone
                )}
            </td>

            <td>
                ${escapeHtml(
                    assignment.vehicle_id
                )}
            </td>
        `;

        tbody.appendChild(row);
    });
}


// ------------------------------------------------------------
// RENDER KPIs
// ------------------------------------------------------------




// ------------------------------------------------------------
// NUMBER FORMAT
// ------------------------------------------------------------

function formatNumber(value) {

    const number =
        Number(value);

    if (!Number.isFinite(number)) {
        return "0";
    }

    return number
        .toFixed(2)
        .replace(/\.00$/, "");
}


// ------------------------------------------------------------
// HTML ESCAPE
// ------------------------------------------------------------

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ------------------------------------------------------------
// OPTIMIZE
// ------------------------------------------------------------

async function runOptimization() {

    hideMessage();

    const parcels =
        collectParcels();

    const vehicles =
        collectVehicles();

    const validationError =
        validateInput(
            parcels,
            vehicles
        );

    if (validationError) {

        showMessage(
            validationError,
            "error"
        );

        return;
    }


    optimizeBtn.disabled = true;

    optimizeBtn.textContent =
        "Optimizing...";


    try {

        const response =
            await fetch(
                "/optimize",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        parcels: parcels,
                        vehicles: vehicles
                    })
                }
            );


        const result =
            await response.json();


        if (!response.ok || !result.success) {

            throw new Error(
                result.error ||
                "Optimization failed."
            );
        }


        renderSummary(
            result.summary
        );

        renderVehicles(
            result.vehicles
        );

        renderAssignments(
            result.assignments
        );



        showResults();

        showMessage(
            "Optimization completed successfully.",
            "success"
        );

    } catch (error) {

        showMessage(
            error.message,
            "error"
        );

    } finally {

        optimizeBtn.disabled =
            false;

        optimizeBtn.textContent =
            "Run Optimization";
    }
}


// ------------------------------------------------------------
// CLEAR
// ------------------------------------------------------------

function clearDashboard() {

    parcelContainer.innerHTML = "";

    vehicleContainer.innerHTML = "";

    parcelCounter = 0;

    vehicleCounter = 0;

    hideMessage();


    document
        .getElementById("summarySection")
        .classList.add("hidden");

    document
        .getElementById("allocationSection")
        .classList.add("hidden");

    document
        .getElementById("assignmentSection")
        .classList.add("hidden");

    document
        .getElementById("kpiSection")
        .classList.add("hidden");


    addParcel();

    addVehicle();
}


// ------------------------------------------------------------
// REMOVE PARCEL / VEHICLE
// ------------------------------------------------------------

document.addEventListener(
    "click",
    function (event) {

        if (
            event.target.classList.contains(
                "remove-parcel"
            )
        ) {

            event.target
                .closest(".parcel-row")
                .remove();
        }


        if (
            event.target.classList.contains(
                "remove-vehicle"
            )
        ) {

            event.target
                .closest(".vehicle-row")
                .remove();
        }
    }
);


// ------------------------------------------------------------
// BUTTON EVENTS
// ------------------------------------------------------------

addParcelBtn.addEventListener(
    "click",
    () => addParcel()
);

addVehicleBtn.addEventListener(
    "click",
    () => addVehicle()
);

optimizeBtn.addEventListener(
    "click",
    runOptimization
);

clearBtn.addEventListener(
    "click",
    clearDashboard
);


// ------------------------------------------------------------
// INITIAL DATA
// ------------------------------------------------------------

addParcel(
    "P1",
    "12",
    "A"
);

addParcel(
    "P2",
    "8",
    "A"
);

addVehicle(
    "V1",
    "A",
    "20"
);

addVehicle(
    "V2",
    "A",
    "20"
);