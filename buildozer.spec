[app]
title = JARVIS
package.name = jarvis
package.domain = org.aditya.jarvis
source.dir = .
source.include_exts = py,kv,txt
version = 0.1
requirements = python3,kivy,requests,pyjnius
orientation = portrait
fullscreen = 0

[android]
permissions = INTERNET,RECORD_AUDIO
android.api = 35
android.build_tools_version = 33.0.2
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
