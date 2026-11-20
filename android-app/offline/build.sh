#!/usr/bin/env bash
# Builds the self-contained Aoi Teacher APK: copies the current web app (../../aoi-teacher) into
# the APK's assets and signs it. Needs the Android SDK (ANDROID_HOME) and Gradle 8.11+.
# Signing: AOI_KEYSTORE=/path/to.keystore AOI_KEYSTORE_PASS=... [AOI_KEY_ALIAS=android]
# Optional: AOI_VERSION_CODE / AOI_VERSION_NAME, GRADLE_ARGS (e.g. --offline).
set -euo pipefail
cd "$(dirname "$0")"
: "${AOI_KEYSTORE:?set AOI_KEYSTORE to your signing keystore}"
: "${AOI_KEYSTORE_PASS:?set AOI_KEYSTORE_PASS}"
rm -rf app/src/main/assets/www
mkdir -p app/src/main/assets/www
cp -r ../../aoi-teacher/index.html ../../aoi-teacher/manifest.json ../../aoi-teacher/icons \
      ../../aoi-teacher/sprites ../../aoi-teacher/audio ../../aoi-teacher/images app/src/main/assets/www/
mkdir -p app/src/main/assets/www/phrasebook
cp ../../aoi-teacher/phrasebook/phrasebook.js app/src/main/assets/www/phrasebook/
mkdir -p app/src/main/assets/www/grammar
cp ../../aoi-teacher/grammar/japanese.js app/src/main/assets/www/grammar/
# Drafts and notes inside the audio folder are not app content.
find app/src/main/assets/www -name '*.md' -delete
python3 make_icons.py
echo "sdk.dir=${ANDROID_HOME:-/opt/android-sdk}" > local.properties
gradle ${GRADLE_ARGS:-} --no-daemon assembleRelease
cp app/build/outputs/apk/release/app-release.apk ./AoiTeacher.apk
echo "Built $(pwd)/AoiTeacher.apk"
