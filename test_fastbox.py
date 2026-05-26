import unittest
from fastbox import Point, Agent, Warehouse, Package, FastBoxSimulator

class TestFastBox(unittest.TestCase):
    def setUp(self):
        """Initialize common test objects."""
        self.p1 = Point(0, 0)
        self.p2 = Point(3, 4)  # 3-4-5 triangle
        self.agent = Agent("A1", self.p1)
        self.warehouse = Warehouse("W1", self.p1)
        self.package = Package("P1", "W1", self.p2)

    def test_distance_calculation(self):
        """Test Euclidean distance calculation."""
        self.assertEqual(self.p1.distance_to(self.p2), 5.0)

    def test_agent_movement(self):
        """Test agent movement and distance tracking."""
        self.agent.move_to(self.p2)
        self.assertEqual(self.agent.total_distance, 5.0)
        self.assertEqual(self.agent.location.x, 3)
        self.assertEqual(self.agent.location.y, 4)

    def test_agent_efficiency(self):
        """Test efficiency calculation."""
        self.agent.move_to(self.p2)
        self.agent.packages_delivered = 2
        # efficiency = 5.0 / 2 = 2.5
        self.assertEqual(self.agent.efficiency, 2.5)

    def test_simulation_assignment(self):
        """Test nearest agent assignment logic."""
        sim = FastBoxSimulator()
        sim.warehouses["W1"] = self.warehouse
        sim.agents = [
            Agent("Near", Point(1, 1)),
            Agent("Far", Point(10, 10))
        ]
        sim.packages = [self.package]
        
        sim.assign_packages()
        self.assertEqual(self.package.assigned_agent.id, "Near")

if __name__ == "__main__":
    unittest.main()
