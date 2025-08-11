#!/usr/bin/env python3
"""
OTC Resource Monitor - Main Handler for FunctionGraph
Monitors all resources in OTC domain and sends email reports with creator information
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from auth import get_token, get_project_id, get_domain_id
from ecs import list_ecs_instances
from rds import list_rds_instances
from obs import list_obs_buckets
from evs import list_evs_volumes
from vpc import list_vpcs, list_subnets
from report import generate_html_report, send_email_report


def handler(event, context):
    """
    FunctionGraph entry point
    
    Args:
        event: Event data from FunctionGraph trigger
        context: FunctionGraph context object with runtime information
    
    Returns:
        dict: Response with status and resource counts
    """
    try:
        print("🚀 Starting OTC Resource Monitor")
        print("-" * 50)
        
        # Get authentication and IDs from FunctionGraph context
        print("🔐 Obtaining authentication from FunctionGraph context...")
        token = get_token(context)
        project_id = get_project_id(context)
        domain_id = get_domain_id(context)
        print("-" * 50)
        
        # Initialize resource collection
        all_resources = {}
        
        # Collect resources from each service
        print("📊 Starting resource collection...")
        
        # ECS Instances
        print("\n📍 Collecting ECS instances...")
        try:
            all_resources['ecs'] = list_ecs_instances(project_id, token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting ECS instances: {str(e)}")
            all_resources['ecs'] = []
        
        # RDS Instances
        print("\n📍 Collecting RDS instances...")
        try:
            all_resources['rds'] = list_rds_instances(project_id, token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting RDS instances: {str(e)}")
            all_resources['rds'] = []
        
        # OBS Buckets
        print("\n📍 Collecting OBS buckets...")
        try:
            all_resources['obs'] = list_obs_buckets(token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting OBS buckets: {str(e)}")
            all_resources['obs'] = []
        
        # EVS Volumes
        print("\n📍 Collecting EVS volumes...")
        try:
            all_resources['evs'] = list_evs_volumes(project_id, token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting EVS volumes: {str(e)}")
            all_resources['evs'] = []
        
        # VPCs
        print("\n📍 Collecting VPCs...")
        try:
            all_resources['vpc'] = list_vpcs(project_id, token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting VPCs: {str(e)}")
            all_resources['vpc'] = []
        
        # Subnets
        print("\n📍 Collecting Subnets...")
        try:
            all_resources['subnet'] = list_subnets(project_id, token, domain_id)
        except Exception as e:
            print(f"⚠️ Error collecting Subnets: {str(e)}")
            all_resources['subnet'] = []
        
        print("-" * 50)
        
        # Generate and send report
        print("\n📝 Generating HTML report...")
        html_report = generate_html_report(all_resources)
        print("✅ HTML report generated successfully")
        
        print("\n📧 Sending email report via SMN...")
        success = send_email_report(html_report, project_id, token)
        
        # Prepare response
        resource_counts = {
            "ecs": len(all_resources.get('ecs', [])),
            "rds": len(all_resources.get('rds', [])),
            "obs": len(all_resources.get('obs', [])),
            "evs": len(all_resources.get('evs', [])),
            "vpc": len(all_resources.get('vpc', [])),
            "subnet": len(all_resources.get('subnet', []))
        }
        
        total_resources = sum(resource_counts.values())
        
        print("-" * 50)
        print(f"\n📊 Resource Summary:")
        print(f"   Total resources found: {total_resources}")
        for resource_type, count in resource_counts.items():
            if count > 0:
                print(f"   - {resource_type.upper()}: {count}")
        
        if success:
            print("\n✅ ✅ ✅ Resource monitor completed successfully!")
            return {
                "statusCode": 200,
                "message": "Resource report sent successfully!",
                "resources_found": resource_counts,
                "total_resources": total_resources
            }
        else:
            print("\n⚠️ Resource collection completed but email sending failed")
            return {
                "statusCode": 500,
                "message": "Resource collection completed but failed to send email report",
                "resources_found": resource_counts,
                "total_resources": total_resources
            }
            
    except Exception as e:
        error_msg = f"Error in resource monitor: {str(e)}"
        print(f"\n❌ {error_msg}")
        return {
            "statusCode": 500,
            "message": error_msg,
            "error": str(e)
        }