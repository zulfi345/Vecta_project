[app]
title = Vecta Kasir
package.name = vectakasir
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

# versi app
version = 0.2

# library
requirements = python3,kivy==2.2.1,pyjnius

orientation = portrait

# android config
android.api = 33
android.minapi = 21
android.ndk = 25b

# 🔥 PERMISSION LENGKAP (FIX GALERI)
android.permissions = INTERNET

# 🔥 FIX AKSES FILE ANDROID 11+
android.enable_androidx = True
p4a.branch = stable

android.disable_ccache = True
p4a.extra_env_vars = USE_CCACHE=0

log_level = 2
warnings = 1

# icon
icon.filename = icon.png
