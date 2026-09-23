import json
import math
import sys

def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File {filepath} is not a valid JSON.")
        sys.exit(1)

def normalize_data(data):
    warehouses_dict = {}
    agents_dict = {}
    
    # Normalize warehouses
    warehouses_data = data.get('warehouses', [])
    if isinstance(warehouses_data, dict):
        warehouses_dict = warehouses_data
    else:
        for w in warehouses_data:
            warehouses_dict[w['id']] = w['location']
            
    # Normalize agents
    agents_data = data.get('agents', [])
    if isinstance(agents_data, dict):
        for a_id, loc in agents_data.items():
            agents_dict[a_id] = {
                'initial_location': loc,
                'current_location': loc,
                'total_distance': 0.0,
                'packages_delivered': 0,
                'assigned_packages': []
            }
    else:
        for a in agents_data:
            agents_dict[a['id']] = {
                'initial_location': a['location'],
                'current_location': a['location'],
                'total_distance': 0.0,
                'packages_delivered': 0,
                'assigned_packages': []
            }
            
    # Packages (List of dicts)
    packages_list = data.get('packages', [])
    
    return warehouses_dict, agents_dict, packages_list

def calculate_distance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def assign_packages(warehouses_dict, agents_dict, packages_list):
    for pkg in packages_list:
        # Check both possible keys for warehouse ID
        w_id = pkg.get('warehouse') or pkg.get('warehouse_id')
        if w_id not in warehouses_dict:
            print(f"Warning: Warehouse {w_id} not found. Skipping package {pkg.get('id')}.")
            continue
            
        w_loc = warehouses_dict[w_id]
        
        min_dist = float('inf')
        assigned_agent_id = None
        
        # We sort agent items by key to ensure deterministic tie-breaking (first agent alphabetically)
        for agent_id, agent_data in sorted(agents_dict.items()):
            dist = calculate_distance(agent_data['initial_location'], w_loc)
            if dist < min_dist:
                min_dist = dist
                assigned_agent_id = agent_id
                
        if assigned_agent_id:
            agents_dict[assigned_agent_id]['assigned_packages'].append(pkg)

def simulate_deliveries(warehouses_dict, agents_dict):
    for agent_id, agent_data in agents_dict.items():
        for pkg in agent_data['assigned_packages']:
            w_id = pkg.get('warehouse') or pkg.get('warehouse_id')
            w_loc = warehouses_dict[w_id]
            dest_loc = pkg['destination']
            
            # Leg 1: Current Location to Warehouse
            leg1 = calculate_distance(agent_data['current_location'], w_loc)
            # Leg 2: Warehouse to Destination
            leg2 = calculate_distance(w_loc, dest_loc)
            
            agent_data['total_distance'] += (leg1 + leg2)
            agent_data['current_location'] = dest_loc
            agent_data['packages_delivered'] += 1

def generate_report(agents_dict, output_filepath):
    report = {}
    best_agent = None
    best_efficiency = float('inf')
    
    for agent_id, agent_data in sorted(agents_dict.items()):
        pkgs_delivered = agent_data['packages_delivered']
        total_dist = agent_data['total_distance']
        
        if pkgs_delivered > 0:
            efficiency = total_dist / pkgs_delivered
            
            if efficiency < best_efficiency:
                best_efficiency = efficiency
                best_agent = agent_id
                
            report[agent_id] = {
                "packages_delivered": pkgs_delivered,
                "total_distance": round(total_dist, 2),
                "efficiency": round(efficiency, 2)
            }
        else:
            report[agent_id] = {
                "packages_delivered": 0,
                "total_distance": 0.0,
                "efficiency": None
            }
            
    report["best_agent"] = best_agent
    
    with open(output_filepath, 'w') as file:
        json.dump(report, file, indent=4)
        
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python delivery_system.py <path_to_data.json> [path_to_report.json]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'report.json'
    
    data = load_data(input_file)
    warehouses_dict, agents_dict, packages_list = normalize_data(data)
    
    assign_packages(warehouses_dict, agents_dict, packages_list)
    simulate_deliveries(warehouses_dict, agents_dict)
    
    report = generate_report(agents_dict, output_file)
    print(f"Report saved to {output_file}")
    
if __name__ == "__main__":
    main()
