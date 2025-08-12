# Using Terraform's archive_file data source
data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "${path.module}/../fg-resource-monitor.zip"
  
  source {
    content  = file("${path.module}/../index.py")
    filename = "index.py"
  }
  
  source {
    content  = file("${path.module}/../requirements.txt")
    filename = "requirements.txt"
  }
  
  # Add all Python files from src directory
  dynamic "source" {
    for_each = fileset("${path.module}/../src", "*.py")
    content {
      content  = file("${path.module}/../src/${source.value}")
      filename = "src/${source.value}"
    }
  }
}

resource "opentelekomcloud_fgs_function_v2" "fg_resource_monitor" {
  name        = "fg-resource-monitor"
  app         = "default"
  agency      = "functiongraph"
  handler     = "index.handler"
  memory_size = 128
  timeout     = 30
  runtime     = "Python3.9"
  code_type   = "zip"
  func_code   = filebase64(data.archive_file.function_zip.output_path)
  
  lifecycle {
    ignore_changes = [user_data]
  }
}