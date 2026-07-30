#!/usr/bin/env python3
"""R35 one-shot, read-only remote post-activation probe."""

import base64
import grp
import hashlib
import json
import os
import pwd
import stat
import subprocess
import sys
import time
import zlib


SCHEMA_VERSION = "d2-r7b-i1-r35-post-activation/v1"
AUTHORITY_ID = "PM-D2-R7B-I1-R35-PHASE5-POST-ACTIVATION-VALIDATION-260729-2143"
PROJECT = "edge-mes-demo"
FRESH_IMAGE = "sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734"
ACTIVE_CONTAINER = "3f0d0457a0a1a929b632a2d865016be6f4104fed001b6015eee14e502bb31ba8"
ALIAS = "edge-mes-demo-collector:latest"
COMPOSE = "/opt/edge-mes-demo/docker-compose.yml"
PARENT = "/opt/edge-mes-demo/config"
TARGET = PARENT + "/mapping.yaml"
BACKUP = (
    PARENT
    + "/.mapping.yaml.d2-r7b-backup.8de5edb."
    + "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
)
UPLOAD = PARENT + "/.mapping.yaml.d2-r7b-new.8de5edb"
ROLLBACK = (
    PARENT
    + "/.mapping.yaml.d2-r7b-rollback.8de5edb."
    + "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
)
SERVICES = {
    "api",
    "collector",
    "dashboard",
    "grafana",
    "node-exporter",
    "postgres",
    "prometheus",
    "s7-plc-sim",
    "simulator",
    "sync-worker",
}
PROTECTED_SERVICES = SERVICES - {"collector"}
COMMAND_PLAN = (
    "aggregate_image_inspect",
    "project_ps_snapshot_a",
    "aggregate_container_inspect_snapshot_a",
    "container_static_exec",
    "project_ps_snapshot_b",
    "aggregate_container_inspect_snapshot_b",
)
CONTAINER_EXEC = (
    "/usr/bin/docker",
    "exec",
    "-i",
    "-e",
    "PYTHONDONTWRITEBYTECODE=1",
    "3f0d0457a0a1a929b632a2d865016be6f4104fed001b6015eee14e502bb31ba8",
    "/usr/local/bin/python",
    "-B",
    "-",
)
INTERVAL_SECONDS = 5
CONTAINER_PROBE_B64 = "IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJSMzUgYWN0aXZlLWNvbnRhaW5lciwgcmVhZC1vbmx5IHNvdXJjZS9pbXBvcnQvc3RhdGljLW1hcHBpbmcgcHJvYmUuIiIiCgppbXBvcnQgaGFzaGxpYgppbXBvcnQgaW1wb3J0bGliCmltcG9ydCBqc29uCmltcG9ydCBzeXMKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgoKU0NIRU1BX1ZFUlNJT04gPSAiZDItcjdiLWkxLXIzNS1jb250YWluZXItc3RhdGljL3YxIgpFWFBFQ1RFRF9NQVBQSU5HID0gewogICAgImJ5dGVzIjogNzExMiwKICAgICJzaGEyNTYiOiAiZDliYjVmY2IwMTdlNmFiNDkxZTg2NDMwNzdjNzkzYmIwMTgwMTFkMWNiZTA2OTgxNzJlNGMwODgyMzA4MGM5ZCIsCiAgICAic2NoZW1hX3ZlcnNpb24iOiAicnVudGltZS1tYXBwaW5nL3YxIiwKICAgICJjb25maWdfdmVyc2lvbiI6ICIyMDI2LjA2LjI2LXNsaWNlLWEiLAogICAgImxpbmVfaWQiOiAiTElORV8wMDEiLAogICAgInJlYWRfcGxhbl9jb3VudCI6IDQsCiAgICAicmVzb2x2ZWRfY29uZmlnX2hhc2giOiAiMDAzOGMwNWQ1Y2Y3NGZmM2I4YzUwOGEzMjIyZWJiNDI2NjU4YWQ4ZTY1N2M1MDM0YWM4OGM0ZmYzMmVmYWUzOCIsCn0KU09VUkNFX0hBU0hFUyA9IHsKICAgICIvYXBwL2FwcC9tYWluLnB5IjogImE4MWI1NDI3ZDY4MmYzYWQyNjc4YmE4MWMxYTA4ZjYxYzgzOWZjZWJlZjg3OTY0ZGI3MWQ0NGVlMThhNjAwOTAiLAogICAgIi9hcHAvYXBwL3NlcnZpY2VzL2V2ZW50X2NvbGxlY3Rvci5weSI6ICJlYjY0N2FmMTVlNTFkMzJjMmFmMGMyZjNkZWZjZThlODQyMWY2MjlhZmQ3MjJiZDM1ODI4MjUzZTI3MTg5NThmIiwKICAgICIvYXBwL2FwcC9zZXJ2aWNlcy9hY2NlcHRlZF9zdGF0aW9uX2V2ZW50X2ZhY3QucHkiOiAiNjU0NWVmNjdkOTY4ZWQ4NDliZTU3MzQyYWQ2MzBiMjU4Y2Q0YTA5NTE5ODc2ZWZiMDI5NTVhOGMzYzZmZDkxMSIsCiAgICAiL2FwcC9hcHAvc2VydmljZXMvc3RvcmFnZS5weSI6ICJmM2FiOGNkYzE4ZWM3NzI1YTFiODYzMDE0YzY5OGY5Y2IyNGYyMTI3NzNiMzZlYWQzOGJlNzU0NWIyODA4ZDBiIiwKICAgICIvYXBwL2FwcC9wbGMvbWFwcGluZy5weSI6ICJjODM0YzQzYjJiYmI0Y2Y4YTIwYTIxMTkwNTNkYmNkMjk3MDI2MGQ3ZTlhODdkNGZjZWQ5OTVlNzNjMTNhMDk4IiwKICAgICIvYXBwL2FwcC9wbGMvcmVhZF9wbGFuLnB5IjogImZkNWY2NzU1MDE0NDRlZDgzNzhkNmEyOTZjM2VkM2Q4NzY5YWY5N2ExZjE5ZDFlOTVmM2MwMGQ3NmQ0YjAyZDYiLAogICAgIi9hcHAvYXBwL3NlcnZpY2VzL3Jlc29sdmVkX2NvbmZpZ19yZWdpc3RyeS5weSI6ICIxODQ0NDQ5YTNmOTllOWNhNTNiZGRjODA2M2MxNTFmYjBmODg5OTIwNTk3YmNjYjE3MGY1ZTYyZjM3MTVkYjJjIiwKICAgICIvYXBwL2NvbW1vbi9zdGF0aW9uX2V2ZW50L19faW5pdF9fLnB5IjogImQ4YTIxNGQwYzRhODVlN2JiYWY3YjVlNzllNmRiOTA1MTE1YmUxZjUwZWZmYjI3MzU3ZmE5ZjM3MWVhMWM3YTciLAogICAgIi9hcHAvY29tbW9uL3N0YXRpb25fZXZlbnQvY29uc3RhbnRzLnB5IjogIjZkZDYwNzA1YWIxOTJhMWM4ODlmMGE0NjUyZDQ3OGY3ZDM2N2JkMjRiOTgwZmMwOTJjNDhhNTFlMjUyMTRlMTEiLAogICAgIi9hcHAvY29tbW9uL3N0YXRpb25fZXZlbnQvZXJyb3JzLnB5IjogIjM1NWM4ODJmNTFjYzdjNjZjZGY4ZjIyYzczYzBkNzI2MzMzOTFkYzg0MDNkNGY5ZjQyOGIwYjhhYzUxMGI0ZjMiLAogICAgIi9hcHAvY29tbW9uL3N0YXRpb25fZXZlbnQvZmluZ2VycHJpbnQucHkiOiAiY2IzNWRjZjVhYjViYTljY2IzZTYwZDBlMzhiMWM4NmNmMjQ3MTc1NTljYzcwZTI1MGFkZjI5N2RmZjkzOTYwOCIsCiAgICAiL2FwcC9jb21tb24vc3RhdGlvbl9ldmVudC9saWZlY3ljbGUucHkiOiAiYWZlYzJjNzUwMTBiODY0MjIzOWQyNDk0YzU3ZjQ3MGYzNDE0YzRmYmZmNDg2YjU4ODU4OWFkZjdiYzRlZmNmZiIsCiAgICAiL2FwcC9jb21tb24vc3RhdGlvbl9ldmVudC9tb2RlbHMucHkiOiAiMTc2NjI3YjcxZjMyYmRlZjA4Yzc1YTZiZmUzYjdiYWRhYjEwOTRlOGVjMmMzY2Y3YjFlNzE5ZDBhMmQxZGY3NyIsCiAgICAiL2FwcC9jb21tb24vc3RhdGlvbl9ldmVudC9wcm9qZWN0aW9uLnB5IjogIjM5ZWQ2MDM0ZDg3ZTIzNzE4YTIyYThhNjZmYmI2MGFmMzY1YTVkN2I1NzNmZjA0NWEwMjFiNzIwNmM3MDg2MjMiLAogICAgIi9hcHAvY29tbW9uL3N0YXRpb25fZXZlbnQvc2VyaWFsaXphdGlvbi5weSI6ICI5Y2JhYmJkNDJlNTY4NTMxMTgyOTAzMGIxM2YyNGZhMTYzOTZmYjg1MzQ1OGUzZjUxYmQ3Y2I3YmY1MTI0NDA3IiwKICAgICIvYXBwL2NvbW1vbi9zdGF0aW9uX2V2ZW50L3ZhbGlkYXRpb24ucHkiOiAiZTdjZmY0NmI5MTExMjIzNjg3Mzc0NGEzMmRhZmVjNTE2MGEwY2E2MDM2ZjE4NDEwNmUxZWM0YTIzMjcyNGJkMSIsCn0KUkVRVUlSRURfSU1QT1JUUyA9ICgKICAgICJjb21tb24uc3RhdGlvbl9ldmVudCIsCiAgICAiYXBwLm1haW4iLAogICAgImFwcC5zZXJ2aWNlcy5ldmVudF9jb2xsZWN0b3IiLAogICAgImFwcC5zZXJ2aWNlcy5hY2NlcHRlZF9zdGF0aW9uX2V2ZW50X2ZhY3QiLAogICAgImFwcC5zZXJ2aWNlcy5zdG9yYWdlIiwKICAgICJhcHAucGxjLm1hcHBpbmciLAogICAgImFwcC5wbGMucmVhZF9wbGFuIiwKICAgICJhcHAuc2VydmljZXMucmVzb2x2ZWRfY29uZmlnX3JlZ2lzdHJ5IiwKKQoKCmRlZiBzaGEyNTYoZGF0YTogYnl0ZXMpIC0+IHN0cjoKICAgIHJldHVybiBoYXNobGliLnNoYTI1NihkYXRhKS5oZXhkaWdlc3QoKQoKCmRlZiBlbWl0KHN0YXR1czogc3RyLCBjbGFzc2lmaWNhdGlvbjogc3RyLCBvYnNlcnZlZDogZGljdCwgYXNzZXJ0aW9uczogZGljdCkgLT4gTm9uZToKICAgIHRlcm1pbmFsID0gewogICAgICAgICJzY2hlbWFfdmVyc2lvbiI6IFNDSEVNQV9WRVJTSU9OLAogICAgICAgICJzdGF0dXMiOiBzdGF0dXMsCiAgICAgICAgImNsYXNzaWZpY2F0aW9uIjogY2xhc3NpZmljYXRpb24sCiAgICAgICAgIm9ic2VydmVkIjogb2JzZXJ2ZWQsCiAgICAgICAgImFzc2VydGlvbnMiOiBhc3NlcnRpb25zLAogICAgICAgICJtdXRhdGlvbl9hdWRpdCI6IHsKICAgICAgICAgICAgImZpbGVzeXN0ZW1fd3JpdGVzIjogMCwKICAgICAgICAgICAgImRiX2Nvbm5lY3Rpb25zIjogMCwKICAgICAgICAgICAgImFwaV9jYWxscyI6IDAsCiAgICAgICAgICAgICJwbGNfY29ubmVjdGlvbnMiOiAwLAogICAgICAgICAgICAic29ja2V0X2Nvbm5lY3Rpb25zIjogMCwKICAgICAgICAgICAgInByb2R1Y3Rpb25fZGF0YV9nZW5lcmF0ZWQiOiAwLAogICAgICAgICAgICAicnVudGltZV93b3JrZXJfY29uc3RydWN0aW9ucyI6IDAsCiAgICAgICAgICAgICJzdG9yYWdlX2NvbnN0cnVjdGlvbnMiOiAwLAogICAgICAgIH0sCiAgICAgICAgImV2aWRlbmNlX2JvdW5kYXJ5IjogewogICAgICAgICAgICAiU1RBVElDX01BUFBJTkdfSU5JVElBTElaRUQiOiBzdGF0dXMgPT0gIlBBU1MiLAogICAgICAgICAgICAiUlVOVElNRV9MT0FERUQiOiBGYWxzZSwKICAgICAgICAgICAgIlBST0RVQ1RJT05fQUNDRVBURUQiOiBGYWxzZSwKICAgICAgICB9LAogICAgfQogICAgc3lzLnN0ZG91dC53cml0ZSgKICAgICAgICBqc29uLmR1bXBzKAogICAgICAgICAgICB0ZXJtaW5hbCwKICAgICAgICAgICAgZW5zdXJlX2FzY2lpPUZhbHNlLAogICAgICAgICAgICBzb3J0X2tleXM9VHJ1ZSwKICAgICAgICAgICAgc2VwYXJhdG9ycz0oIiwiLCAiOiIpLAogICAgICAgICkKICAgICkKCgpkZWYgbWFpbigpIC0+IE5vbmU6CiAgICBvYnNlcnZlZCA9IHsKICAgICAgICAiZG9udF93cml0ZV9ieXRlY29kZSI6IHN5cy5kb250X3dyaXRlX2J5dGVjb2RlLAogICAgICAgICJzb3VyY2VfaGFzaGVzIjoge30sCiAgICAgICAgImltcG9ydHMiOiB7fSwKICAgICAgICAibWFwcGluZyI6IHt9LAogICAgfQogICAgYXNzZXJ0aW9ucyA9IHsKICAgICAgICAiZG9udF93cml0ZV9ieXRlY29kZSI6IHN5cy5kb250X3dyaXRlX2J5dGVjb2RlIGlzIFRydWUsCiAgICAgICAgInNvdXJjZV9oYXNoZXNfZXhhY3QiOiBGYWxzZSwKICAgICAgICAiaW1wb3J0c19leGFjdCI6IEZhbHNlLAogICAgICAgICJtYXBwaW5nX2V4YWN0IjogRmFsc2UsCiAgICB9CgogICAgdHJ5OgogICAgICAgIGZvciBzb3VyY2VfcGF0aCwgZXhwZWN0ZWRfaGFzaCBpbiBzb3J0ZWQoU09VUkNFX0hBU0hFUy5pdGVtcygpKToKICAgICAgICAgICAgZGF0YSA9IFBhdGgoc291cmNlX3BhdGgpLnJlYWRfYnl0ZXMoKQogICAgICAgICAgICBvYnNlcnZlZFsic291cmNlX2hhc2hlcyJdW3NvdXJjZV9wYXRoXSA9IHsKICAgICAgICAgICAgICAgICJieXRlcyI6IGxlbihkYXRhKSwKICAgICAgICAgICAgICAgICJzaGEyNTYiOiBzaGEyNTYoZGF0YSksCiAgICAgICAgICAgICAgICAiZXhwZWN0ZWRfc2hhMjU2IjogZXhwZWN0ZWRfaGFzaCwKICAgICAgICAgICAgICAgICJtYXRjaCI6IHNoYTI1NihkYXRhKSA9PSBleHBlY3RlZF9oYXNoLAogICAgICAgICAgICB9CiAgICAgICAgYXNzZXJ0aW9uc1sic291cmNlX2hhc2hlc19leGFjdCJdID0gKAogICAgICAgICAgICBsZW4ob2JzZXJ2ZWRbInNvdXJjZV9oYXNoZXMiXSkgPT0gbGVuKFNPVVJDRV9IQVNIRVMpCiAgICAgICAgICAgIGFuZCBhbGwoaXRlbVsibWF0Y2giXSBmb3IgaXRlbSBpbiBvYnNlcnZlZFsic291cmNlX2hhc2hlcyJdLnZhbHVlcygpKQogICAgICAgICkKICAgICAgICBpZiBub3QgYXNzZXJ0aW9uc1sic291cmNlX2hhc2hlc19leGFjdCJdOgogICAgICAgICAgICBlbWl0KCJIT0xEIiwgIlNPVVJDRV9JREVOVElUWV9GQUlMRUQiLCBvYnNlcnZlZCwgYXNzZXJ0aW9ucykKICAgICAgICAgICAgcmV0dXJuCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICBvYnNlcnZlZFsic291cmNlX2Vycm9yIl0gPSB0eXBlKGV4YykuX19uYW1lX18KICAgICAgICBlbWl0KCJIT0xEIiwgIlNPVVJDRV9JREVOVElUWV9GQUlMRUQiLCBvYnNlcnZlZCwgYXNzZXJ0aW9ucykKICAgICAgICByZXR1cm4KCiAgICB0cnk6CiAgICAgICAgZm9yIG1vZHVsZV9uYW1lIGluIFJFUVVJUkVEX0lNUE9SVFM6CiAgICAgICAgICAgIGltcG9ydGVkID0gaW1wb3J0bGliLmltcG9ydF9tb2R1bGUobW9kdWxlX25hbWUpCiAgICAgICAgICAgIG9ic2VydmVkWyJpbXBvcnRzIl1bbW9kdWxlX25hbWVdID0gewogICAgICAgICAgICAgICAgIm1vZHVsZSI6IGltcG9ydGVkLl9fbmFtZV9fLAogICAgICAgICAgICAgICAgInN1Y2Nlc3MiOiBUcnVlLAogICAgICAgICAgICB9CiAgICAgICAgYXNzZXJ0aW9uc1siaW1wb3J0c19leGFjdCJdID0gKAogICAgICAgICAgICB0dXBsZShvYnNlcnZlZFsiaW1wb3J0cyJdKSA9PSBSRVFVSVJFRF9JTVBPUlRTCiAgICAgICAgICAgIGFuZCBhbGwoaXRlbVsic3VjY2VzcyJdIGZvciBpdGVtIGluIG9ic2VydmVkWyJpbXBvcnRzIl0udmFsdWVzKCkpCiAgICAgICAgKQogICAgICAgIGlmIG5vdCBhc3NlcnRpb25zWyJpbXBvcnRzX2V4YWN0Il06CiAgICAgICAgICAgIGVtaXQoIkhPTEQiLCAiSU1QT1JUX0NMT1NVUkVfRkFJTEVEIiwgb2JzZXJ2ZWQsIGFzc2VydGlvbnMpCiAgICAgICAgICAgIHJldHVybgogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgb2JzZXJ2ZWRbImltcG9ydF9lcnJvciJdID0gewogICAgICAgICAgICAidHlwZSI6IHR5cGUoZXhjKS5fX25hbWVfXywKICAgICAgICAgICAgIm1vZHVsZSI6IG1vZHVsZV9uYW1lLAogICAgICAgIH0KICAgICAgICBlbWl0KCJIT0xEIiwgIklNUE9SVF9DTE9TVVJFX0ZBSUxFRCIsIG9ic2VydmVkLCBhc3NlcnRpb25zKQogICAgICAgIHJldHVybgoKICAgIHRyeToKICAgICAgICBtYXBwaW5nX3BhdGggPSBQYXRoKCIvYXBwL2NvbmZpZy9tYXBwaW5nLnlhbWwiKQogICAgICAgIG1hcHBpbmdfYnl0ZXMgPSBtYXBwaW5nX3BhdGgucmVhZF9ieXRlcygpCiAgICAgICAgZnJvbSBhcHAucGxjLm1hcHBpbmcgaW1wb3J0IGxvYWRfZWRnZV9tYXBwaW5nCiAgICAgICAgZnJvbSBhcHAucGxjLnJlYWRfcGxhbiBpbXBvcnQgYnVpbGRfcmVhZF9wbGFucwogICAgICAgIGZyb20gYXBwLnNlcnZpY2VzLnJlc29sdmVkX2NvbmZpZ19yZWdpc3RyeSBpbXBvcnQgKAogICAgICAgICAgICBidWlsZF9yZXNvbHZlZF9jb25maWdfc25hcHNob3RfZnJvbV9tYXBwaW5nLAogICAgICAgICkKCiAgICAgICAgbWFwcGluZyA9IGxvYWRfZWRnZV9tYXBwaW5nKG1hcHBpbmdfcGF0aCkKICAgICAgICByZWFkX3BsYW5zID0gYnVpbGRfcmVhZF9wbGFucyhtYXBwaW5nKQogICAgICAgIHJlc29sdmVkID0gYnVpbGRfcmVzb2x2ZWRfY29uZmlnX3NuYXBzaG90X2Zyb21fbWFwcGluZyhtYXBwaW5nLnJ1bnRpbWVfc25hcHNob3QpCiAgICAgICAgb2JzZXJ2ZWRbIm1hcHBpbmciXSA9IHsKICAgICAgICAgICAgInBhdGgiOiBzdHIobWFwcGluZ19wYXRoKSwKICAgICAgICAgICAgImJ5dGVzIjogbGVuKG1hcHBpbmdfYnl0ZXMpLAogICAgICAgICAgICAic2hhMjU2Ijogc2hhMjU2KG1hcHBpbmdfYnl0ZXMpLAogICAgICAgICAgICAic2NoZW1hX3ZlcnNpb24iOiBtYXBwaW5nLnNjaGVtYV92ZXJzaW9uLAogICAgICAgICAgICAiY29uZmlnX3ZlcnNpb24iOiBtYXBwaW5nLmNvbmZpZ192ZXJzaW9uLAogICAgICAgICAgICAibGluZV9pZCI6IG1hcHBpbmcubGluZV9pZCwKICAgICAgICAgICAgInJlYWRfcGxhbl9jb3VudCI6IGxlbihyZWFkX3BsYW5zKSwKICAgICAgICAgICAgInJlc29sdmVkX2NvbmZpZ19oYXNoIjogcmVzb2x2ZWQuY29uZmlnX2hhc2gsCiAgICAgICAgfQogICAgICAgIGFzc2VydGlvbnNbIm1hcHBpbmdfZXhhY3QiXSA9IG9ic2VydmVkWyJtYXBwaW5nIl0gPT0gewogICAgICAgICAgICAicGF0aCI6ICIvYXBwL2NvbmZpZy9tYXBwaW5nLnlhbWwiLAogICAgICAgICAgICAqKkVYUEVDVEVEX01BUFBJTkcsCiAgICAgICAgfQogICAgICAgIGlmIG5vdCBhc3NlcnRpb25zWyJtYXBwaW5nX2V4YWN0Il06CiAgICAgICAgICAgIGVtaXQoIkhPTEQiLCAiTUFQUElOR19JREVOVElUWV9GQUlMRUQiLCBvYnNlcnZlZCwgYXNzZXJ0aW9ucykKICAgICAgICAgICAgcmV0dXJuCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICBvYnNlcnZlZFsibWFwcGluZ19lcnJvciJdID0gdHlwZShleGMpLl9fbmFtZV9fCiAgICAgICAgZW1pdCgiSE9MRCIsICJNQVBQSU5HX0lERU5USVRZX0ZBSUxFRCIsIG9ic2VydmVkLCBhc3NlcnRpb25zKQogICAgICAgIHJldHVybgoKICAgIGlmIG5vdCBhbGwoYXNzZXJ0aW9ucy52YWx1ZXMoKSk6CiAgICAgICAgZW1pdCgiSE9MRCIsICJDT05UQUlORVJfU1RBVElDX1BST0JFX0lOVkFMSUQiLCBvYnNlcnZlZCwgYXNzZXJ0aW9ucykKICAgICAgICByZXR1cm4KICAgIGVtaXQoIlBBU1MiLCAiU1RBVElDX01BUFBJTkdfSU5JVElBTElaRUQiLCBvYnNlcnZlZCwgYXNzZXJ0aW9ucykKCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgbWFpbigpCg=="
EXPECTED_SNAPSHOT_B64 = "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"
EXPECTED_HOST_B64 = "eJzFVE2P0zAQ/S8+p6k/Y7s3kPaKEHBDCI3tSTZqvuS4WqJV/ztO2S4r6IrVFsHR1rzn8Xtv5p74sZ/GGcnunrgl4Ux20lhdkIjQTZBuyY5sxyltMTS46XHeBOzHbRj9HuPmAVwufUdWSHPoIJJdigcsyHwLXFUZD5qBM0yBkLXw0opaGPRKc6S+VsZysKB98NSwYIJAjoJxEIZ6CBZrmqnn/EI77Mmuhm7GY0HqtsN5mRP2p87B7w/Tkz8oK1RB8NuEPmE4d9TEca0iPcQ2k7YBh9Sm5eucwHV4rmqHMeSDUtSyqiD96URoJWXGjHcDxp8Uzyvkx6Fum23ZwzS1Q1Mu0Hdl4Juo3eZHu6UJqDC40lRQi4oCCkDAigqwGkKQTFEuVfA1WqdMcL62Xso6l2kLFXdgeEWlFydu8ifL/kNDjwm4lnDlSpBWH95/uPl48+4TOa7ix2zg6npoYzZ6jMszTp891Fr97uFLZLsUwTh23Src2sDrZD8z/H3hH8R68/as1ZzD7iHm0fhM/l0EvhQkQWwwPRlNzRi/fjQN59eO5lMVXjo9v2AeAx6sc6r2jjKNFThpGZpKihw4r61w+d5QxgLzDmllDcu7T+Z9Z7igec3ZcDngh6kbIbw+XwPenQ29EIrj8TsLyuZe"

