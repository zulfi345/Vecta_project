[app]
title = Vecta Kasir
package.name = vectakasir
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

version = 0.2

requirements = python3,kivy,plyer,pybluez

orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.enable_androidx = True
p4a.branch = master

android.disable_ccache = True
p4a.extra_env_vars = USE_CCACHE=0

log_level = 2
warnings = 1

icon.filename = icon.png
