import requests

EVS_LIST_URL = "https://evs.eu-de.otc.t-systems.com/v2/{project_id}/cloudvolumes/detail"


def list_evs_volumes(project_id, token, domain_id):
    """List EVS volumes"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            EVS_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            volumes = response.json().get("volumes", [])
            evs_report = []
            
            for volume in volumes:
                volume_id = volume.get("id", "Unknown")
                volume_name = volume.get("name", "Unknown")
                size = volume.get("size", 0)
                status = volume.get("status", "Unknown")
                volume_type = volume.get("volume_type", "Unknown")
                created = volume.get("created_at", "Unknown")
                
                evs_report.append({
                    "id": volume_id,
                    "name": volume_name,
                    "size": f"{size} GB",
                    "type": volume_type,
                    "status": status,
                    "created": created
                })
            
            print(f"✅ Found {len(evs_report)} EVS volumes")
            return evs_report
        else:
            print(f"Failed to list EVS volumes: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing EVS volumes: {str(e)}")
        return []