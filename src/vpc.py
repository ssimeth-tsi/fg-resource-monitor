import requests

VPC_LIST_URL = "https://vpc.eu-de.otc.t-systems.com/v1/{project_id}/vpcs"
SUBNET_LIST_URL = "https://vpc.eu-de.otc.t-systems.com/v1/{project_id}/subnets"


def list_vpcs(project_id, token, domain_id):
    """List VPCs"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            VPC_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            vpcs = response.json().get("vpcs", [])
            vpc_report = []
            
            for vpc in vpcs:
                vpc_id = vpc.get("id", "Unknown")
                vpc_name = vpc.get("name", "Unknown")
                cidr = vpc.get("cidr", "Unknown")
                status = vpc.get("status", "Unknown")
                
                vpc_report.append({
                    "id": vpc_id,
                    "name": vpc_name,
                    "cidr": cidr,
                    "status": status
                })
            
            print(f"✅ Found {len(vpc_report)} VPCs")
            return vpc_report
        else:
            print(f"Failed to list VPCs: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing VPCs: {str(e)}")
        return []


def list_subnets(project_id, token, domain_id):
    """List Subnets"""
    headers = {"X-Auth-Token": token}
    
    try:
        response = requests.get(
            SUBNET_LIST_URL.format(project_id=project_id),
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            subnets = response.json().get("subnets", [])
            subnet_report = []
            
            for subnet in subnets:
                subnet_id = subnet.get("id", "Unknown")
                subnet_name = subnet.get("name", "Unknown")
                cidr = subnet.get("cidr", "Unknown")
                vpc_id = subnet.get("vpc_id", "Unknown")
                status = subnet.get("status", "Unknown")
                
                subnet_report.append({
                    "id": subnet_id,
                    "name": subnet_name,
                    "cidr": cidr,
                    "vpc_id": vpc_id,
                    "status": status
                })
            
            print(f"✅ Found {len(subnet_report)} Subnets")
            return subnet_report
        else:
            print(f"Failed to list Subnets: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing Subnets: {str(e)}")
        return []