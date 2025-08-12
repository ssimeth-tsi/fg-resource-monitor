resource "opentelekomcloud_fgs_function_v2" "fg_resource_monitor" {
  name        = "fg-resource-monitor"
  app         = "default"
  agency      = "functiongraph"
  handler     = "index.handler"
  memory_size = 128
  timeout     = 30
  runtime     = "Python3.9"
  code_type   = "zip"
  func_code   = filebase64("${path.module}/../fg-resource-monitor.zip")
  
  lifecycle {
    ignore_changes = [user_data]
  }
}