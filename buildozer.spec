[app]

# (str) Title of your application
title = Vecta Kasir

# (str) Package name
package.name = vectakasir

# (str) Package domain (needs to be unique)
package.domain = org.vecta.kasir

# (str) Version code (Wajib diisi!)
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include/ignore
source.include_exts = py,png,jpg,kv,atlas

# (list) Requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (list) Android permissions
android.permissions = INTERNET

# (int) Android API to use (SDK version)
android.api = 33

# (int) Minimum API version
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android architecture
android.arch = arm64-v8a

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Log level
log_level = 2

# (bool) Show warnings
warnings = True

[buildozer]

# (int) Log level
log_level = 2

# (bool) Show warnings
warnings = True
