[app]
title = Vecta Kasir
package.name = vectakasir
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv

version = 0.2

requirements = python3,kivy,plyer

orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools = 33.0.2

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.enable_androidx = True

icon.filename = icon.png
