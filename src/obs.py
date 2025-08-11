import requests
import xml.etree.ElementTree as ET

OBS_LIST_URL = "https://obs.eu-de.otc.t-systems.com"


def list_obs_buckets(token, domain_id):
    """List OBS buckets"""
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            OBS_LIST_URL,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 403:
            print("⚠️ No permission to list OBS buckets - skipping")
            return []
        
        if response.status_code == 200:
            buckets_report = []
            
            try:
                root_element = ET.fromstring(response.text)
                buckets = root_element.findall(".//{http://obs.otc.t-systems.com/doc/2006-03-01/}Bucket")
                
                for bucket in buckets:
                    bucket_name = bucket.find("{http://obs.otc.t-systems.com/doc/2006-03-01/}Name")
                    creation_date = bucket.find("{http://obs.otc.t-systems.com/doc/2006-03-01/}CreationDate")
                    
                    if bucket_name is not None:
                        buckets_report.append({
                            "name": bucket_name.text,
                            "created": creation_date.text if creation_date is not None else "Unknown"
                        })
                
                print(f"✅ Found {len(buckets_report)} OBS buckets")
            except ET.ParseError:
                print("Could not parse OBS response as XML")
            
            return buckets_report
        else:
            print(f"Failed to list OBS buckets: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error listing OBS buckets: {str(e)}")
        return []