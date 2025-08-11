import requests

RDS_LIST_URL = "https://rds.eu-de.otc.t-systems.com/v3/{project_id}/instances"


def list_rds_instances(project_id, token, domain_id):
    """List RDS instances"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            RDS_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            instances = response.json().get("instances", [])
            rds_report = []
            
            for instance in instances:
                instance_id = instance.get("id", "Unknown")
                instance_name = instance.get("name", "Unknown")
                engine = instance.get("datastore", {}).get("type", "Unknown")
                flavor_ref = instance.get("flavor_ref", "Unknown")
                status = instance.get("status", "Unknown")
                created = instance.get("created", "Unknown")
                
                rds_report.append({
                    "id": instance_id,
                    "name": instance_name,
                    "engine": engine,
                    "flavor": flavor_ref,
                    "status": status,
                    "created": created
                })
            
            print(f"✅ Found {len(rds_report)} RDS instances")
            return rds_report
        else:
            print(f"Failed to list RDS instances: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing RDS instances: {str(e)}")
        return []