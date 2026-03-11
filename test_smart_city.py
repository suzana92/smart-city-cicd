import unittest
from smart_city import calculate_energy_efficiency, calculate_traffic_congestion_index


class TestEnergyEfficiency(unittest.TestCase):
    """Tests for the calculate_energy_efficiency function."""

    def test_normal_calculation(self):
        # 50,000 kWh shared across 1,000 people = 50 kWh/person
        result = calculate_energy_efficiency(50000, 1000)
        self.assertEqual(result, 50.0)

    def test_small_city(self):
        # Smaller zone: 200 kWh, 4 people = 50.0 kWh/person
        result = calculate_energy_efficiency(200, 4)
        self.assertEqual(result, 50.0)

    def test_rounding(self):
        # 100 kWh / 3 people = 33.333... → should round to 33.33
        result = calculate_energy_efficiency(100, 3)
        self.assertEqual(result, 33.33)

    def test_zero_population_raises_error(self):
        # A city with zero people should raise a ValueError
        with self.assertRaises(ValueError):
            calculate_energy_efficiency(5000, 0)

    def test_negative_population_raises_error(self):
        # Negative population is physically impossible
        with self.assertRaises(ValueError):
            calculate_energy_efficiency(5000, -100)


class TestTrafficCongestion(unittest.TestCase):
    """Tests for the calculate_traffic_congestion_index function."""

    def test_light_traffic(self):
        # 400 vehicles on a 1000-capacity road = 0.4 (light traffic)
        result = calculate_traffic_congestion_index(400, 1000)
        self.assertEqual(result, 0.4)

    def test_full_capacity(self):
        # 1000 vehicles on a 1000-capacity road = exactly 1.0
        result = calculate_traffic_congestion_index(1000, 1000)
        self.assertEqual(result, 1.0)

    def test_over_capacity_gridlock(self):
        # 1500 vehicles on a 1000-capacity road = 1.5 (gridlock!)
        result = calculate_traffic_congestion_index(1500, 1000)
        self.assertEqual(result, 1.5)

    def test_empty_road(self):
        # No vehicles at all = 0.0 (perfectly clear road)
        result = calculate_traffic_congestion_index(0, 1000)
        self.assertEqual(result, 0.0)

    def test_zero_capacity_raises_error(self):
        # A road with zero capacity makes no sense — expect ValueError
        with self.assertRaises(ValueError):
            calculate_traffic_congestion_index(500, 0)


# ── Entry point ───────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main()
