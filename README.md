# Delivery System Assignment

A logistics simulator for FastBox company. Simulates one day of operations by assigning packages to the nearest delivery agent, simulating deliveries, and generating a performance report.

## Approach
1. **Normalization:** The system gracefully handles both list-based arrays (like `base_case.json`) and object-based maps (like `test_case_1.json`) for input data structures, ensuring robust parsing.
2. **Assignment:** Agents are assigned packages based on the Euclidean distance from their *initial* location to the package's starting warehouse.
3. **Simulation:** The simulator tracks cumulative distances as agents pick up packages from warehouses and drop them off at their final destinations.
4. **Efficiency Metrics:** Determines the `best_agent` by calculating `total_distance / packages_delivered`. Agents with 0 deliveries are safely excluded from this calculation.

## Requirements
- Python 3.x
- No external libraries required (uses only standard library).

## How to Run
Run the program by passing the input JSON file as an argument:
```bash
python src/delivery_system.py data/base_case.json
```

You can also specify a custom output file path:
```bash
python src/delivery_system.py data/test_case_1.json custom_report.json
```

## Input Format
The program accepts a JSON file containing `warehouses`, `agents`, and `packages`.
(See `data/base_case.json` for structure details)

## Output Format
The program generates a `report.json` containing each agent's stats and the best agent overall.