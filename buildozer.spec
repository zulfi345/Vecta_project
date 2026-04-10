[app]

title = Vecta Kasir
package.name = vectakasir
package.domain = com.vecta.kasir

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 0.1
requirements = python3,kivy,android,sqlite3

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23b
android.arch = arm64-v8a
android.accept_sdk_license = True

log_level = 2
warnings = 1
