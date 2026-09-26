import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Campus parking lot capacity
TOTAL_SLOTS = 15

# In-memory storage for parked vehicles
# Each item will be a dict: {"vehicle_no": str, "vehicle_type": str}
parked_vehicles = []


def get_slot_stats():
    """Helper function to calculate slot counts dynamically."""
    occupied = len(parked_vehicles)
    available = max(0, TOTAL_SLOTS - occupied)
    return TOTAL_SLOTS, occupied, available


@app.route("/")
def index():
    """Renders the dashboard with slot counts and parked vehicles."""
    total, occupied, available = get_slot_stats()
    # Read the commit hash provided by Render, fallback to 'local' for local dev
    commit_sha = os.getenv("RENDER_GIT_COMMIT", "local-dev")[:7]
    return render_template(
        "index.html",
        total=total,
        occupied=occupied,
        available=available,
        vehicles=parked_vehicles,
        commit=commit_sha
    )


@app.route("/park", methods=["POST"])
def park_vehicle():
    """Adds a new vehicle to the parking lot with validation."""
    vehicle_no = request.form.get("vehicle_no", "").strip().upper()
    vehicle_type = request.form.get("vehicle_type", "").strip()

    # Quality Gate / Validation: Check if lot is full
    if len(parked_vehicles) >= TOTAL_SLOTS:
        return jsonify({"error": "Parking lot is full"}), 400

    # Quality Gate / Validation: Empty inputs or invalid type
    if not vehicle_no or vehicle_type not in ["Car", "Bike"]:
        return jsonify({"error": "Invalid vehicle details"}), 400

    # Prevent duplicate entry of the same vehicle
    if any(v["vehicle_no"] == vehicle_no for v in parked_vehicles):
        return jsonify({"error": "Vehicle is already parked"}), 400

    parked_vehicles.append({
        "vehicle_no": vehicle_no,
        "vehicle_type": vehicle_type
    })
    return redirect("/")


@app.route("/exit", methods=["POST"])
def exit_vehicle():
    """Releases a vehicle from the parking lot."""
    vehicle_no = request.form.get("vehicle_no", "").strip().upper()
    global parked_vehicles
    parked_vehicles = [v for v in parked_vehicles if v["vehicle_no"] != vehicle_no]
    return redirect("/")


@app.route("/api/slots")
def api_slots():
    """Mandatory JSON API endpoint returning live state."""
    total, occupied, available = get_slot_stats()
    return jsonify({
        "total_slots": total,
        "occupied_slots": occupied,
        "available_slots": available,
        "vehicles": parked_vehicles
    })


@app.route("/health")
def health():
    """Mandatory health check endpoint for monitoring & pipeline."""
    return jsonify({
        "status": "ok",
        "commit": os.getenv("RENDER_GIT_COMMIT", "local-dev")
    }), 200


if __name__ == "__main__":
    # Render assigns a dynamic port via environment variable PORT
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)