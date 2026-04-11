[app]
title = Vecta Kasir
package.name = vectakasir
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

# 🔥 NAIKKAN VERSION (biar bisa update APK)
version = 0.2

# 🔥 TAMBAH PLYER
requirements = python3,kivy,plyer

orientation = portrait

# 🔥 ANDROID STABLE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2

# 🔥 PERMISSION STORAGE
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 🔥 ICON (WAJIB SESUAI NAMA FILE)
icon.filename = icon.png
