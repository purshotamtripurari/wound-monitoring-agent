import cv2
from pathlib import Path
import shutil

# CHANGE THIS PATH
SOURCE = Path(r"C:\Users\Dell\Downloads\wound-segmentation-master\wound-segmentation-master\data\Foot Ulcer Segmentation Challenge")

# Our new YOLO dataset
OUTPUT = Path("dataset")

splits = ["train", "validation"]

for split in splits:

    image_source = SOURCE / split / "images"
    mask_source = SOURCE / split / "labels"

    image_output = OUTPUT / "images" / split
    label_output = OUTPUT / "labels" / split

    image_output.mkdir(parents=True, exist_ok=True)
    label_output.mkdir(parents=True, exist_ok=True)

    print(f"\nProcessing {split}...")

    count = 0

    for image_path in image_source.iterdir():

        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        mask_path = mask_source / (image_path.stem + ".png")

        if not mask_path.exists():
            print(f"Mask not found: {mask_path.name}")
            continue

        # Read mask
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

        if mask is None:
            print(f"Could not read mask: {mask_path}")
            continue

        # Convert white region to binary
        _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        # Find wound boundary
        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:
            print(f"No wound found in: {image_path.name}")
            continue

        # Use largest contour
        contour = max(contours, key=cv2.contourArea)

        height, width = mask.shape

        # Convert contour points to normalized YOLO coordinates
        points = []

        for point in contour:

            x, y = point[0]

            x_normalized = x / width
            y_normalized = y / height

            points.append(f"{x_normalized:.6f}")
            points.append(f"{y_normalized:.6f}")

        # YOLO segmentation format
        label_text = "0 " + " ".join(points)

        # Save label
        label_file = label_output / f"{image_path.stem}.txt"

        with open(label_file, "w") as f:
            f.write(label_text)

        # Copy image
        shutil.copy2(
            image_path,
            image_output / image_path.name
        )

        count += 1

    print(f"{split}: {count} images converted.")

print("\nConversion completed!")