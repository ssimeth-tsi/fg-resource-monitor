import os
import requests
from datetime import datetime

SMN_PUBLISH_URL = "https://smn.eu-de.otc.t-systems.com/v2/{project_id}/notifications/topics/{topic_urn}/publish"


def generate_html_report(all_resources):
    """Generate a formatted HTML report of all resources"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
            h2 {{ color: #34495e; margin-top: 35px; border-bottom: 1px solid #ecf0f1; padding-bottom: 10px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px; text-align: left; font-weight: 600; }}
            td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
            tr:hover {{ background-color: #f8f9fa; }}
            tr:nth-child(even) {{ background-color: #fafbfc; }}
            .summary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .summary h3 {{ margin-top: 0; color: white; }}
            .summary ul {{ list-style: none; padding-left: 0; }}
            .summary li {{ padding: 5px 0; }}
            .summary strong {{ color: #ffd700; }}
            .status-active {{ color: #10b981; font-weight: 600; }}
            .status-error {{ color: #ef4444; font-weight: 600; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d; text-align: center; }}
            .no-data {{ text-align: center; padding: 20px; color: #95a5a6; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌐 OTC Resource Monitor Report</h1>
            <p><strong>📅 Generated:</strong> {current_time}</p>
            
            <div class="summary">
                <h3>📊 Resource Summary</h3>
                <ul>
                    <li>🔗 <strong>VPCs:</strong> {len(all_resources.get('vpc', []))}</li>
                    <li>🌐 <strong>Subnets:</strong> {len(all_resources.get('subnet', []))}</li>
                    <li>💻 <strong>ECS Instances:</strong> {len(all_resources.get('ecs', []))}</li>
                    <li>💾 <strong>EVS Volumes:</strong> {len(all_resources.get('evs', []))}</li>
                    <li>🗄️ <strong>RDS Instances:</strong> {len(all_resources.get('rds', []))}</li>
                    <li>📦 <strong>OBS Buckets:</strong> {len(all_resources.get('obs', []))}</li>
                    <li>📨 <strong>DMS Instances:</strong> {len(all_resources.get('dms', []))}</li>
                    <li>⚡ <strong>DCS Instances:</strong> {len(all_resources.get('dcs', []))}</li>
                    <li>🌉 <strong>APIG Instances:</strong> {len(all_resources.get('apig', []))}</li>
                    <li>☸️ <strong>CCE Clusters:</strong> {len(all_resources.get('cce', []))}</li>
                </ul>
                <p style="margin-top: 15px; font-size: 14px;">
                    <strong>Total Resources:</strong> {sum(len(v) for v in all_resources.values() if isinstance(v, list))}
                </p>
            </div>
    """
    
    # VPCs (first)
    if all_resources.get('vpc'):
        html += """
        <h2>🔗 VPCs</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>CIDR</th>
                <th>Status</th>
            </tr>
        """
        for vpc in all_resources['vpc']:
            html += f"""
            <tr>
                <td><strong>{vpc['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{vpc['id']}</td>
                <td>{vpc['cidr']}</td>
                <td>{vpc['status']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>🔗 VPCs</h2><p class="no-data">No VPCs found</p>'
    
    # Subnets (second)
    if all_resources.get('subnet'):
        html += """
        <h2>🌐 Subnets</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>CIDR</th>
                <th>VPC ID</th>
                <th>Status</th>
            </tr>
        """
        for subnet in all_resources['subnet']:
            html += f"""
            <tr>
                <td><strong>{subnet['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{subnet['id']}</td>
                <td>{subnet['cidr']}</td>
                <td style="font-size: 12px; color: #7f8c8d;">{subnet['vpc_id']}</td>
                <td>{subnet['status']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>🌐 Subnets</h2><p class="no-data">No Subnets found</p>'
    
    # ECS Instances
    if all_resources.get('ecs'):
        html += """
        <h2>💻 ECS Instances</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Flavor</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for ecs in all_resources['ecs']:
            status_class = 'status-active' if ecs['status'].upper() == 'ACTIVE' else 'status-error' if 'ERROR' in ecs['status'].upper() else ''
            html += f"""
            <tr>
                <td><strong>{ecs['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{ecs['id']}</td>
                <td>{ecs['flavor']}</td>
                <td class="{status_class}">{ecs['status']}</td>
                <td>{ecs['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>💻 ECS Instances</h2><p class="no-data">No ECS instances found</p>'
    
    # EVS Volumes (directly after ECS)
    if all_resources.get('evs'):
        html += """
        <h2>💾 EVS Volumes</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Size</th>
                <th>Type</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for evs in all_resources['evs']:
            html += f"""
            <tr>
                <td><strong>{evs['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{evs['id']}</td>
                <td>{evs['size']}</td>
                <td>{evs['type']}</td>
                <td>{evs['status']}</td>
                <td>{evs['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>💾 EVS Volumes</h2><p class="no-data">No EVS volumes found</p>'
    
    # RDS Instances
    if all_resources.get('rds'):
        html += """
        <h2>🗄️ RDS Instances</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Engine</th>
                <th>Flavor</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for rds in all_resources['rds']:
            html += f"""
            <tr>
                <td><strong>{rds['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{rds['id']}</td>
                <td>{rds['engine']}</td>
                <td>{rds['flavor']}</td>
                <td>{rds['status']}</td>
                <td>{rds['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>🗄️ RDS Instances</h2><p class="no-data">No RDS instances found</p>'
    
    # OBS Buckets
    if all_resources.get('obs'):
        html += """
        <h2>📦 OBS Buckets</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Created</th>
            </tr>
        """
        for bucket in all_resources['obs']:
            html += f"""
            <tr>
                <td><strong>{bucket['name']}</strong></td>
                <td>{bucket['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>📦 OBS Buckets</h2><p class="no-data">No OBS buckets found</p>'
    
    # DMS Instances
    if all_resources.get('dms'):
        html += """
        <h2>📨 DMS Instances</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Type</th>
                <th>Engine Version</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for dms in all_resources['dms']:
            html += f"""
            <tr>
                <td><strong>{dms.get('name', 'Unknown')}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{dms.get('id', 'Unknown')}</td>
                <td>{dms.get('type', 'Unknown')}</td>
                <td>{dms.get('engine_version', '-')}</td>
                <td>{dms.get('status', '-')}</td>
                <td>{dms.get('created', 'Unknown')}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>📨 DMS Instances</h2><p class="no-data">No DMS instances found</p>'
    
    # DCS Instances
    if all_resources.get('dcs'):
        html += """
        <h2>⚡ DCS Instances</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Type</th>
                <th>Version</th>
                <th>Capacity</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for dcs in all_resources['dcs']:
            html += f"""
            <tr>
                <td><strong>{dcs['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{dcs['id']}</td>
                <td>{dcs['type']}</td>
                <td>{dcs['engine_version']}</td>
                <td>{dcs['capacity']}</td>
                <td>{dcs['status']}</td>
                <td>{dcs['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>⚡ DCS Instances</h2><p class="no-data">No DCS instances found</p>'
    
    # APIG Instances
    if all_resources.get('apig'):
        html += """
        <h2>🌉 APIG Instances</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Spec</th>
                <th>APIs</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for apig in all_resources['apig']:
            html += f"""
            <tr>
                <td><strong>{apig['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{apig['id']}</td>
                <td>{apig['spec']}</td>
                <td>{apig['api_count']}</td>
                <td>{apig['status']}</td>
                <td>{apig['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>🌉 APIG Instances</h2><p class="no-data">No APIG instances found</p>'
    
    # CCE Clusters
    if all_resources.get('cce'):
        html += """
        <h2>☸️ CCE Clusters</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Type</th>
                <th>Version</th>
                <th>Nodes</th>
                <th>Status</th>
                <th>Created</th>
            </tr>
        """
        for cce in all_resources['cce']:
            html += f"""
            <tr>
                <td><strong>{cce['name']}</strong></td>
                <td style="font-size: 12px; color: #7f8c8d;">{cce['id']}</td>
                <td>{cce['type']}</td>
                <td>{cce['version']}</td>
                <td>{cce['node_count']}</td>
                <td>{cce['status']}</td>
                <td>{cce['created']}</td>
            </tr>
            """
        html += "</table>"
    else:
        html += '<h2>☸️ CCE Clusters</h2><p class="no-data">No CCE clusters found</p>'
    
    html += """
            <div class="footer">
                <p><strong>⚠️ Important:</strong> Please review and clean up unused resources to optimize costs.</p>
                <p><em>This report was automatically generated by the OTC Resource Monitor.</em></p>
                <p style="font-size: 12px; margin-top: 10px;">© 2024 OTC Resource Monitor - Powered by FunctionGraph</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email_report(html_report, project_id, token):
    """Send the resource report via SMN"""
    smn_topic_urn = os.environ.get('SMN_TOPIC_URN')
    if not smn_topic_urn:
        raise Exception("SMN_TOPIC_URN environment variable required")
    
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "subject": f"🌐 OTC Resource Monitor Report - {datetime.now().strftime('%Y-%m-%d')}",
        "message": html_report
    }
    
    try:
        response = requests.post(
            SMN_PUBLISH_URL.format(project_id=project_id, topic_urn=smn_topic_urn),
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Report sent successfully via SMN!")
            return True
        else:
            print(f"❌ Failed to send report via SMN: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False