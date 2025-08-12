import requests

CCE_CLUSTER_LIST_URL = "https://cce.eu-de.otc.t-systems.com/api/v3/projects/{project_id}/clusters"
CCE_NODE_LIST_URL = "https://cce.eu-de.otc.t-systems.com/api/v3/projects/{project_id}/clusters/{cluster_id}/nodes"


def list_cce_clusters(project_id, token, domain_id):
    """List CCE clusters and their nodes"""
    headers = {"X-Auth-Token": token}
    
    try:
        # Get CCE clusters
        response = requests.get(
            CCE_CLUSTER_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            clusters = response.json().get("items", [])
            cce_report = []
            
            for cluster in clusters:
                metadata = cluster.get("metadata", {})
                spec = cluster.get("spec", {})
                status = cluster.get("status", {})
                
                cluster_id = metadata.get("uid", "Unknown")
                cluster_name = metadata.get("name", "Unknown")
                cluster_status = status.get("phase", "Unknown")
                cluster_version = spec.get("version", "Unknown")
                cluster_type = spec.get("type", "Unknown")
                created = metadata.get("creationTimestamp", "Unknown")
                
                # Try to get node count for this cluster
                node_count = 0
                try:
                    node_response = requests.get(
                        CCE_NODE_LIST_URL.format(project_id=project_id, cluster_id=cluster_id),
                        headers=headers,
                        timeout=10
                    )
                    if node_response.status_code == 200:
                        nodes = node_response.json().get("items", [])
                        node_count = len(nodes)
                except Exception:
                    pass
                
                cce_report.append({
                    "id": cluster_id,
                    "name": cluster_name,
                    "type": cluster_type,
                    "version": cluster_version,
                    "status": cluster_status,
                    "node_count": node_count,
                    "created": created
                })
            
            print(f"✅ Found {len(cce_report)} CCE clusters")
            return cce_report
        else:
            print(f"Failed to list CCE clusters: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing CCE clusters: {str(e)}")
        return []