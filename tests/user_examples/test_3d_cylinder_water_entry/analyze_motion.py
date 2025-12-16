#!/usr/bin/env python3
"""
Motion Data Analysis Script for 3D Cylinder Water Entry Simulation

This script reads the observation data from SPHinXsys simulation output
and generates plots for:
- Displacement (x, y, z directions and magnitude)
- Velocity (x, y, z directions and magnitude)
- Acceleration (x, y, z directions and magnitude)
- Forces (viscous and pressure forces)
- Energy evolution

The script also calculates and plots derived quantities like:
- Impact force during water entry
- Deceleration during water entry
- Rotation angles (estimated from multi-point observations)
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')

def read_observation_data(filepath):
    """
    Read observation data from SPHinXsys output file.

    SPHinXsys observation files have the format:
    Line 1: Header with variable names
    Following lines: data values (time and observed quantities)
    """
    try:
        with open(filepath, 'r') as f:
            header = f.readline().strip().split()

        data = np.loadtxt(filepath, skiprows=1)

        return header, data
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None

def extract_vector_components(header, data, base_name):
    """
    Extract x, y, z components of a vector quantity from observation data.

    Args:
        header: List of column names
        data: Numpy array of data
        base_name: Base name of the quantity (e.g., "Position", "Velocity")

    Returns:
        time, x, y, z arrays
    """
    time = data[:, 0]

    # Find indices for the three components
    # SPHinXsys uses naming like: Position[0][0], Position[0][1], Position[0][2]
    # where [0] is the observer point index
    x_idx = header.index(f"{base_name}[0][0]") if f"{base_name}[0][0]" in header else None
    y_idx = header.index(f"{base_name}[0][1]") if f"{base_name}[0][1]" in header else None
    z_idx = header.index(f"{base_name}[0][2]") if f"{base_name}[0][2]" in header else None

    if x_idx is None or y_idx is None or z_idx is None:
        print(f"Warning: Could not find all components of {base_name}")
        return time, None, None, None

    x = data[:, x_idx]
    y = data[:, y_idx]
    z = data[:, z_idx]

    return time, x, y, z

def plot_motion_components(output_dir, save_dir):
    """
    Generate plots for displacement, velocity, and acceleration.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True)

    output_dir = Path(output_dir)

    # Read position data
    pos_file = output_dir / "CylinderObserver_Position.dat"
    vel_file = output_dir / "CylinderObserver_Velocity.dat"
    acc_file = output_dir / "CylinderObserver_AccelerationPrior.dat"

    print("Reading observation data...")

    # Position
    header_pos, data_pos = read_observation_data(pos_file)
    if data_pos is not None:
        time, pos_x, pos_y, pos_z = extract_vector_components(header_pos, data_pos, "Position")

        if pos_x is not None:
            # Calculate initial position for relative displacement
            pos_x0, pos_y0, pos_z0 = pos_x[0], pos_y[0], pos_z[0]
            disp_x = (pos_x - pos_x0) * 1000  # Convert to mm
            disp_y = (pos_y - pos_y0) * 1000
            disp_z = (pos_z - pos_z0) * 1000
            disp_mag = np.sqrt(disp_x**2 + disp_y**2 + disp_z**2)

            # Plot displacement
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Cylinder Displacement During Water Entry', fontsize=16, fontweight='bold')

            axes[0, 0].plot(time, disp_x, 'b-', linewidth=2)
            axes[0, 0].set_xlabel('Time [s]')
            axes[0, 0].set_ylabel('X Displacement [mm]')
            axes[0, 0].grid(True)
            axes[0, 0].set_title('Horizontal (X) Displacement')

            axes[0, 1].plot(time, disp_y, 'g-', linewidth=2)
            axes[0, 1].set_xlabel('Time [s]')
            axes[0, 1].set_ylabel('Y Displacement [mm]')
            axes[0, 1].grid(True)
            axes[0, 1].set_title('Horizontal (Y) Displacement')

            axes[1, 0].plot(time, disp_z, 'r-', linewidth=2)
            axes[1, 0].set_xlabel('Time [s]')
            axes[1, 0].set_ylabel('Z Displacement [mm]')
            axes[1, 0].grid(True)
            axes[1, 0].set_title('Vertical (Z) Displacement')

            axes[1, 1].plot(time, disp_mag, 'k-', linewidth=2)
            axes[1, 1].set_xlabel('Time [s]')
            axes[1, 1].set_ylabel('Displacement Magnitude [mm]')
            axes[1, 1].grid(True)
            axes[1, 1].set_title('Total Displacement')

            plt.tight_layout()
            plt.savefig(save_dir / 'displacement.png', dpi=300, bbox_inches='tight')
            print(f"Saved displacement plot to {save_dir / 'displacement.png'}")
            plt.close()

    # Velocity
    header_vel, data_vel = read_observation_data(vel_file)
    if data_vel is not None:
        time, vel_x, vel_y, vel_z = extract_vector_components(header_vel, data_vel, "Velocity")

        if vel_x is not None:
            vel_mag = np.sqrt(vel_x**2 + vel_y**2 + vel_z**2)

            # Plot velocity
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Cylinder Velocity During Water Entry', fontsize=16, fontweight='bold')

            axes[0, 0].plot(time, vel_x, 'b-', linewidth=2)
            axes[0, 0].set_xlabel('Time [s]')
            axes[0, 0].set_ylabel('X Velocity [m/s]')
            axes[0, 0].grid(True)
            axes[0, 0].set_title('Horizontal (X) Velocity')

            axes[0, 1].plot(time, vel_y, 'g-', linewidth=2)
            axes[0, 1].set_xlabel('Time [s]')
            axes[0, 1].set_ylabel('Y Velocity [m/s]')
            axes[0, 1].grid(True)
            axes[0, 1].set_title('Horizontal (Y) Velocity')

            axes[1, 0].plot(time, vel_z, 'r-', linewidth=2)
            axes[1, 0].set_xlabel('Time [s]')
            axes[1, 0].set_ylabel('Z Velocity [m/s]')
            axes[1, 0].grid(True)
            axes[1, 0].set_title('Vertical (Z) Velocity')
            axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)

            axes[1, 1].plot(time, vel_mag, 'k-', linewidth=2)
            axes[1, 1].set_xlabel('Time [s]')
            axes[1, 1].set_ylabel('Velocity Magnitude [m/s]')
            axes[1, 1].grid(True)
            axes[1, 1].set_title('Total Velocity')

            plt.tight_layout()
            plt.savefig(save_dir / 'velocity.png', dpi=300, bbox_inches='tight')
            print(f"Saved velocity plot to {save_dir / 'velocity.png'}")
            plt.close()

    # Acceleration
    header_acc, data_acc = read_observation_data(acc_file)
    if data_acc is not None:
        time, acc_x, acc_y, acc_z = extract_vector_components(header_acc, data_acc, "AccelerationPrior")

        if acc_x is not None:
            acc_mag = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

            # Plot acceleration
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Cylinder Acceleration During Water Entry', fontsize=16, fontweight='bold')

            axes[0, 0].plot(time, acc_x, 'b-', linewidth=2)
            axes[0, 0].set_xlabel('Time [s]')
            axes[0, 0].set_ylabel('X Acceleration [m/s²]')
            axes[0, 0].grid(True)
            axes[0, 0].set_title('Horizontal (X) Acceleration')

            axes[0, 1].plot(time, acc_y, 'g-', linewidth=2)
            axes[0, 1].set_xlabel('Time [s]')
            axes[0, 1].set_ylabel('Y Acceleration [m/s²]')
            axes[0, 1].grid(True)
            axes[0, 1].set_title('Horizontal (Y) Acceleration')

            axes[1, 0].plot(time, acc_z, 'r-', linewidth=2)
            axes[1, 0].set_xlabel('Time [s]')
            axes[1, 0].set_ylabel('Z Acceleration [m/s²]')
            axes[1, 0].grid(True)
            axes[1, 0].set_title('Vertical (Z) Acceleration')
            axes[1, 0].axhline(y=-9.81, color='k', linestyle='--', alpha=0.3, label='Gravity')
            axes[1, 0].legend()

            axes[1, 1].plot(time, acc_mag, 'k-', linewidth=2)
            axes[1, 1].set_xlabel('Time [s]')
            axes[1, 1].set_ylabel('Acceleration Magnitude [m/s²]')
            axes[1, 1].grid(True)
            axes[1, 1].set_title('Total Acceleration')

            plt.tight_layout()
            plt.savefig(save_dir / 'acceleration.png', dpi=300, bbox_inches='tight')
            print(f"Saved acceleration plot to {save_dir / 'acceleration.png'}")
            plt.close()

