from ultralytics import YOLO
from pathlib import Path
import matplotlib.pyplot as plt
from agent import analyze_wound_progress

# Load trained YOLO model
model = YOLO("runs/segment/train/weights/best.pt")

# Monitoring folders
days = {
    "Day 1": Path("monitoring/day1"),
    "Day 7": Path("monitoring/day7"),
    "Day 14": Path("monitoring/day14")
}

areas = {}

for day, folder in days.items():

    images = list(folder.glob("*.png")) + list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg"))

    if not images:
        print(f"{day}: No image found")
        continue

    image = images[0]

    print(f"\nProcessing {day}: {image.name}")

    results = model(str(image), verbose=False)

    total_area = 0

    for result in results:

        if result.masks is None:
            continue

        masks = result.masks.data.cpu().numpy()

        for mask in masks:

            binary_mask = (mask > 0.5).astype("uint8")

            area = binary_mask.sum()

            total_area += area

    areas[day] = total_area

    print(f"{day} wound area: {total_area} pixels")


# Compare areas
print("\n==============================")
print("WOUND MONITORING SUMMARY")
print("==============================")

for day, area in areas.items():
    print(f"{day}: {area} pixels")


if "Day 1" in areas:

    initial_area = int(areas["Day 1"])

    for day, area in areas.items():

        if day == "Day 1":
            continue

        area = int(area)

        change = ((initial_area - area) / initial_area) * 100

        if change > 0:
            print(f"{day}: Wound area decreased by {change:.2f}%")

        elif change < 0:
            print(f"{day}: Wound area increased by {abs(change):.2f}%")

        else:
            print(f"{day}: Wound area unchanged")
# Create progress graph

if len(areas) >= 2:

    day_names = list(areas.keys())
    area_values = [int(value) for value in areas.values()]

    plt.figure(figsize=(8, 5))

    plt.plot(day_names, area_values, marker="o")

    plt.title("Wound Area Progress")
    plt.xlabel("Time")
    plt.ylabel("Wound Area (pixels)")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig("wound_progress.png")

    print("\nProgress graph saved as:")
    print("wound_progress.png")

    plt.show()
analyze_wound_progress(areas)