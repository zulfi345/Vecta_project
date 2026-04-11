[app]
title = Vecta Kasir
package.name = vectakasir
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

# versi app
version = 0.2

# library
requirements = python3,kivy,cython

orientation = portrait

# android config
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2

# 🔥 PERMISSION LENGKAP (FIX GALERI)
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 🔥 FIX AKSES FILE ANDROID 11+
android.enable_androidx = True

# icon
icon.filename = icon.png
