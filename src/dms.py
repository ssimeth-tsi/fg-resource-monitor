import requests

DMS_QUEUE_LIST_URL = "https://dms.eu-de.otc.t-systems.com/v2/{project_id}/queues"
DMS_KAFKA_LIST_URL = "https://dms.eu-de.otc.t-systems.com/v2/{project_id}/instances"


def list_dms_queues(project_id, token):
    """List DMS queues"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            DMS_QUEUE_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            queues = response.json().get("queues", [])
            queue_report = []
            
            for queue in queues:
                queue_report.append({
                    "id": queue.get("id", "Unknown"),
                    "name": queue.get("name", "Unknown"),
                    "type": "Queue",
                    "created": queue.get("created", "Unknown")
                })
            
            return queue_report
        else:
            return []
            
    except Exception:
        return []


def list_dms_kafka(project_id, token):
    """List DMS Kafka instances"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            DMS_KAFKA_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        print(f"DMS Kafka API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            instances = data.get("instances", [])
            print(f"Found {len(instances)} Kafka instances in API response")
            
            kafka_report = []
            
            for instance in instances:
                # Convert timestamp to readable date
                created_at = instance.get("created_at", instance.get("created", ""))
                if created_at and str(created_at).isdigit():
                    from datetime import datetime
                    created_at = datetime.fromtimestamp(int(created_at) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                
                kafka_report.append({
                    "id": instance.get("instance_id", "Unknown"),
                    "name": instance.get("name", "Unknown"),
                    "type": "Kafka",
                    "engine": instance.get("engine", "kafka"),
                    "engine_version": instance.get("engine_version", "Unknown"),
                    "status": instance.get("status", "Unknown"),
                    "created": created_at if created_at else "Unknown"
                })
            
            return kafka_report
        else:
            print(f"Failed to get Kafka instances: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error getting Kafka instances: {str(e)}")
        return []


def list_dms_resources(project_id, token, domain_id):
    """List all DMS resources (queues and Kafka)"""
    all_dms = []
    
    # Get queues
    print("Fetching DMS queues...")
    queues = list_dms_queues(project_id, token)
    all_dms.extend(queues)
    print(f"  - Found {len(queues)} DMS queues")
    
    # Get Kafka instances
    print("Fetching DMS Kafka instances...")
    kafka = list_dms_kafka(project_id, token)
    all_dms.extend(kafka)
    print(f"  - Found {len(kafka)} Kafka instances")
    
    print(f"✅ Found {len(all_dms)} DMS resources total")
    return all_dms