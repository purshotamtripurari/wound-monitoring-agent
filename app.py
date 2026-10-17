
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import matplotlib.pyplot as plt
from datetime import date, timedelta

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Wound Monitoring Agent",
    page_icon="🩹",
    layout="centered"
)

st.title("🩹 Wound Monitoring Agent")
st.write("YOLO-based wound segmentation and temporal monitoring")

st.info(
    "This system provides image-based monitoring information "
    "and is not a medical diagnosis."
)

# ==========================================
# LOAD YOLO MODEL
# ==========================================

@st.cache_resource
def load_model():
    return YOLO("models/best.pt")


model = load_model()

# ==========================================
# CALCULATE WOUND AREA
# ==========================================

def calculate_wound_area(image):
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ) as temp_file:
            temp_path = temp_file.name
            image.save(temp_path)

        results = model(temp_path, verbose=False)
        total_area = 0

        for result in results:
            if result.masks is not None:
                masks = result.masks.data.cpu().numpy()

                for mask in masks:
                    binary_mask = (mask > 0.5).astype("uint8")
                    total_area += int(binary_mask.sum())

        return total_area

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ==========================================
# OBSERVATION SETTINGS
# ==========================================

st.subheader("📅 Wound Observations")

number_of_observations = st.number_input(
    "Number of observations",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

first_date = st.date_input(
    "Observation 1 date",
    value=date.today()
)

st.caption(
    "Follow-up observations are automatically scheduled "
    "7 days apart."
)

# ==========================================
# OBSERVATION INPUTS
# ==========================================

observations = []

for i in range(int(number_of_observations)):
    observation_date = first_date + timedelta(days=i * 7)

    st.markdown(f"### Observation {i + 1}")
    st.write(f"📅 Date: **{observation_date}**")

    uploaded_file = st.file_uploader(
        f"Upload wound image for Observation {i + 1}",
        type=["png", "jpg", "jpeg"],
        key=f"image_{i}"
    )

    observations.append({
        "date": observation_date,
        "file": uploaded_file
    })


# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("🔍 Analyze Wound Progress"):

    results_data = []

    # Process uploaded images
    for observation in observations:
        if observation["file"] is None:
            continue

        try:
            image = Image.open(
                observation["file"]
            ).convert("RGB")

            area = calculate_wound_area(image)

            results_data.append({
                "date": observation["date"],
                "area": area,
                "image": image
            })

        except Exception as error:
            st.error(
                f"Could not process an uploaded image: {error}"
            )

    # ==========================================
    # CHECK UPLOADS
    # ==========================================

    if len(results_data) == 0:
        st.warning("Please upload at least one valid wound image.")

    else:

        # ==========================================
        # MEASUREMENTS DASHBOARD
        # ==========================================

        st.divider()
        st.subheader("📊 Wound Measurements Dashboard")
        st.subheader("📋 Measurement Summary")

        summary_rows = []

        for i, observation in enumerate(results_data):
            if i == 0:
                change_text = "Baseline"
            else:
                previous_area = results_data[i - 1]["area"]
                current_area = observation["area"]

                if previous_area > 0:
                    change_percent = (
                        (current_area - previous_area)
                        / previous_area
                    ) * 100
                    change_text = f"{change_percent:+.2f}%"
                else:
                    change_text = "N/A"

            summary_rows.append({
                "Observation": i + 1,
                "Date": observation["date"],
                "Wound Area (pixels)": observation["area"],
                "Change from Previous": change_text
            })

        st.dataframe(
            summary_rows,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==========================================
        # INDIVIDUAL OBSERVATIONS
        # ==========================================

        for i, observation in enumerate(results_data):
            st.markdown(f"### 🩹 Observation {i + 1}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📅 Date: **{observation['date']}**")

                st.metric(
                    "Wound Area",
                    f"{observation['area']:,} pixels"
                )

                if i == 0:
                    st.caption("Initial observation (baseline)")
                else:
                    previous_area = results_data[i - 1]["area"]
                    current_area = observation["area"]

                    if previous_area > 0:
                        change = (
                            (current_area - previous_area)
                            / previous_area
                        ) * 100

                        st.metric(
                            "Change from Previous Observation",
                            f"{abs(change):.2f}%",
                            delta=f"{change:+.2f}% area change",
                            delta_color="inverse"
                        )
                    else:
                        st.caption(
                            "Cannot calculate change because "
                            "the previous area is zero."
                        )

            with col2:
                st.image(
                    observation["image"],
                    caption=f"Observation {i + 1}",
                    width=300
                )

            st.divider()

        # ==========================================
        # PROGRESS ANALYSIS
        # ==========================================

        if len(results_data) >= 2:
            dates = [
                str(item["date"])
                for item in results_data
            ]

            areas = [
                item["area"]
                for item in results_data
            ]

            initial_area = areas[0]
            latest_area = areas[-1]

            # Overall change
            st.subheader("📈 Overall Progress")

            if initial_area > 0:
                overall_change = (
                    (initial_area - latest_area)
                    / initial_area
                ) * 100

                if overall_change > 0:
                    st.success(
                        f"Measured wound area decreased by "
                        f"{overall_change:.2f}% from the first "
                        f"to the latest observation."
                    )
                elif overall_change < 0:
                    st.warning(
                        f"Measured wound area increased by "
                        f"{abs(overall_change):.2f}% from the first "
                        f"to the latest observation."
                    )
                else:
                    st.info("Measured wound area remained unchanged.")

                # Graph
                st.subheader("📊 Wound Area Progress")

                fig, ax = plt.subplots(figsize=(9, 5))
                ax.plot(dates, areas, marker="o")
                ax.set_title("Wound Area Progress")
                ax.set_xlabel("Observation Date")
                ax.set_ylabel("Wound Area (pixels)")
                ax.tick_params(axis="x", rotation=45)
                ax.grid(True)
                fig.tight_layout()

                st.pyplot(fig)
                plt.close(fig)

                # Consecutive analysis
                st.subheader(
                    "🔄 Observation-to-Observation Analysis"
                )

                significant_changes = []

                for i in range(1, len(areas)):
                    previous_area = areas[i - 1]
                    current_area = areas[i]

                    if previous_area == 0:
                        st.warning(
                            f"{dates[i]}: Previous measured area was "
                            "zero; percentage change cannot be calculated."
                        )
                        continue

                    consecutive_change = (
                        (current_area - previous_area)
                        / previous_area
                    ) * 100

                    if consecutive_change > 0:
                        st.warning(
                            f"{dates[i]}: Measured area increased by "
                            f"{consecutive_change:.2f}% compared with "
                            f"{dates[i - 1]}."
                        )
                    elif consecutive_change < 0:
                        st.info(
                            f"{dates[i]}: Measured area decreased by "
                            f"{abs(consecutive_change):.2f}% compared "
                            f"with {dates[i - 1]}."
                        )
                    else:
                        st.write(
                            f"{dates[i]}: Measured area remained unchanged."
                        )

                    if abs(consecutive_change) > 50:
                        significant_changes.append({
                            "date": dates[i],
                            "change": consecutive_change
                        })

                # Significant changes
                st.subheader("⚠️ Significant Measurement Changes")

                if significant_changes:
                    for item in significant_changes:
                        change_value = item["change"]

                        if change_value > 0:
                            st.warning(
                                f"{item['date']}: Measurement increased "
                                f"by {change_value:.2f}%."
                            )
                        else:
                            st.warning(
                                f"{item['date']}: Measurement decreased "
                                f"by {abs(change_value):.2f}%."
                            )

                    st.caption(
                        "Large changes may reflect actual wound changes "
                        "or differences in image angle, lighting, distance, "
                        "or segmentation accuracy."
                    )
                else:
                    st.success(
                        "No measurement change greater than 50% "
                        "was detected between consecutive observations."
                    )

                # AI monitoring summary
                st.subheader("🤖 AI Monitoring Summary")

                if overall_change > 0:
                    st.write(
                        f"The measured wound area decreased by "
                        f"{overall_change:.2f}% between the first and "
                        "latest observations."
                    )
                elif overall_change < 0:
                    st.write(
                        f"The measured wound area increased by "
                        f"{abs(overall_change):.2f}% between the first "
                        "and latest observations."
                    )
                else:
                    st.write(
                        "The measured wound area remained unchanged "
                        "between the first and latest observations."
                    )

            else:
                st.warning(
                    "Initial measured area is zero, so overall "
                    "percentage change cannot be calculated."
                )

        # ==========================================
        # DISCLAIMER
        # ==========================================

        st.caption(
            "Pixel measurements are image-based estimates, not real-world "
            "area measurements or a clinically validated healing assessment. "
            "This tool does not replace professional medical advice."
        )
