def calculate_energy_efficiency(consumption_kwh, population):
    """
    Calculate energy consumption per capita (kWh per person).
    Used to measure how efficiently a smart city uses energy.

    Args:
        consumption_kwh (float): Total energy consumed in kilowatt-hours.
        population (int): Number of residents in the city zone.

    Returns:
        float: Energy used per person (kWh/person).

    Raises:
        ValueError: If population is zero or negative.
    """
    if population <= 0:
        raise ValueError("Population must be greater than zero.")
    return round(consumption_kwh / population, 2)


def calculate_traffic_congestion_index(vehicles, road_capacity):
    """
    Calculate a simple traffic congestion index (0.0 to 1.0+).
    A value above 1.0 means the road is over capacity — gridlock!

    Args:
        vehicles (int): Number of vehicles currently on the road.
        road_capacity (int): Maximum vehicles the road can handle.

    Returns:
        float: Congestion index rounded to 2 decimal places.

    Raises:
        ValueError: If road_capacity is zero or negative.
    """
    if road_capacity <= 0:
        raise ValueError("Road capacity must be greater than zero.")
    return round(vehicles / road_capacity, 2)


def calculate_air_quality_index(pm25, pm10, no2):
    """
    Calculate air quality index based on pollution values.
    """
    if any(v < 0 for v in [pm25, pm10, no2]):
        raise ValueError("Pollution values cannot be negative.")

    score = round((pm25 * 0.5) + (pm10 * 0.3) + (no2 * 0.2), 1)

    if score <= 50:
        category = "Good"
    elif score <= 100:
        category = "Moderate"
    elif score <= 150:
        category = "Unhealthy for Sensitive Groups"
    else:
        category = "Unhealthy"

    return {"score": score, "category": category}


if __name__ == "__main__":
    energy = calculate_energy_efficiency(50000, 1000)
    print(f"Energy per capita: {energy} kWh/person")  # Expected: 50.0

    traffic = calculate_traffic_congestion_index(800, 1000)
    print(f"Congestion index: {traffic}")  # Expected: 0.8

    gridlock = calculate_traffic_congestion_index(1200, 1000)
    print(f"Gridlock scenario: {gridlock}")  # Expected: 1.2

    air = calculate_air_quality_index(40, 30, 20)
    print(f"Air quality: {air}")