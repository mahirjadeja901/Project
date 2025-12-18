# Model.py  (Streamlit app)

import streamlit as st  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import io
import json

st.set_page_config(page_title="Agricultural Robot Flat Patterns", layout="wide")

st.title("🔧 Agricultural Robot Chassis - Flat Patterns")
st.write("Detailed cutting patterns for 18‑gauge steel sheet fabrication.")

# --- Sidebar: component selection ---
components = [
    "Base Chassis Platform",
    "Middle Frame Section",
    "Upper Platform",
    "Front Extension Arms",
    "Wheel Mounting Bracket",
    "Solar Panel Frame",
    "Battery Tray",
]
component = st.sidebar.selectbox("Select Component", components)

# --- Sidebar: dimensions input ---
st.sidebar.markdown("### Custom Dimensions (mm)")
length = st.sidebar.number_input("Length (mm)", min_value=50.0, max_value=3000.0, value=600.0)
width = st.sidebar.number_input("Width (mm)", min_value=50.0, max_value=3000.0, value=400.0)
thickness = 1.2  # 18‑gauge steel (approx)

# Simple component-specific parameter
if component == "Base Chassis Platform":
    corner_radius = 20
elif component == "Wheel Mounting Bracket":
    corner_radius = 10
else:
    corner_radius = 0

# --- Generate parametric model from dimensions ---
def generate_model(component_name, L, W, t, corner_r):
    """Return a parametric model dictionary from basic dimensions."""
    bend_offset = 50  # example value, mm
    hole_offset = 10  # example value, mm

    model = {
        "component": component_name,
        "length_mm": L,
        "width_mm": W,
        "thickness_mm": t,
        "corner_radius_mm": corner_r,
        "features": {
            "plate": {
                "origin": [0, 0],
                "length": L,
                "width": W,
            },
            "bend_lines": [
                {"x": bend_offset, "y_start": 0, "y_end": W},
                {"x": L - bend_offset, "y_start": 0, "y_end": W},
            ],
            "holes": [
                {"x": hole_offset, "y": hole_offset},
                {"x": L - hole_offset, "y": hole_offset},
                {"x": hole_offset, "y": W - hole_offset},
                {"x": L - hole_offset, "y": W - hole_offset},
            ],
        },
    }
    return model

model = generate_model(component, length, width, thickness, corner_radius)

# --- Main layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Flat Pattern Diagram")
    fig, ax = plt.subplots()

    # Plate
    plate_rect = Rectangle((0, 0), length, width, fill=False, linewidth=2)
    ax.add_patch(plate_rect)

    # Bend lines
    for bend in model["features"]["bend_lines"]:
        ax.axvline(bend["x"], color="orange", linestyle="--", linewidth=1)

    # Holes
    hole_x = [h["x"] for h in model["features"]["holes"]]
    hole_y = [h["y"] for h in model["features"]["holes"]]
    ax.scatter(hole_x, hole_y, color="red", s=20)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-20, length + 20)
    ax.set_ylim(-20, width + 20)
    ax.set_xlabel("Length (mm)")
    ax.set_ylabel("Width (mm)")
    ax.set_title(f"{component} - Flat Pattern")

    st.pyplot(fig)

with col2:
    st.subheader("Fabrication Notes")
    st.markdown(
        f"""
**Component:** {component}  

- Material: 18‑gauge (1.2 mm) cold‑rolled mild steel.  
- Bend allowance: Add 1.9 mm to each 90° bend.  
- Hole clearances: Drill undersized, then ream to final size.  
- Tolerances: ±0.5 mm for cuts, ±1° for bends.  
- Edge treatment: Deburr all edges with file or grinder.  
- Nesting: Optimized for 4'×8' sheet where possible.  
"""
    )

    st.markdown("### Generated Model (Parametric Data)")
    st.json(model)

    # ---- Export model as CSV ----
    feature_rows = []

    # Plate
    plate = model["features"]["plate"]
    feature_rows.append(
        {
            "type": "plate",
            "x": plate["origin"][0],
            "y": plate["origin"][1],
            "length": plate["length"],
            "width": plate["width"],
        }
    )

    # Bend lines
    for i, bend in enumerate(model["features"]["bend_lines"], start=1):
        feature_rows.append(
            {
                "type": "bend_line",
                "id": i,
                "x": bend["x"],
                "y_start": bend["y_start"],
                "y_end": bend["y_end"],
            }
        )

    # Holes
    for i, hole in enumerate(model["features"]["holes"], start=1):
        feature_rows.append(
            {
                "type": "hole",
                "id": i,
                "x": hole["x"],
                "y": hole["y"],
            }
        )

    df = pd.DataFrame(feature_rows)

    # CSV buffer
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        "📥 Export Model CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{component.replace(' ', '_').lower()}_model.csv",
        mime="text/csv",
    )

    # ---- Export model as JSON (for CAD scripts / backends) ----
    json_buffer = io.StringIO()
    json.dump(model, json_buffer, indent=2)

    st.download_button(
        "📥 Export Model JSON",
        data=json_buffer.getvalue(),
        file_name=f"{component.replace(' ', '_').lower()}_model.json",
        mime="application/json",
    )

st.markdown("---")
st.caption(
    "The model is defined parametrically from the given dimensions. Import the CSV/JSON into your CAD or CAM scripts (e.g., Fusion 360 API) to generate DXF/3D geometry."
)
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np
import io
import json

# Page configuration
st.set_page_config(page_title="Agricultural Robot Design Suite", layout="wide", initial_sidebar_state="expanded")

# Sidebar navigation
st.sidebar.markdown("# 🌾 Agricultural Robot Design Suite")
page = st.sidebar.radio("Select Tool", options=["🛞 Motor Selector", "📐 Flat Patterns", "📋 Documentation"])

# Motor database (shared)
motor_database = {
    "DC_Gear_Motor_12V_100RPM_50W": {
        "type": "DC Gear Motor", "voltage": 12, "power": 50, "torque": 4.2, "rpm": 100, 
        "current": 5, "model": "12V 100RPM 50W", "applications": ["wheels", "ploughing"], "approx_cost": 400
    },
    "DC_Gear_Motor



