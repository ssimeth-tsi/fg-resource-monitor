import requests

ECS_LIST_URL = "https://ecs.eu-de.otc.t-systems.com/v2/{project_id}/servers/detail"


def list_ecs_instances(project_id, token, domain_id):
    """List ECS instances"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            ECS_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            servers = response.json().get("servers", [])
            ecs_report = []
            
            for server in servers:
                server_id = server.get("id", "Unknown")
                server_name = server.get("name", "Unknown")
                flavor = server.get("flavor", {}).get("id", "Unknown")
                status = server.get("status", "Unknown")
                created = server.get("created", "Unknown")
                
                ecs_report.append({
                    "id": server_id,
                    "name": server_name,
                    "flavor": flavor,
                    "status": status,
                    "created": created
                })
            
            print(f"✅ Found {len(ecs_report)} ECS instances")
            return ecs_report
        else:
            print(f"Failed to list ECS instances: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing ECS instances: {str(e)}")
        return []