# Delivery System Assignment

A Python-based logistics simulator for a fictional delivery company called **FastBox**.

The system simulates one day of delivery operations by assigning packages to the nearest delivery agent, calculating delivery distances, tracking agent performance, and generating a final report.

## Approach

### 1. Data Normalization

The system supports both input formats provided in the assignment:

- List-based `warehouses` and `agents`
- Dictionary-based `warehouses` and `agents`

The data is normalized into a consistent internal structure before processing.

### 2. Package Assignment

Each package is assigned to the nearest delivery agent based on the **Euclidean distance between the agent's initial location and the package's warehouse**.

The Euclidean distance is calculated using:

```text
distance = √((x2 - x1)² + (y2 - y1)²)
