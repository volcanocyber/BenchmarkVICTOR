"""
Example setup for laboratory-scale lava flow simulations using synthetic topography.

This example demonstrates how to run models at cm to dm scales without requiring
a georeferenced DEM, using the improved set_topo_* functions.
"""

import sim
from globals import params as p
from globals import grids as g
import numpy as np

# ==============================================================================
# 1. TOPOGRAPHY SETUP - Choose one of these options:
# ==============================================================================

# Option A: Simple inclined plane (easiest starting point)
sim.set_topo_incline(
    slope_angle = -10.0,              # degrees (negative = elevation high on left, low on right)
    length_upstream = 0.5,            # meters
    length_downstream = 5.0,          # meters
    width = 3.0,                      # meters
    dx = 0.02,                        # 1 cm grid spacing
    dy = 0.02,
    )

# Export topography for visualization
sim.export_dem('topography_incline.asc', format='ascii')

# Option B: Flat domain (for comparison or baseline)
# sim.set_topo_flat(
#     length_x = 5.0,                 # total length in x
#     length_y = 3.0,                 # total length in y
#     base_elevation = 0.0,
#     dx = 0.01,
#     dy = 0.01
#     )

# Option C: Conical dome
# sim.set_topo_cone(
#     radius = 1.0,                   # cone radius
#     height = 0.5,                   # cone height
#     center_x = 0.0,
#     center_y = 0.0,
#     domain_size = 6.0,
#     dx = 0.01,
#     dy = 0.01
#     )

# Option D: V-shaped valley
# sim.set_topo_valley(
#     valley_depth = 0.2,
#     valley_width = 1.0,
#     valley_length = 5.0,
#     side_slope = 30.0,
#     domain_size = 8.0,
#     dx = 0.01,
#     dy = 0.01
#     )

#
#===============================================================================
# 2. INITIALIZATION
#===============================================================================
sim.set_init(
    init_type = None,                 # Start from bare ground, no previous model
    init_file = None
    )

#
#===============================================================================
# 3. LAVA PROPERTIES
#===============================================================================

# Lab-scale analog material properties (typical for PDMS or similar)
sim.set_vent_props(
    temperature_vent_C = 1150,        # Core temperature (K)
    viscosity_melt_vent = 200*(1 - 0.25/.64)**-2.5,  # Pa·s
    cryst_vent = 0.00                 # Erupted crystal fraction
    )

sim.set_lava_props(
    liquid_density = 2700,            # kg/m³
    porosity = 0.25,                  # Porosity for bulk density
    lava_specific_heat = 1500,        # J/(kg·K)
    lava_diffusivity = 1e-6,          # m²/s (higher for analog materials)
    lava_conductivity = None,         # Will be calculated from diffusivity
    lava_emissivity = 0.95
    )

#
#===============================================================================
# 4. RHEOLOGICAL PROPERTIES
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
# 5. AMBIENT CONDITIONS
#===============================================================================
sim.set_ambient(
    atm_temperature = 300,            # Room temperature (K)
    h_conv = 10,                      # Convection coeff, W/(m²·K)
    ground_temperature = 300          # Initial ground temp (K)
    )

#
#===============================================================================
# 6. NUMERICAL SETTINGS
#===============================================================================
sim.set_numerics(
    efficiency_min = 0,               # Min model:wall-clock ratio
    efficiency_max = 10000,           # Max allowed ratio
    cfl_max = 0.7,                    # Courant-Friedrichs-Lewy condition at stability limit (trades accuracy for speed)
    dt_max = 0.01,                    # Max time step (seconds)
    fraction_to_freeze = 0.0,         # Freezing fraction (0 for isothermal)
    tiny_flow = 6e-5,                 # Min lava thickness (m)
    )

#
#===============================================================================
# 7. VENT SPECIFICATION - Choose one approach
#===============================================================================

# Approach A: Simple programmatic vent setup (recommended for synthetic topo)
sim.set_vent_simple(
    x_center = 0.0,                   # meters
    y_center = 0.0,                   # meters
    vent_width = 0.06,                # 6 cm fissure
    discharge = 1.222e-4,             # m³/s (DRE)
    duration_hr = 0.3,                # 6 minutes (0.1 hours)
    orientation = 'NS'                # North-South oriented fissure
    )

# Approach B: Using external vent file (original method)
# sim.set_source(
#     path_to_vent_files = './example_vents'
#     )

#
#===============================================================================
# 8. RUNTIME CONFIGURATION
#===============================================================================
sim.set_runtime(
    max_iter = None,                  # No iteration limit
    max_time_hr = 0.3,                # 0.1 hours = 6 minutes
    out_times = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3],  # Output at these times (hours)
    run_to_ocean = False              # No ocean boundary for simple topo
    )

#
#===============================================================================
# 9. OUTPUT CONFIGURATION
#===============================================================================
sim.set_output(
    path_out = './outputs/inclined/'            # Directory for output NetCDF file
    )

#
#===============================================================================
# 10. RUN THE SIMULATION
#===============================================================================
print("\n" + "="*70)
print("Starting Laboratory-Scale Lava Flow Simulation")
print("="*70 + "\n")

sim.run()

print("\n" + "="*70)
print("Simulation Complete!")
print("="*70 + "\n")
