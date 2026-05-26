# FastBox Logistics Simulation System

A complete Python-based logistics simulator designed to optimize delivery assignments using Object-Oriented Programming (OOP) and modular principles.

## 🚀 Overview

FastBox is a simulation engine that manages multiple warehouses, delivery agents, and packages. It calculates the most efficient delivery routes using Euclidean distance metrics and generates detailed performance reports.

## ✨ Features

- **Object-Oriented Design**: Clean separation of entities (Agents, Warehouses, Packages, Points).
- **Proximity-Based Assignment**: Automatically assigns packages to the nearest agent based on warehouse location.
- **Euclidean Distance Engine**: Precise calculation of travel distances across a 2D map.
- **Performance Reporting**: Generates `report.json` with distance and efficiency metrics.
- **CSV Export**: Automatically exports details of the top-performing agent.
- **Error Handling**: Robust JSON parsing and file management.

## 🛠️ Technical Requirements

- Python 3.x
- Modules: `json`, `math`, `csv`, `sys`, `unittest`

## 📂 Project Structure

- `fastbox.py`: Main simulation engine and logic.
- `data.json`: Configuration file for warehouses, agents, and packages.
- `test_fastbox.py`: Unit test suite for verifying core functionality.
- `report.json`: Generated summary of the simulation results.
- `best_agent.csv`: Detailed stats for the most efficient agent.

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Prajkad96/fastbox-delivery.git
   ```
2. Run the simulation:
   ```bash
   python fastbox.py
   ```
3. (Optional) Run tests:
   ```bash
   python test_fastbox.py
   ```

## 📊 Logic Explanation

1. **Loading**: Data is parsed from `data.json` into specialized Python objects.
2. **Assignment**: For each package, the system finds the agent whose current location is closest to the package's starting warehouse.
3. **Simulation**: Agents move from their location to the warehouse, then to the destination, accumulating distance.
4. **Efficiency**: Efficiency is calculated as `total_distance / packages_delivered`. Lower values indicate better performance.

---
*Developed for the Nexgensis Logistics Assignment.*