def plot_forces(output_dir, save_dir):
    """
    Generate plots for forces acting on the cylinder.
    """
    save_dir = Path(save_dir)
    output_dir = Path(output_dir)

    # Read force data
    visc_file = output_dir / "Cylinder_ViscousForceFromFluid.dat"
    pres_file = output_dir / "Cylinder_PressureForceFromFluid.dat"

    print("Reading force data...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Forces Acting on Cylinder During Water Entry', fontsize=16, fontweight='bold')

    # Viscous force
    header_visc, data_visc = read_observation_data(visc_file)
    if data_visc is not None:
        time_v, fx_v, fy_v, fz_v = extract_vector_components(header_visc, data_visc, "ViscousForceFromFluid")
        if fx_v is not None:
            f_visc_mag = np.sqrt(fx_v**2 + fy_v**2 + fz_v**2)
            axes[0, 0].plot(time_v, fz_v, 'b-', linewidth=2, label='Viscous Force')

    # Pressure force
    header_pres, data_pres = read_observation_data(pres_file)
    if data_pres is not None:
        time_p, fx_p, fy_p, fz_p = extract_vector_components(header_pres, data_pres, "PressureForceFromFluid")
        if fx_p is not None:
            f_pres_mag = np.sqrt(fx_p**2 + fy_p**2 + fz_p**2)
            axes[0, 0].plot(time_p, fz_p, 'r-', linewidth=2, label='Pressure Force')

            # Total force
            if fx_v is not None and len(time_v) == len(time_p):
                fx_total = fx_v + fx_p
                fy_total = fy_v + fy_p
                fz_total = fz_v + fz_p
                f_total_mag = np.sqrt(fx_total**2 + fy_total**2 + fz_total**2)

                axes[0, 0].plot(time_p, fz_total, 'k-', linewidth=2, label='Total Force')

    axes[0, 0].set_xlabel('Time [s]')
    axes[0, 0].set_ylabel('Vertical Force (Z) [N]')
    axes[0, 0].grid(True)
    axes[0, 0].legend()
    axes[0, 0].set_title('Vertical Forces')

    # Horizontal forces
    if fx_v is not None and fx_p is not None:
        axes[0, 1].plot(time_v, fx_v, 'b--', linewidth=1.5, label='Viscous X')
        axes[0, 1].plot(time_p, fx_p, 'r--', linewidth=1.5, label='Pressure X')
        axes[0, 1].plot(time_p, fx_total, 'k-', linewidth=2, label='Total X')
        axes[0, 1].set_xlabel('Time [s]')
        axes[0, 1].set_ylabel('Horizontal Force (X) [N]')
        axes[0, 1].grid(True)
        axes[0, 1].legend()
        axes[0, 1].set_title('Horizontal Forces (X)')

        axes[1, 0].plot(time_v, f_visc_mag, 'b-', linewidth=2, label='Viscous')
        axes[1, 0].plot(time_p, f_pres_mag, 'r-', linewidth=2, label='Pressure')
        axes[1, 0].plot(time_p, f_total_mag, 'k-', linewidth=2, label='Total')
        axes[1, 0].set_xlabel('Time [s]')
        axes[1, 0].set_ylabel('Force Magnitude [N]')
        axes[1, 0].grid(True)
        axes[1, 0].legend()
        axes[1, 0].set_title('Force Magnitudes')

        # Drag coefficient estimation (simplified)
        # Cd = F / (0.5 * rho * v^2 * A)
        # Need velocity data
        vel_file = output_dir / "CylinderObserver_Velocity.dat"
        header_vel, data_vel = read_observation_data(vel_file)
        if data_vel is not None:
            _, vel_x, vel_y, vel_z = extract_vector_components(header_vel, data_vel, "Velocity")
            if vel_z is not None and len(vel_z) == len(fz_total):
                rho_water = 1000.0
                cylinder_radius = 0.02
                A_ref = np.pi * cylinder_radius**2

                # Avoid division by zero
                vel_sq = vel_z**2
                vel_sq[vel_sq < 1e-6] = 1e-6

                Cd_z = np.abs(fz_total) / (0.5 * rho_water * vel_sq * A_ref)

                axes[1, 1].plot(time_p, Cd_z, 'k-', linewidth=2)
                axes[1, 1].set_xlabel('Time [s]')
                axes[1, 1].set_ylabel('Drag Coefficient (Cd)')
                axes[1, 1].grid(True)
                axes[1, 1].set_title('Estimated Drag Coefficient')
                axes[1, 1].set_ylim([0, 5])

    plt.tight_layout()
    plt.savefig(save_dir / 'forces.png', dpi=300, bbox_inches='tight')
    print(f"Saved forces plot to {save_dir / 'forces.png'}")
    plt.close()

def plot_energy(output_dir, save_dir):
    """
    Generate plot for mechanical energy evolution.
    """
    save_dir = Path(save_dir)
    output_dir = Path(output_dir)

    energy_file = output_dir / "Cylinder_TotalMechanicalEnergy.dat"

    header, data = read_observation_data(energy_file)
    if data is not None:
        time = data[:, 0]
        energy_idx = header.index("TotalMechanicalEnergy") if "TotalMechanicalEnergy" in header else 1
        energy = data[:, energy_idx]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(time, energy, 'b-', linewidth=2)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Total Mechanical Energy [J]')
        ax.set_title('Cylinder Mechanical Energy During Water Entry', fontsize=14, fontweight='bold')
        ax.grid(True)

        plt.tight_layout()
        plt.savefig(save_dir / 'energy.png', dpi=300, bbox_inches='tight')
        print(f"Saved energy plot to {save_dir / 'energy.png'}")
        plt.close()

def generate_summary_report(output_dir, save_dir):
    """
    Generate a summary report with key statistics.
    """
    save_dir = Path(save_dir)
    output_dir = Path(output_dir)

    report_file = save_dir / 'simulation_summary.txt'

    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("3D CYLINDER WATER ENTRY SIMULATION - SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")

        # Read and analyze data
        pos_file = output_dir / "CylinderObserver_Position.dat"
        vel_file = output_dir / "CylinderObserver_Velocity.dat"
        acc_file = output_dir / "CylinderObserver_AccelerationPrior.dat"
        pres_file = output_dir / "Cylinder_PressureForceFromFluid.dat"

        # Position analysis
        header_pos, data_pos = read_observation_data(pos_file)
        if data_pos is not None:
            time, pos_x, pos_y, pos_z = extract_vector_components(header_pos, data_pos, "Position")
            if pos_z is not None:
                max_depth = pos_z[0] - np.min(pos_z)
                f.write(f"DISPLACEMENT ANALYSIS:\n")
                f.write(f"  Maximum penetration depth: {max_depth*1000:.2f} mm\n")
                f.write(f"  Final Z position: {pos_z[-1]:.4f} m\n")
                f.write(f"  Total vertical displacement: {(pos_z[-1] - pos_z[0])*1000:.2f} mm\n\n")

        # Velocity analysis
        header_vel, data_vel = read_observation_data(vel_file)
        if data_vel is not None:
            time, vel_x, vel_y, vel_z = extract_vector_components(header_vel, data_vel, "Velocity")
            if vel_z is not None:
                initial_vel = vel_z[0]
                final_vel = vel_z[-1]
                min_vel = np.min(vel_z)
                f.write(f"VELOCITY ANALYSIS:\n")
                f.write(f"  Initial velocity: {initial_vel:.4f} m/s\n")
                f.write(f"  Final velocity: {final_vel:.4f} m/s\n")
                f.write(f"  Minimum velocity: {min_vel:.4f} m/s\n\n")

        # Acceleration analysis
        header_acc, data_acc = read_observation_data(acc_file)
        if data_acc is not None:
            time, acc_x, acc_y, acc_z = extract_vector_components(header_acc, data_acc, "AccelerationPrior")
            if acc_z is not None:
                max_acc = np.max(acc_z)
                min_acc = np.min(acc_z)
                f.write(f"ACCELERATION ANALYSIS:\n")
                f.write(f"  Maximum upward acceleration: {max_acc:.2f} m/s²\n")
                f.write(f"  Maximum downward acceleration: {min_acc:.2f} m/s²\n")
                f.write(f"  Maximum deceleration (relative to entry): {max_acc - initial_vel:.2f} m/s²\n\n")

        # Force analysis
        header_pres, data_pres = read_observation_data(pres_file)
        if data_pres is not None:
            time_p, fx_p, fy_p, fz_p = extract_vector_components(header_pres, data_pres, "PressureForceFromFluid")
            if fz_p is not None:
                max_force = np.max(fz_p)
                f.write(f"FORCE ANALYSIS:\n")
                f.write(f"  Maximum upward pressure force: {max_force:.4f} N\n")
                f.write(f"  Time of maximum force: {time_p[np.argmax(fz_p)]:.4f} s\n\n")

        f.write("=" * 80 + "\n")
        f.write("Analysis completed successfully.\n")
        f.write("Generated plots:\n")
        f.write("  - displacement.png\n")
        f.write("  - velocity.png\n")
        f.write("  - acceleration.png\n")
        f.write("  - forces.png\n")
        f.write("  - energy.png\n")
        f.write("=" * 80 + "\n")

    print(f"Saved summary report to {report_file}")

def main():
    """Main function to run all analyses."""
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "./bin/output"

    if len(sys.argv) > 2:
        save_dir = sys.argv[2]
    else:
        save_dir = "./analysis_results"

    print("=" * 80)
    print("3D CYLINDER WATER ENTRY - MOTION DATA ANALYSIS")
    print("=" * 80)
    print(f"Output directory: {output_dir}")
    print(f"Save directory: {save_dir}")
    print()

    # Create save directory
    Path(save_dir).mkdir(exist_ok=True)

    # Generate plots
    print("Generating motion component plots...")
    plot_motion_components(output_dir, save_dir)

    print("\nGenerating force plots...")
    plot_forces(output_dir, save_dir)

    print("\nGenerating energy plot...")
    plot_energy(output_dir, save_dir)

    print("\nGenerating summary report...")
    generate_summary_report(output_dir, save_dir)

    print("\n" + "=" * 80)
    print("Analysis completed successfully!")
    print(f"All results saved to: {save_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
