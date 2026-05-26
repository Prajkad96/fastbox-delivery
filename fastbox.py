import json
import math
import random
import csv
import sys

# --- Configuration ---
INPUT_FILE = "data.json"
OUTPUT_JSON = "report.json"
OUTPUT_CSV = "best_agent.csv"

class Point:
    """Represents a coordinate (x, y) on a 2D map."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def distance_to(self, other):
        """Uses Euclidean distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __str__(self):
        return f"({self.x}, {self.y})"

class Warehouse:
    """Represents a warehouse location."""
    def __init__(self, id, location_point):
        self.id = id
        self.location = location_point

class Package:
    """Represents a package to be delivered."""
    def __init__(self, id, warehouse_id, destination_point):
        self.id = id
        self.warehouse_id = warehouse_id
        self.destination = destination_point
        self.assigned_agent = None

class Agent:
    """Represents a delivery agent."""
    def __init__(self, id, start_location):
        self.id = id
        self.location = start_location
        self.total_distance = 0.0
        self.packages_delivered = 0

    def move_to(self, target_point, label=""):
        """Moves agent to target, updates distance, and prints progress."""
        distance = self.location.distance_to(target_point)
        print(f"  [Move] Agent {self.id} moving to {label} at {target_point} (Distance: {distance:.2f})")
        
        # Track metrics
        self.total_distance += distance
        self.location = target_point

    @property
    def efficiency(self):
        """Efficiency = total distance / packages delivered (Lower is better)."""
        if self.packages_delivered == 0:
            return 0.0
        return self.total_distance / self.packages_delivered

class FastBoxSimulator:
    """Main logic for the logistics simulation."""
    def __init__(self):
        self.warehouses = {}
        self.agents = []
        self.packages = []

    def load_data(self, filename):
        """Loads data from JSON file with error handling."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            
            # 1. Parse Warehouses
            for w_id, coords in data.get('warehouses', {}).items():
                self.warehouses[w_id] = Warehouse(w_id, Point(coords[0], coords[1]))
            
            # 2. Parse Agents
            for a_id, coords in data.get('agents', {}).items():
                self.agents.append(Agent(a_id, Point(coords[0], coords[1])))
            
            # 3. Parse Packages
            for p in data.get('packages', []):
                dest = Point(p['destination'][0], p['destination'][1])
                self.packages.append(Package(p['id'], p['warehouse'], dest))
                
            print(f"Successfully loaded data from {filename}")
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {filename}")
            sys.exit(1)

    def assign_packages(self):
        """Assigns each package to the nearest agent based on warehouse location."""
        print("\n--- Assigning Packages ---")
        if not self.agents:
            print("Error: No agents available for assignment.")
            return

        for package in self.packages:
            warehouse = self.warehouses.get(package.warehouse_id)
            if not warehouse:
                continue
            
            # Find nearest agent using the distance to the warehouse
            nearest_agent = min(self.agents, key=lambda a: a.location.distance_to(warehouse.location))
            
            package.assigned_agent = nearest_agent
            print(f"Package {package.id} (at {warehouse.id}) assigned to Agent {nearest_agent.id}")

    def run_simulation(self):
        """Simulates the actual delivery process."""
        print("\n--- Starting Delivery Simulation ---")
        
        # Group tasks by agent
        for agent in self.agents:
            agent_packages = [p for p in self.packages if p.assigned_agent == agent]
            
            if not agent_packages:
                continue
                
            print(f"\nAgent {agent.id} is starting their route:")
            for pkg in agent_packages:
                warehouse = self.warehouses[pkg.warehouse_id]
                
                # Step 1: Move to Warehouse
                agent.move_to(warehouse.location, f"Warehouse {warehouse.id}")
                
                # Step 2: Move to Destination
                agent.move_to(pkg.destination, f"Destination for {pkg.id}")
                
                # Step 3: Complete Delivery
                agent.packages_delivered += 1
                print(f"  [Done] Package {pkg.id} delivered!")

    def generate_report(self):
        """Generates the final report and saves to JSON/CSV."""
        report = {}
        best_agent_id = None
        min_eff = float('inf')

        for agent in self.agents:
            efficiency = round(agent.efficiency, 2)
            report[agent.id] = {
                "packages_delivered": agent.packages_delivered,
                "total_distance": round(agent.total_distance, 2),
                "efficiency": efficiency
            }
            
            # Find best agent (non-zero deliveries and lowest efficiency)
            if agent.packages_delivered > 0 and efficiency < min_eff:
                min_eff = efficiency
                best_agent_id = agent.id

        report["best_agent"] = best_agent_id
        
        # Save to JSON
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"\nReport saved to {OUTPUT_JSON}")

        # Save Best Agent to CSV (Bonus)
        if best_agent_id:
            stats = report[best_agent_id]
            with open(OUTPUT_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Field", "Value"])
                writer.writerow(["Best Agent ID", best_agent_id])
                writer.writerow(["Efficiency", stats["efficiency"]])
            print(f"Top performer details exported to {OUTPUT_CSV}")

def main():
    print("FastBox Logistics Simulator - Submission Version")
    
    sim = FastBoxSimulator()
    sim.load_data(INPUT_FILE)
    sim.assign_packages()
    sim.run_simulation()
    sim.generate_report()
    
    print("\nSimulation complete. Thank you!")

if __name__ == "__main__":
    main()
