import requests

DCS_LIST_URL = "https://dcs.eu-de.otc.t-systems.com/v2/{project_id}/instances"


def list_dcs_instances(project_id, token, domain_id):
    """List DCS (Redis/Memcached) instances"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            DCS_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            instances = response.json().get("instances", [])
            dcs_report = []
            
            for instance in instances:
                instance_id = instance.get("instance_id", "Unknown")
                instance_name = instance.get("name", "Unknown")
                engine = instance.get("engine", "Unknown")
                engine_version = instance.get("engine_version", "Unknown")
                capacity = instance.get("capacity", 0)
                status = instance.get("status", "Unknown")
                created = instance.get("created_at", "Unknown")
                
                # Determine instance type
                instance_type = "Redis" if "redis" in engine.lower() else "Memcached"
                
                dcs_report.append({
                    "id": instance_id,
                    "name": instance_name,
                    "type": instance_type,
                    "engine_version": engine_version,
                    "capacity": f"{capacity} GB",
                    "status": status,
                    "created": created
                })
            
            print(f"✅ Found {len(dcs_report)} DCS instances")
            return dcs_report
        else:
            print(f"Failed to list DCS instances: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing DCS instances: {str(e)}")
        return []