[app]

title = Vecta Kasir
package.name = vectakasir
package.domain = org.vecta.kasir
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy

orientation = portrait

android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 23c
android.sdk = 30
android.arch = arm64-v8a
android.accept_sdk_license = True

log_level = 2
warnings = True

[buildozer]

log_level = 2
warnings = True
