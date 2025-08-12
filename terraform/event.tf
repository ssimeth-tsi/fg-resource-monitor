resource "opentelekomcloud_fgs_event_v2" "fg_resource_monitor_test" {
  name         = "fg-resource-monitor-test"
  function_urn = opentelekomcloud_fgs_function_v2.fg_resource_monitor.urn
  content      = base64encode(jsonencode({ triggeredBy = "terraform" }))
}
