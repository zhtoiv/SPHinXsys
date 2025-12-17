/**
 * @file    cylinder_water_entry.cpp
 * @brief   3D cylinder water entry simulation using SPH method
 * @details This simulation includes:
 *          - Fluid-structure interaction (FSI)
 *          - 6-DOF rigid body dynamics recording
 *          - Particle visualization output
 *          - Motion data analysis (displacement, velocity, acceleration)
 *
 * Cylinder parameters:
 *          - Diameter: 40mm (0.04m)
 *          - Height: 300mm (0.3m)
 *          - Mass: 0.4kg
 *          - Entry velocity: 10m/s (downward)
 *
 * Water domain:
 *          - Length: 1.0m
 *          - Width: 0.2m
 *          - Height: 0.8m
 */

#include "sphinxsys.h"
using namespace SPH;

//----------------------------------------------------------------------
//	Geometric parameters
//----------------------------------------------------------------------
Real cylinder_diameter = 0.04;                  // Cylinder diameter [m]
Real cylinder_radius = 0.5 * cylinder_diameter; // Cylinder radius [m]
Real cylinder_height = 0.3;                     // Cylinder height [m]
Real particle_spacing_ref = cylinder_diameter / 20.0; // Particle spacing

// Water domain dimensions
Real water_length = 1.0;                        // Water tank length [m]
Real water_width = 0.2;                         // Water tank width [m]
Real water_height = 0.8;                        // Water tank height [m]
Real BW = particle_spacing_ref * 4;             // Boundary wall thickness

// Domain bounds for the system
Real DL = water_length;
Real DW = water_width;
Real DH = water_height + 0.5;                   // Extra height for cylinder entry

// Cylinder initial position (centered horizontally, above water surface)
Vecd cylinder_center(0.5 * DL, 0.5 * DW, water_height + 0.5 * cylinder_height + 0.05);
Vecd cylinder_initial_velocity(0.0, 0.0, -10.0); // Entry velocity: 10 m/s downward

//----------------------------------------------------------------------
//	Material parameters
//----------------------------------------------------------------------
Real rho0_f = 1000.0;                           // Water density [kg/m^3]
Real rho0_s = 0.4 / (M_PI * pow(cylinder_radius, 2) * cylinder_height); // Cylinder density from mass
Real gravity_g = 9.81;                          // Gravity acceleration [m/s^2]
Real U_max = 10.0;                              // Maximum characteristic velocity
Real c_f = 10.0 * U_max;                        // Reference sound speed
Real mu_f = 1.0e-3;                             // Water dynamic viscosity [Pa·s]

//----------------------------------------------------------------------
//	Geometry definitions
//----------------------------------------------------------------------

// Water block shape
class WaterBlock : public ComplexShape
{
public:
    explicit WaterBlock(const std::string &shape_name) : ComplexShape(shape_name)
    {
        Vecd halfsize_water(0.5 * water_length, 0.5 * water_width, 0.5 * water_height);
        Vecd translation_water(0.5 * water_length, 0.5 * water_width, 0.5 * water_height);
        add<GeometricShapeBox>(Transform(translation_water), halfsize_water);
    }
};

// Wall boundary shape (hollow box)
class WallBoundary : public ComplexShape
{
public:
    explicit WallBoundary(const std::string &shape_name) : ComplexShape(shape_name)
    {
        Vecd halfsize_outer(0.5 * DL + BW, 0.5 * DW + BW, 0.5 * DH + BW);
        Vecd halfsize_inner(0.5 * DL, 0.5 * DW, 0.5 * DH);
        Vecd translation(0.5 * DL, 0.5 * DW, 0.5 * DH);
        add<GeometricShapeBox>(Transform(translation), halfsize_outer);
        subtract<GeometricShapeBox>(Transform(translation), halfsize_inner);
    }
};

// Cylinder shape
class CylinderShape : public ComplexShape
{
public:
    explicit CylinderShape(const std::string &shape_name) : ComplexShape(shape_name)
    {
        // Create cylinder along Z-axis
        // TriangleMeshShapeCylinder(axis_direction, radius, half_height, resolution, translation)
        int resolution = 40; // Resolution for triangle mesh
        add<TriangleMeshShapeCylinder>(SimTK::UnitVec3(0, 0, 1.0),
                                       cylinder_radius,
                                       0.5 * cylinder_height,
                                       resolution,
                                       cylinder_center);
    }
};

