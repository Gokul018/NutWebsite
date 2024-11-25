import streamlit as st
from datetime import datetime
import pandas as pd

def main():
    # Configure page settings
    st.set_page_config(
        page_title="30-Day Diet & Workout Plan",
        page_icon="🥗",
        layout="wide"
    )

    # Custom CSS to style the app
    st.markdown("""
        <style>
        .main {
            background-color: #fff5eb;
        }
        .stButton>button {
            background-color: #10b981;
            color: white;
            border-radius: 20px;
            padding: 10px 30px;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #059669;
        }
        div[data-testid="stRadio"] > div {
            display: flex;
            gap: 1rem;
            padding: 10px;
        }
        div[data-testid="stRadio"] > div:first-child {
            background-color: #ffedd5;
            border-radius: 10px;
            padding: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create two columns: one for text and one for the image
    col1, col2 = st.columns([3, 1])  # Adjust the column ratios as needed

    with col1:
        st.markdown("""
            <h1 style='color: black;'>
                Get your 
                <span style='color: #10b981;'>30-Day personalised</span> 
                <span style='color: #f97316;'>Diet & Workout</span> 
                for just
            </h1>
            <h2 style='color: #10b981; font-size: 3em;'>₹499</h2>
        """, unsafe_allow_html=True)

        st.markdown("### Begin your health journey now by providing a few basic details!")

    with col2:
        # Display image in the second column (right side)
        st.image("./assets/iet_img.jfif", width=350)  # Adjust the width as needed

    # Form for user input
    with st.form("diet_plan_form", clear_on_submit=False):
        # Gender selection
        gender = st.selectbox(
            "Select Gender", 
            ["Select Gender", "👨 Male", "👩 Female"]
        )

        # Create three columns for first row of inputs
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.selectbox(
                "Age 📅", 
                options=["Select Age"] + list(range(15, 81)),
                format_func=lambda x: f"{x} years" if isinstance(x, int) else x
            )

        with col2:
            height = st.text_input("Height (in cm) 📏", "")

        with col3:
            weight = st.text_input("Weight (in kg) ⚖️", "")

        # Create three columns for second row of inputs
        col1, col2, col3 = st.columns(3)

        with col1:
            meal_preference = st.selectbox("Meal Preference 🍽️",
                                           ["Select Meal Preference", "Vegetarian", "Non-Vegetarian", "Vegan"])

        with col2:
            activity_level = st.selectbox("Activity Level 🏃‍♂️",
                                          ["Select Activity Level", "Sedentary", "Lightly Active", 
                                           "Moderately Active", "Very Active"])

        with col3:
            objective = st.selectbox("Objective 🎯",
                                     ["Select Objective", "Weight Loss", "Weight Gain", 
                                      "Muscle Gain", "Maintenance"])

        # Submit button inside the form
        submit_button = st.form_submit_button("Create my plan")

    # Check if form has been submitted
    if submit_button:
        # Check if all fields are filled and show error message if not
        if gender == "Select Gender":
            st.error("Please select your gender.")
        elif age == "Select Age":
            st.error("Please select your age.")
        elif not height.isdigit() or int(height) < 140 or int(height) > 220:
            st.error("Please provide a valid height between 140 and 220 cm.")
        elif not weight.isdigit() or int(weight) < 40 or int(weight) > 150:
            st.error("Please provide a valid weight between 40 and 150 kg.")
        elif meal_preference == "Select Meal Preference":
            st.error("Please select your meal preference.")
        elif activity_level == "Select Activity Level":
            st.error("Please select your activity level.")
        elif objective == "Select Objective":
            st.error("Please select your objective.")
        else:
            # Convert height and weight to integers after validation
            height = int(height)
            weight = int(weight)

            # If all fields are filled, proceed with the calculations and display the plan

            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)

            # Calculate basic calorie needs (using Harris-Benedict equation)
            is_male = gender == "👨 Male"
            if is_male:
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

            # Activity multipliers
            activity_multipliers = {
                "Sedentary": 1.2,
                "Lightly Active": 1.375,
                "Moderately Active": 1.55,
                "Very Active": 1.725
            }

            daily_calories = bmr * activity_multipliers[activity_level]

            # Adjust calories based on objective
            if objective == "Weight Loss":
                target_calories = daily_calories - 500
            elif objective in ["Weight Gain", "Muscle Gain"]:
                target_calories = daily_calories + 500
            else:
                target_calories = daily_calories

            # Calculate macronutrient distribution
            protein_cals = target_calories * 0.3
            carb_cals = target_calories * 0.4
            fat_cals = target_calories * 0.3

            protein_g = protein_cals / 4
            carb_g = carb_cals / 4
            fat_g = fat_cals / 9

            # Display the personalized plan
            st.success("Your personalized plan has been created!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Daily Calorie Target", f"{target_calories:.0f} kcal")
                st.metric("BMI", f"{bmi:.1f}")

                st.markdown("### Macronutrient Distribution")
                st.metric("Protein", f"{protein_g:.0f}g")
                st.metric("Carbohydrates", f"{carb_g:.0f}g")
                st.metric("Fats", f"{fat_g:.0f}g")

            with col2:
                st.markdown(f"""
                    ### Your Plan Includes:
                    - Personalized {meal_preference} meal plan
                    - Daily calorie target: {target_calories:.0f} kcal
                    - Protein: {protein_g:.0f}g | Carbs: {carb_g:.0f}g | Fats: {fat_g:.0f}g
                    - Customized workout routine for {objective.lower()}
                    - 30 days of meal and exercise scheduling
                    - Progress tracking tools
                """)

                # Add a payment button (placeholder)
                st.markdown("### Complete Your Purchase")
                if st.button("Pay ₹499"):
                    st.success("Payment button clicked! (Payment integration would go here)")

if __name__ == "__main__":
    main()
