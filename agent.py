def analyze_wound_progress(areas):

    print("\n================================")
    print("AI WOUND MONITORING AGENT")
    print("================================")

    if len(areas) < 2:
        print("Not enough observations for trend analysis.")
        return

    # Convert values to normal integers
    areas = {day: int(area) for day, area in areas.items()}

    first_day = list(areas.keys())[0]
    last_day = list(areas.keys())[-1]

    initial_area = areas[first_day]
    latest_area = areas[last_day]

    change = ((initial_area - latest_area) / initial_area) * 100

    print(f"\nInitial observation: {first_day}")
    print(f"Initial wound area: {initial_area} pixels")

    print(f"\nLatest observation: {last_day}")
    print(f"Latest wound area: {latest_area} pixels")

    print(f"\nOverall change: {change:.2f}%")

    if change > 0:
        print("\nTrend: Wound area decreased.")

    elif change < 0:
        print("\nTrend: Wound area increased.")

    else:
        print("\nTrend: Wound area remained unchanged.")

    # Check each consecutive observation
    days = list(areas.keys())

    print("\nObservation analysis:")

    for i in range(1, len(days)):

        previous_day = days[i - 1]
        current_day = days[i]

        previous_area = areas[previous_day]
        current_area = areas[current_day]

        percentage = (
            (previous_area - current_area)
            / previous_area
        ) * 100

        if percentage > 0:
            print(
                f"{current_day}: area decreased "
                f"by {percentage:.2f}% from {previous_day}."
            )

        elif percentage < 0:
            print(
                f"{current_day}: area increased "
                f"by {abs(percentage):.2f}% from {previous_day}."
            )

        else:
            print(
                f"{current_day}: area remained "
                f"unchanged from {previous_day}."
            )

    print("\nAI Monitoring Summary:")

    if change > 0:
        print(
            "The measured wound area is smaller in the "
            "latest observation compared with the initial observation."
        )

    elif change < 0:
        print(
            "The measured wound area is larger in the "
            "latest observation compared with the initial observation."
        )

    else:
        print(
            "The measured wound area is approximately unchanged "
            "compared with the initial observation."
        )

    print(
        "\nNote: This system provides image-based monitoring "
        "information and is not a medical diagnosis."
    )