// Initial velocity condition for cylinder
class CylinderInitialVelocity : public LocalDynamics
{
public:
    explicit CylinderInitialVelocity(SPHBody &sph_body)
        : LocalDynamics(sph_body),
          pos_(particles_->getVariableDataByName<Vecd>("Position")),
          vel_(particles_->getVariableDataByName<Vecd>("Velocity")) {}

    void update(size_t index_i, Real dt)
    {
        vel_[index_i] = cylinder_initial_velocity;
    }

protected:
    Vecd *pos_;
    Vecd *vel_;
};

// Observer points for 6-DOF data recording
StdVec<Vecd> createObserverPoints()
{
    StdVec<Vecd> observation_points;
    // Center of mass
    observation_points.push_back(cylinder_center);
    // Points along cylinder axis for rotation measurement
    observation_points.push_back(cylinder_center + Vecd(0.0, 0.0, 0.4 * cylinder_height));
    observation_points.push_back(cylinder_center - Vecd(0.0, 0.0, 0.4 * cylinder_height));
    // Points on cylinder edge for rotation measurement
    observation_points.push_back(cylinder_center + Vecd(0.8 * cylinder_radius, 0.0, 0.0));
    observation_points.push_back(cylinder_center + Vecd(0.0, 0.8 * cylinder_radius, 0.0));
    return observation_points;
}

