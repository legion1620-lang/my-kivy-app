[app]
title = Word Card App
package.name = wordcardapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
[buildozer]
log_level = 2
warn_on_root = 1
