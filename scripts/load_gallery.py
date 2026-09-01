"""
Bulk-load gallery photos/video into GalleryPhoto.

Usage (from your project root, venv active):
    python manage.py shell < scripts/load_gallery.py

Edit SOURCE_DIR below to the absolute path of the folder containing
the files (the output of `pwd` in that terminal), then run the command
above. Safe to re-run — it skips filenames it has already imported.
"""

import os
from django.core.files import File
from travel.models import GalleryPhoto

# EDIT THIS to the absolute path shown by `pwd` in your gallery/ folder
SOURCE_DIR = "/Users/luckythakur/travel_booking_platform/media/gallery"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
VIDEO_EXTENSIONS = (".mp4", ".mov")

already_imported = set(
    GalleryPhoto.objects.exclude(caption="")
    .values_list("caption", flat=True)
)

for fname in sorted(os.listdir(SOURCE_DIR)):
    if fname.startswith("."):
        continue  # skip .DS_Store and similar

    if fname in already_imported:
        print(f"Skipping (already imported): {fname}")
        continue

    full_path = os.path.join(SOURCE_DIR, fname)
    if not os.path.isfile(full_path):
        continue

    lower = fname.lower()

    if lower.endswith(IMAGE_EXTENSIONS):
        with open(full_path, "rb") as f:
            photo = GalleryPhoto(category="CUSTOMER", caption=fname)
            photo.image.save(fname, File(f), save=True)
        print(f"Uploaded photo: {fname} -> id {photo.id}")

    elif lower.endswith(VIDEO_EXTENSIONS):
        with open(full_path, "rb") as f:
            photo = GalleryPhoto(category="CUSTOMER", caption=fname)
            photo.video.save(fname, File(f), save=True)
        print(f"Uploaded video: {fname} -> id {photo.id}")

    else:
        print(f"Skipping unrecognised file type: {fname}")

print("Done.")