AUDIT = []
OBSERVED = {}
ASSERTIONS = {}
MUTATION_AUDIT = {
    "image_tag_mutations": 0,
    "compose_commands": 0,
    "container_lifecycle_commands": 0,
    "protected_service_lifecycle": 0,
    "rollback": 0,
    "cleanup": 0,
    "filesystem_writes": 0,
    "db_api_plc_access": 0,
}
CONTAINER_EXEC_COUNT = 0


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def decoded_constant(value):
    return json.loads(zlib.decompress(base64.b64decode(value)).decode("utf-8", "strict"))


EXPECTED_SNAPSHOT = decoded_constant(EXPECTED_SNAPSHOT_B64)
EXPECTED_HOST = decoded_constant(EXPECTED_HOST_B64)
CONTAINER_PROBE = base64.b64decode(CONTAINER_PROBE_B64)


def run(name, argv, input_bytes=None):
    global CONTAINER_EXEC_COUNT
    if len(AUDIT) >= len(COMMAND_PLAN) or COMMAND_PLAN[len(AUDIT)] != name:
        raise RuntimeError("COMMAND_BUDGET_EXCEEDED")
    if name == "container_static_exec":
        if tuple(argv) != CONTAINER_EXEC or CONTAINER_EXEC_COUNT != 0:
            raise RuntimeError("COMMAND_BUDGET_EXCEEDED")
        CONTAINER_EXEC_COUNT = 1
    proc = subprocess.run(
        argv,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    AUDIT.append(
        {
            "name": name,
            "argv": list(argv),
            "returncode": proc.returncode,
            "stdout_bytes": len(proc.stdout),
            "stderr_bytes": len(proc.stderr),
            "stdout_sha256": sha256(proc.stdout),
            "stderr_sha256": sha256(proc.stderr),
            "stdin_bytes": 0 if input_bytes is None else len(input_bytes),
            "stdin_sha256": None if input_bytes is None else sha256(input_bytes),
        }
    )
    return proc


def parsed(proc):
    if proc is None or proc.returncode != 0 or proc.stderr:
        return None
    try:
        return json.loads(proc.stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def container_view(item):
    state = item.get("State") or {}
    config = item.get("Config") or {}
    host = item.get("HostConfig") or {}
    labels = config.get("Labels") or {}
    mounts = [
        {
            "Type": mount.get("Type"),
            "Source": mount.get("Source"),
            "Destination": mount.get("Destination"),
            "RW": mount.get("RW"),
        }
        for mount in item.get("Mounts", [])
    ]
    return {
        "Id": item.get("Id"),
        "Name": item.get("Name"),
        "Image": item.get("Image"),
        "Config.Image": config.get("Image"),
        "labels": {
            "project": labels.get("com.docker.compose.project"),
            "service": labels.get("com.docker.compose.service"),
        },
        "Created": item.get("Created"),
        "State.StartedAt": state.get("StartedAt"),
        "State.Status": state.get("Status"),
        "State.Running": state.get("Running"),
        "State.Restarting": state.get("Restarting"),
        "State.Dead": state.get("Dead"),
        "State.ExitCode": state.get("ExitCode"),
        "State.OOMKilled": state.get("OOMKilled"),
        "State.Error": state.get("Error"),
        "RestartCount": item.get("RestartCount"),
        "HostConfig.RestartPolicy": (host.get("RestartPolicy") or {}).get("Name"),
        "Mounts": sorted(
            mounts,
            key=lambda mount: (
                str(mount.get("Type")),
                str(mount.get("Source")),
                str(mount.get("Destination")),
                str(mount.get("RW")),
            ),
        ),
    }


def raw_snapshot(ps_proc, inspect_proc):
    ids = (
        ps_proc.stdout.decode("utf-8", "strict").splitlines()
        if ps_proc.returncode == 0 and not ps_proc.stderr
        else []
    )
    inspected = parsed(inspect_proc)
    return {
        "ids": ids,
        "containers": [] if not isinstance(inspected, list) else [container_view(item) for item in inspected],
        "inspect_ok": isinstance(inspected, list) and inspect_proc.returncode == 0,
    }


def canonical(snapshot):
    ids = snapshot.get("ids", [])
    if len(ids) != len(set(ids)):
        raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
    services = set()
    full_ids = set()
    containers = []
    for original in snapshot.get("containers", []):
        item = dict(original)
        labels = item.get("labels") or {}
        service = labels.get("service")
        full_id = item.get("Id")
        if labels.get("project") != PROJECT or not service:
            raise ValueError("DUPLICATE_DISCOVERED_SERVICE")
        if service in services:
            raise ValueError("DUPLICATE_DISCOVERED_SERVICE")
        if not full_id or full_id in full_ids:
            raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
        services.add(service)
        full_ids.add(full_id)
        item["Mounts"] = sorted(
            item.get("Mounts", []),
            key=lambda mount: (
                str(mount.get("Type")),
                str(mount.get("Source")),
                str(mount.get("Destination")),
                str(mount.get("RW")),
            ),
        )
        containers.append(item)
    return {
        "ids": sorted(set(ids)),
        "containers": sorted(
            containers,
            key=lambda item: (item["labels"]["service"], item["Id"]),
        ),
        "inspect_ok": snapshot.get("inspect_ok"),
    }


def nofollow_file(path, expected_bytes, expected_hash):
    metadata = os.lstat(path)
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        return {"path": path, "state": "INVALID_TYPE_OR_SYMLINK"}
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        chunks = []
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    data = b"".join(chunks)
    return {
        "path": path,
        "state": "PRESENT",
        "realpath": os.path.realpath(path),
        "owner": pwd.getpwuid(before.st_uid).pw_name,
        "group": grp.getgrgid(before.st_gid).gr_name,
        "mode": format(stat.S_IMODE(before.st_mode), "04o"),
        "bytes": len(data),
        "sha256": sha256(data),
        "inode": before.st_ino,
        "identity_stable": (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        )
        == (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ),
        "expected": len(data) == expected_bytes and sha256(data) == expected_hash,
    }


def absent(path):
    try:
        return {
            "path": path,
            "state": "PRESENT",
            "symlink": stat.S_ISLNK(os.lstat(path).st_mode),
        }
    except FileNotFoundError:
        return {"path": path, "state": "ABSENT"}


def filesystem_snapshot():
    parent_stat = os.lstat(PARENT)
    return {
        "parent": {
            "directory": stat.S_ISDIR(parent_stat.st_mode),
            "symlink": stat.S_ISLNK(parent_stat.st_mode),
            "realpath": os.path.realpath(PARENT),
            "owner": pwd.getpwuid(parent_stat.st_uid).pw_name,
            "group": grp.getgrgid(parent_stat.st_gid).gr_name,
            "mode": format(stat.S_IMODE(parent_stat.st_mode), "04o"),
        },
        "target": nofollow_file(
            TARGET,
            7112,
            "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d",
        ),
        "backup": nofollow_file(
            BACKUP,
            5935,
            "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3",
        ),
        "upload": absent(UPLOAD),
        "rollback": absent(ROLLBACK),
        "sidecars": sorted(
            name for name in os.listdir(PARENT) if name.startswith(".mapping.yaml.d2-r7b-")
        ),
    }


def compose_snapshot():
    metadata = os.lstat(COMPOSE)
    descriptor = os.open(COMPOSE, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        data = b""
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            data += chunk
    finally:
        os.close(descriptor)
    return {
        "regular": stat.S_ISREG(metadata.st_mode),
        "symlink": stat.S_ISLNK(metadata.st_mode),
        "realpath": os.path.realpath(COMPOSE),
        "bytes": len(data),
        "sha256": sha256(data),
    }


def host_snapshot():
    return {
        "filesystem": filesystem_snapshot(),
        "compose": compose_snapshot(),
    }


def by_service(snapshot):
    return {
        item["labels"]["service"]: item
        for item in snapshot["containers"]
    }


def protected_hard_view(item):
    return {
        key: value
        for key, value in item.items()
        if key not in {"Config.Image", "Name"}
    }


def terminal(status, classification):
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_id": AUTHORITY_ID,
        "status": status,
        "classification": classification,
        "observed": OBSERVED,
        "assertions": ASSERTIONS,
        "command_audit": AUDIT,
        "remote_call_budget": {
            "structured_ssh_calls": 1,
            "retry": 0,
            "resume": 0,
            "supplemental_ssh": 0,
            "other_network_calls": 0,
        },
        "docker_budget": {
            "commands": len(AUDIT),
            "maximum": 6,
            "container_exec": CONTAINER_EXEC_COUNT,
            "container_exec_maximum": 1,
        },
        "mutation_audit": MUTATION_AUDIT,
        "evidence_boundary": {
            "ACTIVATED": status == "PASS",
            "STATIC_MAPPING_INITIALIZED": status == "PASS",
            "RUNTIME_LOADED": False,
            "PRODUCTION_ACCEPTED": False,
        },
    }


def emit(status, classification):
    sys.stdout.write(
        json.dumps(
            terminal(status, classification),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def hold_classification():
    priorities = (
        ("duplicate_service_absent", "DUPLICATE_DISCOVERED_SERVICE"),
        ("duplicate_container_absent", "DUPLICATE_DISCOVERED_CONTAINER_ID"),
        ("command_plan_exact", "COMMAND_BUDGET_EXCEEDED"),
        ("image_alias_exact", "WRONG_ACTIVE_IMAGE"),
        ("snapshot_a_authority_exact", "ACTIVE_COLLECTOR_LIFECYCLE_DRIFT"),
        ("collector_lifecycle_stable", "ACTIVE_COLLECTOR_LIFECYCLE_DRIFT"),
        ("collector_safe", "RESTART_LOOP"),
        ("protected_hard_fields_stable", "PROTECTED_SERVICE_DRIFT"),
        ("remote_compose_exact", "REMOTE_COMPOSE_IDENTITY_DRIFT"),
        ("host_filesystem_exact_and_stable", "MAPPING_IDENTITY_FAILED"),
        ("container_terminal_valid", "CONTAINER_STATIC_PROBE_INVALID"),
        ("source_hashes_exact", "SOURCE_IDENTITY_FAILED"),
        ("imports_exact", "IMPORT_CLOSURE_FAILED"),
        ("mapping_exact", "MAPPING_IDENTITY_FAILED"),
        ("host_container_mapping_agree", "MAPPING_IDENTITY_FAILED"),
        ("mutation_counters_zero", "ALLOWLIST_VIOLATION"),
    )
    for assertion, classification in priorities:
        if ASSERTIONS.get(assertion) is not True:
            return classification
    return "REMOTE_OBSERVATION_FAILED"


def main():
    duplicate_service_absent = True
    duplicate_container_absent = True
    try:
        host_a = host_snapshot()
        image_proc = run(
            "aggregate_image_inspect",
            ["/usr/bin/docker", "image", "inspect", FRESH_IMAGE, ALIAS],
        )
        ps_a = run(
            "project_ps_snapshot_a",
            [
                "/usr/bin/docker",
                "ps",
                "-aq",
                "--filter",
                "label=com.docker.compose.project=" + PROJECT,
            ],
        )
        ids_a = (
            ps_a.stdout.decode("utf-8", "strict").splitlines()
            if ps_a.returncode == 0 and not ps_a.stderr
            else []
        )
        inspect_a = run(
            "aggregate_container_inspect_snapshot_a",
            ["/usr/bin/docker", "inspect", *ids_a],
        )
        raw_a = raw_snapshot(ps_a, inspect_a)
        canonical_a = canonical(raw_a)

        container_proc = run(
            "container_static_exec",
            list(CONTAINER_EXEC),
            input_bytes=CONTAINER_PROBE,
        )
        container_terminal = parsed(container_proc)

        time.sleep(INTERVAL_SECONDS)

        ps_b = run(
            "project_ps_snapshot_b",
            [
                "/usr/bin/docker",
                "ps",
                "-aq",
                "--filter",
                "label=com.docker.compose.project=" + PROJECT,
            ],
        )
        ids_b = (
            ps_b.stdout.decode("utf-8", "strict").splitlines()
            if ps_b.returncode == 0 and not ps_b.stderr
            else []
        )
        inspect_b = run(
            "aggregate_container_inspect_snapshot_b",
            ["/usr/bin/docker", "inspect", *ids_b],
        )
        raw_b = raw_snapshot(ps_b, inspect_b)
        canonical_b = canonical(raw_b)
        host_b = host_snapshot()
    except ValueError as exc:
        duplicate_service_absent = str(exc) != "DUPLICATE_DISCOVERED_SERVICE"
        duplicate_container_absent = str(exc) != "DUPLICATE_DISCOVERED_CONTAINER_ID"
        ASSERTIONS.update(
            {
                "duplicate_service_absent": duplicate_service_absent,
                "duplicate_container_absent": duplicate_container_absent,
            }
        )
        emit("HOLD", str(exc))
        return
    except Exception as exc:
        OBSERVED["remote_exception"] = type(exc).__name__
        emit(
            "HOLD",
            "COMMAND_BUDGET_EXCEEDED"
            if str(exc) == "COMMAND_BUDGET_EXCEEDED"
            else "REMOTE_OBSERVATION_FAILED",
        )
        return

    images = parsed(image_proc)
    services_a = by_service(canonical_a)
    services_b = by_service(canonical_b)
    collector_a = services_a.get("collector")
    collector_b = services_b.get("collector")
    expected_collector = by_service(EXPECTED_SNAPSHOT).get("collector")
    container_mapping = (
        (container_terminal.get("observed") or {}).get("mapping")
        if isinstance(container_terminal, dict)
        else None
    )
    host_mapping = host_a["filesystem"]["target"]

    OBSERVED.update(
        {
            "host_snapshot_a": host_a,
            "image_alias_inspect": images,
            "snapshot_a_raw": raw_a,
            "snapshot_a_canonical": canonical_a,
            "container_static_terminal": container_terminal,
            "interval_seconds": INTERVAL_SECONDS,
            "snapshot_b_raw": raw_b,
            "snapshot_b_canonical": canonical_b,
            "host_snapshot_b": host_b,
        }
    )

    ASSERTIONS.update(
        {
            "duplicate_service_absent": duplicate_service_absent,
            "duplicate_container_absent": duplicate_container_absent,
            "command_plan_exact": tuple(item["name"] for item in AUDIT) == COMMAND_PLAN
            and len(AUDIT) == 6
            and CONTAINER_EXEC_COUNT == 1,
            "image_alias_exact": isinstance(images, list)
            and len(images) == 2
            and all(item.get("Id") == FRESH_IMAGE for item in images)
            and all(item.get("Os") == "linux" and item.get("Architecture") == "arm64" for item in images)
            and all(ALIAS in (item.get("RepoTags") or []) for item in images),
            "snapshot_a_authority_exact": canonical_a == EXPECTED_SNAPSHOT,
            "service_set_exact": set(services_a) == SERVICES == set(services_b),
            "collector_lifecycle_stable": collector_a == expected_collector
            and collector_b == collector_a
            and collector_a is not None
            and collector_a.get("Id") == ACTIVE_CONTAINER
            and collector_a.get("Image") == FRESH_IMAGE
            and collector_a.get("Config.Image") == "edge-mes-demo-collector"
            and collector_a.get("Created") == "2026-07-29T13:37:58.275753165Z"
            and collector_a.get("State.StartedAt") == "2026-07-29T13:38:09.122963461Z"
            and collector_a.get("RestartCount") == 0,
            "collector_safe": collector_a is not None
            and collector_b is not None
            and all(
                item.get("State.Running") is True
                and item.get("State.Restarting") is False
                and item.get("State.Dead") is False
                and item.get("State.ExitCode") == 0
                and item.get("State.OOMKilled") is False
                and item.get("State.Error") == ""
                and item.get("RestartCount") == 0
                and item.get("HostConfig.RestartPolicy") == "unless-stopped"
                for item in (collector_a, collector_b)
            ),
            "collector_mount_exact": collector_a is not None
            and collector_b is not None
            and collector_a.get("Mounts")
            == collector_b.get("Mounts")
            == [
                {
                    "Type": "bind",
                    "Source": PARENT,
                    "Destination": "/app/config",
                    "RW": False,
                }
            ],
            "protected_hard_fields_stable": all(
                service in services_a
                and service in services_b
                and protected_hard_view(services_a[service])
                == protected_hard_view(services_b[service])
                == protected_hard_view(by_service(EXPECTED_SNAPSHOT)[service])
                for service in PROTECTED_SERVICES
            ),
            "remote_compose_exact": host_a["compose"]
            == host_b["compose"]
            == {
                "regular": True,
                "symlink": False,
                "realpath": COMPOSE,
                "bytes": 4897,
                "sha256": "a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0",
            },
            "host_filesystem_exact_and_stable": host_a == EXPECTED_HOST
            and host_b == host_a,
            "container_terminal_valid": isinstance(container_terminal, dict)
            and container_proc.returncode == 0
            and not container_proc.stderr
            and container_terminal.get("schema_version")
            == "d2-r7b-i1-r35-container-static/v1"
            and container_terminal.get("status") == "PASS"
            and container_terminal.get("classification") == "STATIC_MAPPING_INITIALIZED",
            "source_hashes_exact": isinstance(container_terminal, dict)
            and (container_terminal.get("assertions") or {}).get("source_hashes_exact")
            is True,
            "imports_exact": isinstance(container_terminal, dict)
            and (container_terminal.get("assertions") or {}).get("imports_exact") is True,
            "mapping_exact": isinstance(container_terminal, dict)
            and (container_terminal.get("assertions") or {}).get("mapping_exact") is True,
            "host_container_mapping_agree": isinstance(container_mapping, dict)
            and host_mapping.get("bytes") == container_mapping.get("bytes") == 7112
            and host_mapping.get("sha256")
            == container_mapping.get("sha256")
            == "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d",
            "bytecode_disabled": isinstance(container_terminal, dict)
            and (container_terminal.get("observed") or {}).get("dont_write_bytecode")
            is True,
            "mutation_counters_zero": all(value == 0 for value in MUTATION_AUDIT.values())
            and isinstance(container_terminal, dict)
            and all(
                value == 0
                for value in (container_terminal.get("mutation_audit") or {}).values()
            ),
        }
    )

    if all(ASSERTIONS.values()):
        emit("PASS", "ACTIVATED")
    else:
        emit("HOLD", hold_classification())


if __name__ == "__main__":
    main()
