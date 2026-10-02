[app]

title = Kanal Marla Calculator
package.name = kanalmarla
package.domain = org.wajahat

source.dir = .
source.include_exts = py,json,png,jpg,kv

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1


[android]

android.api = 35
android.minapi = 21

android.ndk = 28c

android.archs = arm64-v8a

android.enable_androidx = True

android.accept_sdk_license = True
