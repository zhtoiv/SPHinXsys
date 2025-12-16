#!/bin/bash

##############################################################################
# Automated script to build, run, and analyze the 3D cylinder water entry
# simulation
##############################################################################

set -e  # Exit on error

echo "========================================================================"
echo "3D Cylinder Water Entry Simulation - Automated Build and Run"
echo "========================================================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_NAME="test_3d_cylinder_water_entry"

# Configuration
BUILD_DIR="${SCRIPT_DIR}/build"
NPROC=$(nproc 2>/dev/null || echo 4)

# Step 1: Build the project
echo ""
echo "Step 1: Building the project..."
echo "------------------------------------------------------------------------"

if [ -d "${BUILD_DIR}" ]; then
    echo "Build directory exists. Cleaning..."
    rm -rf "${BUILD_DIR}"
fi

mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

echo "Running CMake..."
cmake ..

echo "Compiling (using ${NPROC} cores)..."
make -j${NPROC}

if [ $? -eq 0 ]; then
    echo "✓ Build successful!"
else
    echo "✗ Build failed!"
    exit 1
fi

# Step 2: Run the simulation
echo ""
echo "Step 2: Running the simulation..."
echo "------------------------------------------------------------------------"

cd bin

if [ -f "./${PROJECT_NAME}" ]; then
    echo "Starting simulation..."
    echo ""
    ./${PROJECT_NAME}

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Simulation completed successfully!"
    else
        echo ""
        echo "✗ Simulation failed!"
        exit 1
    fi
else
    echo "✗ Executable not found: ./${PROJECT_NAME}"
    exit 1
fi

# Step 3: Analyze results
echo ""
echo "Step 3: Analyzing results..."
echo "------------------------------------------------------------------------"

if [ -d "./output" ]; then
    echo "Output directory found. Running analysis script..."

    # Check if Python is available
    if command -v python3 &> /dev/null; then
        mkdir -p analysis_results
        python3 ../../analyze_motion.py ./output ./analysis_results

        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ Analysis completed successfully!"
            echo "  Results saved to: ${BUILD_DIR}/bin/analysis_results/"
        else
            echo ""
            echo "⚠ Analysis script encountered errors"
            echo "  You can run it manually: python3 ../analyze_motion.py ./output ./analysis_results"
        fi
    else
        echo "⚠ Python3 not found. Skipping automatic analysis."
        echo "  Install Python3 and run: python3 ../analyze_motion.py ./output ./analysis_results"
    fi
else
    echo "⚠ Output directory not found. Simulation may not have completed successfully."
fi

# Step 4: Summary
echo ""
echo "========================================================================"
echo "Simulation Pipeline Completed!"
echo "========================================================================"
echo ""
echo "Output locations:"
echo "  - Executable: ${BUILD_DIR}/bin/${PROJECT_NAME}"
echo "  - VTP files (ParaView): ${BUILD_DIR}/bin/output/"
echo "  - Data files (DAT): ${BUILD_DIR}/bin/output/"
echo "  - Analysis results: ${BUILD_DIR}/bin/analysis_results/"
echo ""
echo "Next steps:"
echo "  1. View 3D visualization in ParaView:"
echo "     paraview ${BUILD_DIR}/bin/output/*.vtp"
echo ""
echo "  2. View analysis plots:"
echo "     cd ${BUILD_DIR}/bin/analysis_results/"
echo "     xdg-open displacement.png  # or your image viewer"
echo ""
echo "  3. Read the summary report:"
echo "     cat ${BUILD_DIR}/bin/analysis_results/simulation_summary.txt"
echo ""
echo "========================================================================"
