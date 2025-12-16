# 3D Cylinder Water Entry Simulation

This project simulates a 3D cylinder entering water using the SPH (Smoothed Particle Hydrodynamics) method with SPHinXsys.

## Simulation Parameters

### Cylinder
- **Diameter**: 40 mm (0.04 m)
- **Height**: 300 mm (0.3 m)
- **Mass**: 0.4 kg
- **Entry velocity**: 10 m/s (downward)

### Water Domain
- **Length**: 1.0 m
- **Width**: 0.2 m
- **Height**: 0.8 m
- **Density**: 1000 kg/m³

### Numerical Setup
- **Particle spacing**: 2 mm (cylinder_diameter / 20)
- **Simulation time**: 1.0 s
- **Output interval**: 0.01 s

## Features

1. **6-DOF Motion Recording**: Tracks position, velocity, and acceleration of the cylinder's center of mass and additional observation points for rotation analysis.

2. **Force Recording**: Records viscous and pressure forces acting on the cylinder.

3. **Energy Analysis**: Monitors total mechanical energy throughout the simulation.

4. **Particle Visualization**: Outputs VTP files for visualization in ParaView.

5. **Data Analysis**: Python script for generating motion curves and summary statistics.

## Building the Project

### Prerequisites
- SPHinXsys library installed
- CMake (version 3.16 or higher)
- C++ compiler with C++17 support
- Python 3.x with numpy and matplotlib (for data analysis)

### Build Instructions

```bash
# Navigate to the project directory
cd tests/user_examples/test_3d_cylinder_water_entry

# Create build directory
mkdir -p build
cd build

# Configure with CMake
cmake ..

# Build
make -j$(nproc)
```

## Running the Simulation

```bash
# From the build directory
cd bin
./test_3d_cylinder_water_entry
```

The simulation will create an `output` directory containing:
- **VTP files**: For 3D visualization in ParaView
- **DAT files**: Observation data (position, velocity, acceleration, forces, energy)

## Analyzing Results

After the simulation completes, run the Python analysis script:

```bash
# From the build directory
python3 ../analyze_motion.py ./bin/output ./bin/analysis_results
```

This will generate:
- `displacement.png`: Displacement curves (x, y, z, and magnitude)
- `velocity.png`: Velocity curves (x, y, z, and magnitude)
- `acceleration.png`: Acceleration curves (x, y, z, and magnitude)
- `forces.png`: Force analysis (viscous, pressure, total, and drag coefficient)
- `energy.png`: Mechanical energy evolution
- `simulation_summary.txt`: Summary report with key statistics

## Visualizing in ParaView

1. Open ParaView
2. Load the VTP files from `bin/output/`
3. Recommended views:
   - **Water particles**: Color by "Pressure" or "Velocity"
   - **Cylinder**: Color by "Velocity" or solid color
   - **Animation**: Play through time steps to see the water entry process

### ParaView Tips
- Use "Glyph" filter to show velocity vectors
- Use "Clip" filter to create cross-section views
- Use "Threshold" filter to show only surface particles
- Enable "Surface With Edges" for better particle visualization

## Output Files

### VTP Files (Visualization)
- `WaterBody_*.vtp`: Water particle states
- `Cylinder_*.vtp`: Cylinder particle states
- `WallBoundary_*.vtp`: Wall boundary particles

### DAT Files (Observation Data)

#### Motion Data
- `CylinderObserver_Position.dat`: Position of observation points
- `CylinderObserver_Velocity.dat`: Velocity of observation points
- `CylinderObserver_AccelerationPrior.dat`: Acceleration of observation points

#### Force Data
- `Cylinder_ViscousForceFromFluid.dat`: Viscous forces
- `Cylinder_PressureForceFromFluid.dat`: Pressure forces

#### Energy Data
- `Cylinder_TotalMechanicalEnergy.dat`: Mechanical energy

### Data File Format

Observation data files have the following format:
```
run_time  Variable[0][0]  Variable[0][1]  Variable[0][2]  ...
0.0000    value_x         value_y         value_z         ...
0.0001    value_x         value_y         value_z         ...
...
```

Where:
- `run_time`: Simulation time
- `[0]`: Observer point index (0 = center of mass)
- `[0]`, `[1]`, `[2]`: x, y, z components

## Customization

### Modifying Simulation Parameters

Edit `cylinder_water_entry.cpp`:

```cpp
// Geometry
Real cylinder_diameter = 0.04;      // Cylinder diameter
Real cylinder_height = 0.3;         // Cylinder height
Real water_length = 1.0;            // Water tank dimensions
Real water_width = 0.2;
Real water_height = 0.8;

// Physics
Real rho0_f = 1000.0;               // Water density
Vecd cylinder_initial_velocity(0.0, 0.0, -10.0);  // Entry velocity

// Numerical
Real particle_spacing_ref = cylinder_diameter / 20.0;  // Resolution
Real end_time = 1.0;                // Simulation duration
Real output_interval = 0.01;        // Output frequency
```

### Adding More Observation Points

Modify the `createObserverPoints()` function to add more observation points for detailed 6-DOF analysis.

### Changing Output Quantities

Add or remove quantities in the `body_states_recording` section:

```cpp
body_states_recording.addToWrite<Vecd>(cylinder, "Force");
body_states_recording.addToWrite<Real>(water_block, "Temperature");
```

## Physics Background

### SPH Method
This simulation uses the Smoothed Particle Hydrodynamics method, where both the fluid and solid are represented by discrete particles. Particle interactions are computed using smoothing kernels.

### FSI Coupling
Fluid-Structure Interaction is handled through:
1. **Pressure forces**: Computed from fluid pressure on cylinder surface
2. **Viscous forces**: Computed from fluid viscosity
3. **Rigid body dynamics**: Cylinder motion governed by Newton's laws

### Key Equations

**Momentum equation (fluid)**:
```
dv/dt = -∇P/ρ + ν∇²v + g
```

**Rigid body motion**:
```
M dv/dt = F_pressure + F_viscous + F_gravity
```

## Troubleshooting

### Compilation Errors
- Ensure SPHinXsys is properly installed
- Check CMake can find `sphinxsys_3d` library
- Verify C++17 support in your compiler

### Runtime Errors
- **Segmentation fault**: May indicate insufficient memory or particle configuration issues
- **Slow performance**: Reduce particle resolution or simulation time
- **Unstable simulation**: Check time step size and material properties

### Analysis Script Issues
- **File not found**: Check that simulation completed and output files exist
- **Import errors**: Install required Python packages: `pip install numpy matplotlib`
- **Empty plots**: Verify observation data files contain data

## Performance Tips

1. **Particle resolution**: Use `cylinder_diameter / 20` for good accuracy
2. **Parallel execution**: SPHinXsys uses OpenMP; set `OMP_NUM_THREADS` environment variable
3. **Particle sorting**: Enabled by default every 100 iterations for better cache performance
4. **Output frequency**: Reduce output interval for faster simulation

## References

1. SPHinXsys Documentation: https://www.sphinxsys.org/
2. SPHinXsys GitHub: https://github.com/Xiangyu-Hu/SPHinXsys
3. SPH Method: Liu, G. R., & Liu, M. B. (2003). Smoothed particle hydrodynamics: a meshfree particle method.

## License

This project follows the SPHinXsys license terms.

## Contact

For issues and questions about this simulation case, please refer to the SPHinXsys community forums or GitHub issues.
