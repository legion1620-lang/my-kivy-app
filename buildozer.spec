[app]
title = Word Card App
package.name = wordcardapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

# Задаем фиксированные и стабильные версии
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
