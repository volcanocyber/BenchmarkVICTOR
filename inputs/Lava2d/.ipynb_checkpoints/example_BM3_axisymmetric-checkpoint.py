import sim
from globals import params as p
from globals import grids as g
import numpy as np

# ==============================================================================
# 1. TOPOGRAPHY SETUP - Flat horizontal plane
# ==============================================================================

sim.set_topo_flat(
    length_x = 1.0,                   # meters, total domain length (x)
    length_y = 1.0,                   # meters, total domain length (y)
    base_elevation = 0.0,             # meters, no elevation
    dx = 0.003,                        # 2 cm grid spacing
    dy = 0.003
    )

# Export the DEM for visualization
sim.export_dem('BM3_topography_flat.asc', format='ascii')

#
#===============================================================================
# 2. INITIALIZATION
#===============================================================================
sim.set_init(
    init_type = None,                 # Start from bare ground
    init_file = None
    )

#
#===============================================================================
# 3. LAVA PROPERTIES
#===============================================================================

# Simplified rheology for benchmarking
sim.set_vent_props(
    temperature_vent_C = 1150,        # Core temperature (K)
    viscosity_melt_vent = 200*(1 - 0.25/.64)**-2.5,  # Pa·s
    cryst_vent = 0.00                 # No crystallization
    )

sim.set_lava_props(
    liquid_density = 2700,            # kg/m³
    porosity = 0.25,                  # Porosity
    lava_specific_heat = 1500,        # J/(kg·K)
    lava_diffusivity = 1e-6,          # m²/s
    lava_conductivity = None,         # Calculated from diffusivity
    lava_emissivity = 0.95
    )

#
#===============================================================================
# 4. RHEOLOGICAL PROPERTIES
#===============================================================================

# Isothermal, purely viscous flow
sim.set_rheo(
    phi_max = 0.6,                    # Max crystal packing
    phi_inf = 0.58,                   # Equilibrium crystal fraction
    max_cryst_rate = 0.0,             # s⁻¹ (0 for isothermal)
    yield_strength_crust = 0.0,       # Pa (0 for Newtonian)
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
    cfl_max = 0.8,                    # Courant-Friedrichs-Lewy at stability limit
    dt_max = 0.01,                    # Max time step (seconds)
    fraction_to_freeze = 0.0,         # Freezing fraction (0 for isothermal)
    tiny_flow = 2e-8,                 # Min lava thickness (m)
    )

#
#===============================================================================
# 7. VENT SPECIFICATION - Point source at cone apex
#===============================================================================

# Source at the center (cone apex, x=0, y=0)
# Discharge and duration can be adjusted for different spreading tests
sim.set_vent_simple(
    x_center = 0.0,                   # meters, at apex
    y_center = 0.0,                   # meters, at apex
    vent_width = 0.009,                # 5 cm effective source diameter
    discharge = 1e-5,                 # m³/s (DRE) - adjust for sensitivity studies
    duration_hr = 0.05,               # 3 minutes eruption duration
    orientation = 'NS'                # Orientation doesn't matter at point source
    )

#
#===============================================================================
# 8. RUNTIME CONFIGURATION
#===============================================================================

sim.set_runtime(
    max_iter = None,                  # No iteration limit
    max_time_hr = 0.05,               # 3 minutes total runtime
    out_times = [0.01, 0.02, 0.03, 0.04, 0.05],  # Output at these times (hours)
    run_to_ocean = False              # No ocean boundary
    )

#
#===============================================================================
# 9. OUTPUT CONFIGURATION
#===============================================================================

sim.set_output(
    path_out = './outputs/axisymmetric'            # Output directory
    )

#
#===============================================================================
# 10. RUN THE SIMULATION
#===============================================================================

print("\n" + "="*70)
print("BM3/BM-C: Cooling Isoviscous Axisymmetric Flow on Horizontal Plane")
print("="*70 + "\n")

sim.run()

print("\n" + "="*70)
print("Simulation Complete!")
print("="*70 + "\n")