//----------------------------------------------------------------------
//	Main program
//----------------------------------------------------------------------
int main(int ac, char *av[])
{
    std::cout << "========================================" << std::endl;
    std::cout << "3D Cylinder Water Entry Simulation" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Cylinder - Diameter: " << cylinder_diameter * 1000 << " mm" << std::endl;
    std::cout << "         - Height: " << cylinder_height * 1000 << " mm" << std::endl;
    std::cout << "         - Mass: " << M_PI * pow(cylinder_radius, 2) * cylinder_height * rho0_s << " kg" << std::endl;
    std::cout << "         - Density: " << rho0_s << " kg/m^3" << std::endl;
    std::cout << "         - Entry velocity: " << abs(cylinder_initial_velocity[2]) << " m/s" << std::endl;
    std::cout << "Water    - Length: " << water_length << " m" << std::endl;
    std::cout << "         - Width: " << water_width << " m" << std::endl;
    std::cout << "         - Height: " << water_height << " m" << std::endl;
    std::cout << "         - Density: " << rho0_f << " kg/m^3" << std::endl;
    std::cout << "Particle spacing: " << particle_spacing_ref * 1000 << " mm" << std::endl;
    std::cout << "========================================" << std::endl;

    //----------------------------------------------------------------------
    //	Build up an SPHSystem
    //----------------------------------------------------------------------
    BoundingBoxd system_domain_bounds(Vecd(-BW, -BW, -BW),
                                       Vecd(DL + BW, DW + BW, DH + BW));
    SPHSystem sph_system(system_domain_bounds, particle_spacing_ref);
    sph_system.handleCommandlineOptions(ac, av);

    //----------------------------------------------------------------------
    //	Creating bodies with corresponding materials and particles
    //----------------------------------------------------------------------
    FluidBody water_block(sph_system, makeShared<WaterBlock>("WaterBody"));
    water_block.defineClosure<WeaklyCompressibleFluid, Viscosity>(
        ConstructArgs(rho0_f, c_f), mu_f);
    water_block.generateParticles<BaseParticles, Lattice>();

    SolidBody wall_boundary(sph_system, makeShared<WallBoundary>("WallBoundary"));
    wall_boundary.defineMaterial<Solid>();
    wall_boundary.generateParticles<BaseParticles, Lattice>();

    SolidBody cylinder(sph_system, makeShared<CylinderShape>("Cylinder"));
    cylinder.defineAdaptationRatios(1.15, 2.0);
    cylinder.defineBodyLevelSetShape();
    cylinder.defineMaterial<Solid>(rho0_s);
    cylinder.generateParticles<BaseParticles, Lattice>();

    // Observer body for recording cylinder motion (6-DOF data)
    ObserverBody cylinder_observer(sph_system, "CylinderObserver");
    cylinder_observer.generateParticles<ObserverParticles>(createObserverPoints());

    //----------------------------------------------------------------------
    //	Define body relation map
    //----------------------------------------------------------------------
    InnerRelation water_block_inner(water_block);
    InnerRelation cylinder_inner(cylinder);
    ContactRelation water_block_contact(water_block, {&wall_boundary, &cylinder});
    ContactRelation cylinder_contact(cylinder, {&water_block});
    ContactRelation cylinder_observer_contact(cylinder_observer, {&cylinder});
    ComplexRelation water_block_complex(water_block_inner, water_block_contact);

    //----------------------------------------------------------------------
    //	Define the numerical methods used in the simulation
    //----------------------------------------------------------------------
    // Gravity
    Gravity gravity(Vecd(0.0, 0.0, -gravity_g));
    SimpleDynamics<GravityForce<Gravity>> constant_gravity_to_fluid(water_block, gravity);
    SimpleDynamics<GravityForce<Gravity>> constant_gravity_to_cylinder(cylinder, gravity);

    // Wall and cylinder normal directions
    SimpleDynamics<NormalDirectionFromBodyShape> wall_boundary_normal_direction(wall_boundary);
    SimpleDynamics<NormalDirectionFromBodyShape> cylinder_normal_direction(cylinder);

    // Initial condition for cylinder velocity
    SimpleDynamics<CylinderInitialVelocity> cylinder_initial_velocity_setup(cylinder);

    // Fluid dynamics
    Dynamics1Level<fluid_dynamics::Integration1stHalfWithWallRiemann>
        pressure_relaxation(water_block_inner, water_block_contact);
    Dynamics1Level<fluid_dynamics::Integration2ndHalfWithWallRiemann>
        density_relaxation(water_block_inner, water_block_contact);
    InteractionWithUpdate<fluid_dynamics::DensitySummationComplexFreeSurface>
        update_density_by_summation(water_block_inner, water_block_contact);
    InteractionWithUpdate<fluid_dynamics::ViscousForceWithWall>
        viscous_force(water_block_inner, water_block_contact);

    // Time step size computation
    ReduceDynamics<fluid_dynamics::AdvectionTimeStep>
        get_fluid_advection_time_step_size(water_block, U_max);
    ReduceDynamics<fluid_dynamics::AcousticTimeStep>
        get_fluid_time_step_size(water_block);

    // FSI interactions
    InteractionWithUpdate<solid_dynamics::ViscousForceFromFluid>
        viscous_force_on_cylinder(cylinder_contact);
    InteractionWithUpdate<solid_dynamics::PressureForceFromFluid<decltype(density_relaxation)>>
        pressure_force_on_cylinder(cylinder_contact);

    // Solid dynamics - simplified for rigid body
    SimpleDynamics<solid_dynamics::UpdateElasticNormalDirection>
        cylinder_update_normal(cylinder);

    // Rigid body time step
    ReduceDynamics<solid_dynamics::AcousticTimeStep>
        cylinder_get_time_step_size(cylinder);

    // Particle sorting for efficiency
    ParticleSorting particle_sorting(water_block);

    //----------------------------------------------------------------------
    //	Define the methods for I/O operations, observations and analysis
    //----------------------------------------------------------------------
    // VTP output for visualization (ParaView)
    BodyStatesRecordingToVtp body_states_recording(sph_system);
    body_states_recording.addToWrite<Real>(water_block, "Pressure");
    body_states_recording.addToWrite<Real>(water_block, "Density");
    body_states_recording.addToWrite<int>(water_block, "SurfaceIndicator");
    body_states_recording.addToWrite<Vecd>(water_block, "Velocity");
    // Note: Cylinder velocity is recorded via observer, not per-particle
    body_states_recording.addToWrite<Vecd>(wall_boundary, "NormalDirection");

    // Observer data recording for 6-DOF motion analysis
    ObservedQuantityRecording<Vecd>
        write_cylinder_position("Position", cylinder_observer_contact);
    ObservedQuantityRecording<Vecd>
        write_cylinder_velocity("Velocity", cylinder_observer_contact);
    ObservedQuantityRecording<Vecd>
        write_cylinder_acceleration("AccelerationPrior", cylinder_observer_contact);

    // Reduced quantities (total forces, energy, etc.)
    ReducedQuantityRecording<QuantitySummation<Vecd>>
        write_total_viscous_force_on_cylinder(cylinder, "ViscousForceFromFluid");
    ReducedQuantityRecording<QuantitySummation<Vecd>>
        write_total_pressure_force_on_cylinder(cylinder, "PressureForceFromFluid");
    ReducedQuantityRecording<TotalMechanicalEnergy>
        write_cylinder_mechanical_energy(cylinder, gravity);

    //----------------------------------------------------------------------
    //	Prepare the simulation
    //----------------------------------------------------------------------
    sph_system.initializeSystemCellLinkedLists();
    sph_system.initializeSystemConfigurations();
    wall_boundary_normal_direction.exec();
    cylinder_normal_direction.exec();
    cylinder_initial_velocity_setup.exec();
    constant_gravity_to_fluid.exec();

    //----------------------------------------------------------------------
    //	Setup for time-stepping control
    //----------------------------------------------------------------------
    Real &physical_time = *sph_system.getSystemVariableDataByName<Real>("PhysicalTime");
    size_t number_of_iterations = 0;
    int screen_output_interval = 100;
    int observation_sample_interval = 10;
    Real end_time = 1.0;              // Total simulation time [s]
    Real output_interval = 0.01;      // VTP output interval [s]
    Real dt = 0.0;

    //----------------------------------------------------------------------
    //	Statistics for CPU time
    //----------------------------------------------------------------------
    TickCount t1 = TickCount::now();
    TimeInterval interval;

    //----------------------------------------------------------------------
    //	First output before the main loop
    //----------------------------------------------------------------------
    body_states_recording.writeToFile(0);
    write_cylinder_position.writeToFile(0);
    write_cylinder_velocity.writeToFile(0);
    write_cylinder_acceleration.writeToFile(0);
    write_total_viscous_force_on_cylinder.writeToFile(0);
    write_total_pressure_force_on_cylinder.writeToFile(0);
    write_cylinder_mechanical_energy.writeToFile(0);

    //----------------------------------------------------------------------
    //	Main loop starts here
    //----------------------------------------------------------------------
    std::cout << "Simulation started..." << std::endl;

    while (physical_time < end_time)
    {
        Real integration_time = 0.0;

        while (integration_time < output_interval)
        {
            Real Dt = get_fluid_advection_time_step_size.exec();
            update_density_by_summation.exec();
            viscous_force.exec();

            Real relaxation_time = 0.0;
            while (relaxation_time < Dt)
            {
                dt = SMIN(get_fluid_time_step_size.exec(), Dt - relaxation_time);

                // Fluid dynamics
                pressure_relaxation.exec(dt);

                // FSI coupling - forces on cylinder
                viscous_force_on_cylinder.exec();
                pressure_force_on_cylinder.exec();

                // Apply gravity to cylinder
                constant_gravity_to_cylinder.exec();

                // Fluid dynamics continues
                density_relaxation.exec(dt);

                relaxation_time += dt;
                integration_time += dt;
                physical_time += dt;
            }

            // Screen output
            if (number_of_iterations % screen_output_interval == 0)
            {
                std::cout << std::fixed << std::setprecision(6)
                          << "N=" << number_of_iterations
                          << "  Time=" << physical_time
                          << "  Dt=" << Dt
                          << "  dt=" << dt << std::endl;
            }

            // Record observation data
            if (number_of_iterations % observation_sample_interval == 0)
            {
                write_cylinder_position.writeToFile(number_of_iterations);
                write_cylinder_velocity.writeToFile(number_of_iterations);
                write_cylinder_acceleration.writeToFile(number_of_iterations);
                write_total_viscous_force_on_cylinder.writeToFile(number_of_iterations);
                write_total_pressure_force_on_cylinder.writeToFile(number_of_iterations);
                write_cylinder_mechanical_energy.writeToFile(number_of_iterations);
            }

            number_of_iterations++;

            // Particle sorting for better performance
            if (number_of_iterations % 100 == 0)
            {
                particle_sorting.exec();
            }

            // Update configurations
            water_block.updateCellLinkedList();
            cylinder.updateCellLinkedList();
            water_block_complex.updateConfiguration();
            cylinder_contact.updateConfiguration();
            cylinder_observer_contact.updateConfiguration();
        }

        // Output visualization data
        TickCount t2 = TickCount::now();
        body_states_recording.writeToFile();
        TickCount t3 = TickCount::now();
        interval += t3 - t2;
    }

    TickCount t4 = TickCount::now();
    TimeInterval tt = t4 - t1 - interval;

    std::cout << "========================================" << std::endl;
    std::cout << "Simulation completed!" << std::endl;
    std::cout << "Total wall time for computation: " << tt.seconds() << " seconds." << std::endl;
    std::cout << "========================================" << std::endl;

    return 0;
}
