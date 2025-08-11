"""
Authentication module for OTC Resource Monitor
Uses FunctionGraph context token with assigned agency
"""


def get_token(context):
    """
    Get FunctionGraph token from context
    The FunctionGraph function must have an agency assigned with proper permissions
    
    Args:
        context: FunctionGraph context object
    
    Returns:
        str: Authentication token
    """
    if not context:
        raise Exception("FunctionGraph context is required")
    
    try:
        token = context.getToken()
        print("✅ Successfully obtained FunctionGraph token")
        return token
    except Exception as e:
        print(f"❌ Failed to get FunctionGraph token: {str(e)}")
        raise Exception(f"Could not obtain FunctionGraph token: {str(e)}")


def get_project_id(context):
    """
    Get project ID from FunctionGraph context
    
    Args:
        context: FunctionGraph context object
    
    Returns:
        str: Project ID
    """
    if not context:
        raise Exception("FunctionGraph context is required")
    
    try:
        project_id = context.getProjectID()
        print(f"📌 Project ID: {project_id}")
        return project_id
    except Exception as e:
        print(f"❌ Failed to get project ID: {str(e)}")
        raise Exception(f"Could not obtain project ID: {str(e)}")


def get_domain_id(context):
    """
    Get domain ID from FunctionGraph context
    In OTC FunctionGraph, the domain ID is typically the same as the project ID
    
    Args:
        context: FunctionGraph context object
    
    Returns:
        str: Domain ID (using project ID)
    """
    if not context:
        raise Exception("FunctionGraph context is required")
    
    try:
        # In OTC, domain ID and project ID are typically the same for FunctionGraph context
        domain_id = context.getProjectID()
        print(f"📌 Domain ID: {domain_id}")
        return domain_id
    except Exception as e:
        print(f"❌ Failed to get domain ID: {str(e)}")
        raise Exception(f"Could not obtain domain ID: {str(e)}")