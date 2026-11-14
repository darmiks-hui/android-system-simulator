[app]
title = Android System Simulator
package.name = androidsystem
package.domain = org.radmir
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0
requirements = python3==3.11.6,kivy,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.accept_sdk_license = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
