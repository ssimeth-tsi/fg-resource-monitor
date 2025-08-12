import requests

APIG_INSTANCE_LIST_URL = "https://apig.eu-de.otc.t-systems.com/v2/{project_id}/apigw/instances"
APIG_API_LIST_URL = "https://apig.eu-de.otc.t-systems.com/v2/{project_id}/apigw/instances/{instance_id}/apis"


def list_apig_instances(project_id, token, domain_id):
    """List API Gateway instances and their APIs"""
    headers = {"X-Auth-Token": token}
    
    try:
        # Get APIG instances
        response = requests.get(
            APIG_INSTANCE_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            instances = response.json().get("instances", [])
            apig_report = []
            
            for instance in instances:
                instance_id = instance.get("id", "Unknown")
                instance_name = instance.get("instance_name", "Unknown")
                status = instance.get("status", "Unknown")
                spec = instance.get("spec", "Unknown")
                
                # Convert timestamp to readable date
                created = instance.get("create_time", "")
                if created and str(created).isdigit():
                    from datetime import datetime
                    created = datetime.fromtimestamp(int(created) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                elif not created:
                    created = "Unknown"
                
                # Try to get API count for this instance
                api_count = 0
                try:
                    api_response = requests.get(
                        APIG_API_LIST_URL.format(project_id=project_id, instance_id=instance_id),
                        headers=headers,
                        timeout=10
                    )
                    if api_response.status_code == 200:
                        apis = api_response.json().get("apis", [])
                        api_count = len(apis)
                except Exception:
                    pass
                
                apig_report.append({
                    "id": instance_id,
                    "name": instance_name,
                    "spec": spec,
                    "status": status,
                    "api_count": api_count,
                    "created": created
                })
            
            print(f"✅ Found {len(apig_report)} API Gateway instances")
            return apig_report
        else:
            print(f"Failed to list API Gateway instances: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing API Gateway instances: {str(e)}")
        return []