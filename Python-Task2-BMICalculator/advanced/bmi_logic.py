def calculate_bmi(weight, height):
    return weight / (height ** 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def get_category_color(category):
    colors = {
        "Underweight": "orange",
        "Normal": "green",
        "Overweight": "orange",
        "Obese": "red"
    }

    return colors.get(category, "black")
