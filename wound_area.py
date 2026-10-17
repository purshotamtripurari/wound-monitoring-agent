from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("runs/segment/train/weights/best.pt")

# Image to analyze
image_path = "test_images/0812.png"

# Run YOLO
results = model(image_path)

for result in results:

    if result.masks is None:
        print("No wound detected.")
        continue

    # Get segmentation masks
    masks = result.masks.data.cpu().numpy()

    # Calculate area of each mask
    for i, mask in enumerate(masks):

        # Convert mask to binary
        binary_mask = (mask > 0.5).astype("uint8")

        # Count wound pixels
        area_pixels = binary_mask.sum()

        print(f"Wound {i + 1}")
        print(f"Wound area: {area_pixels} pixels")