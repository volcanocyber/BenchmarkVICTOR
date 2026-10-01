"""
Example: Lava flow around a triangular obstacle on an inclined plane.

Recreates an experimental setup with a triangular steel obstacle located
on a sloping bed. The apex points left (upstream), and the opening angle
can be adjusted to study flow splitting behavior.

Experimental reference:
- Obstacle location: 45 cm from start of sandy bed (0.45 m)
- Obstacle arm length: 14 cm each side (0.14 m)
- Opening angle: 90° (default, adjustable)
"""

import sim
from globals import params as p
from globals import grids as g
import numpy as np

# ==============================================================================
# 1. CREATE INCLINED PLANE BASE TOPOGRAPHY
# ==============================================================================

sim.set_topo_incline(
    slope_angle = -14.0,              # degrees (negative = high on left)
    length_upstream = 0.5,            # meters (vent to upstream edge)
    length_downstream = 5.0,          # meters (vent to downstream edge)
    width = 3.0,                      # meters (y-direction)
    dx = 0.02,                        # 1 cm grid spacing
    dy = 0.02
    )

#
#===============================================================================
# 2. ADD TRIANGULAR OBSTACLE ON TOP OF INCLINE
#===============================================================================

# Position obstacle 45 cm (0.45 m) downstream from vent location
# With vent at x=0, obstacle center is at x=0.45
# Apex always points left (-x), opening angle is adjustable

sim.set_topo_triangle(
    height = 0.5,                     # meters (0.5 m high obstacle)
    arm_length = 0.28,                # meters (14 cm per side, as in experiment)
    center_x = 0.25,                  # meters, 45 cm from vent
    center_y = 0.0,                   # meters, centered on flow path
    opening_angle = 180.0,             # degrees (try 60, 90, 120 for different splits)
    apex_direction = 'left',          # Apex points left (upstream, -x direction)
    add_to_existing = True            # Add on top of inclined plane
    )

# Export topography for visualization
sim.export_dem('topography_incline_triangle.asc', format='ascii')

#
#===============================================================================
# 3. INITIALIZATION
#===============================================================================
sim.set_init(
    init_type = None,                 # Start from bare ground, no previous model
    init_file = None
    )

#
#===============================================================================
# 4. LAVA PROPERTIES
#===============================================================================

# Lab-scale analog material properties
sim.set_vent_props(
    temperature_vent_C = 1150,        # Core temperature (K)
    viscosity_melt_vent = 200*(1 - 0.25/.64)**-2.5,  # Pa·s
    cryst_vent = 0.00                 # Erupted crystal fraction
    )

sim.set_lava_props(
    liquid_density = 2700,            # kg/m³
    porosity = 0.25,                  # Porosity for bulk density
    lava_specific_heat = 1500,        # J/(kg·K)
    lava_diffusivity = 1e-6,          # m²/s
    lava_conductivity = None,         # Calculated from diffusivity
    lava_emissivity = 0.95
    )

#
#===============================================================================
# 5. RHEOLOGICAL PROPERTIES
#===============================================================================
sim.set_rheo(
    phi_max = 0.6,                    # Max crystal packing
    phi_inf = 0.58,                   # Equilibrium crystal fraction
    max_cryst_rate = 0.0,             # s⁻¹ (0 for isothermal)
    yield_strength_crust = 0.0,       # Pa (0 for isothermal)
    T_core_T_vent_equal = True        # Core = vent temperature
    )

#
#===============================================================================
# 6. AMBIENT CONDITIONS
#===============================================================================
sim.set_ambient(
    atm_temperature = 300,            # Room temperature (K)
    h_conv = 10,                      # Convection coeff, W/(m²·K)
    ground_temperature = 300          # Initial ground temp (K)
    )

#
#===============================================================================
# 7. NUMERICAL SETTINGS
#===============================================================================
sim.set_numerics(
    efficiency_min = 0,               # Min model:wall-clock ratio
    efficiency_max = 10000,           # Max allowed ratio
    cfl_max = 1.0,                    # Courant-Friedrichs-Lewy at stability limit
    dt_max = 0.01,                    # Max time step (seconds)
    fraction_to_freeze = 0.0,         # Freezing fraction (0 for isothermal)
    tiny_flow = 1e-5,                 # Min lava thickness (m)
    )

#
#===============================================================================
# 8. VENT SPECIFICATION
#===============================================================================

# Source at origin (upstream of obstacle)
sim.set_vent_simple(
    x_center = 0.0,                   # meters, at vent location
    y_center = 0.0,                   # meters, centered on obstacle
    vent_width = 0.06,                # 6 cm fissure width
    discharge = 0.77e-3,             # m³/s (DRE)
    duration_hr = 0.1,                # 6 minutes
    orientation = 'NS'                # North-South oriented fissure
    )

#
#===============================================================================
# 9. RUNTIME CONFIGURATION
#===============================================================================
sim.set_runtime(
    max_iter = None,                  # No iteration limit
    max_time_hr = 0.1,                # 0.1 hours = 6 minutes
    out_times = [0.02, 0.04, 0.06, 0.08, 0.1],  # Output times (hours)
    run_to_ocean = False              # No ocean boundary
    )

#
#===============================================================================
# 10. OUTPUT CONFIGURATION
#===============================================================================
sim.set_output(
    path_out = './outputs/split/'            # Output directory
    )

#
#===============================================================================
# 11. RUN THE SIMULATION
#===============================================================================
print("\n" + "="*70)
print("Starting Lava Flow on Incline with Triangular Obstacle")
print("="*70 + "\n")

sim.run()

print("\n" + "="*70)
print("Simulation Complete!")
print("="*70 + "\n")
