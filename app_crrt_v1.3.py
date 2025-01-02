import streamlit as st

def main():
    st.title("Survival Prediction Tool v1.3")

    # Define variables and their upper limits with labels
    variables = {
        "sex": {"label": "Sex", "default": "Male"},
        "age": {"label": "Age (years)", "default": 5.7},
        "weight": {"label": "Weight (kg)", "default": 16.0},
        "prism_score": {"label": "PRISM Score", "default": 14.0},
        "vis": {"label": "VIS Score", "default": 9.36},
        "picu_stay": {"label": "PICU Stay (days)", "default": 13.0},
        "ventilator": {"label": "Ventilator Usage", "default": "No"},
        "admss": {"label": "Interval from Admission", "default": 18.17},
        "crrt": {"label": "Duration of CRRT (days)", "default": 4.23},
        "fo": {"label": "Fluid Overload", "default": "No"},
        "fo_at_crrt": {"label": "Fluid Overload % at CRRT", "default": 8.12},
        "ph": {"label": "pH Level", "default": 7.33},
        "lactic": {"label": "Lactic Acid (mmol/L)", "default": 2.24},
        "hb": {"label": "Hemoglobin (g/dL)", "default": 9.45},
        "platelet": {"label": "Platelet (103/µL)", "default": 109.54},
        "urine_v": {"label": "Urine Volume (mL/Kg/h)", "default": 0.9},
        "sepsis": {"label": "Sepsis", "default": "No"},
        "alf": {"label": "Acute Liver Failure", "default": "No"},
        "rsd": {"label": "Respiratory System Disease", "default": "No"},
        "albumin": {"label": "Albumin (g/dL)", "default": 3.05},
        "kreatinin": {"label": "Creatinine (mg/dL)", "default": 1.5},
        "pelod": {"label": "PELOD Score", "default": 12.22},
        "psofa": {"label": "pSOFA Score", "default": 9.56},
        "bicarbonate": {"label": "Bicarbonate (mmEq/L)", "default": 21.7},
        "sodium": {"label": "Sodium (mmol/L)", "default": 138.72},
        "potassium": {"label": "Potassium (mmol/L)", "default": 3.61},
        "tls": {"label": "Tumor Lysis Syndrome", "default": "Yes"},
        "hyperammonemia": {"label": "Hyperammonemia", "default": "Yes"}
    }

    # Define correct categorical options
    categorical_options = {
        "sex": ["Male", "Female"],
        "ventilator": ["Yes", "No"],
        "fo": ["Yes", "No"],
        "sepsis": ["Yes", "No"],
        "alf": ["Yes", "No"],
        "rsd": ["Yes", "No"],
        "tls": ["Yes", "No"],
        "hyperammonemia": ["Yes", "No"]
    }

    # Mark significant variables
    significant_variables = ["prism_score", "vis", "ventilator", "fo", "fo_at_crrt", "ph", "lactic", "urine_v", "rsd", "albumin", "pelod", "psofa"]

    # Variables that are correct if higher or same than upper limits
    higher_or_equal_variables = ["ph", "platelet", "urine_v", "albumin", "bicarbonate", "potassium"]

    # Split view into two columns
    col1, col2 = st.columns(2)

    # Input fields for user data
    user_data = {}
    with col1:
        for i, (var, props) in enumerate(variables.items()):
            if i % 2 == 0:  # Variables for column 1
                if var in categorical_options:
                    user_data[var] = st.selectbox(f"{props['label']}", categorical_options[var], index=None)
                else:
                    user_data[var] = st.number_input(f"{props['label']}", value=None, step=0.1, format="%.2f")
    with col2:
        for i, (var, props) in enumerate(variables.items()):
            if i % 2 != 0:  # Variables for column 2
                if var in categorical_options:
                    user_data[var] = st.selectbox(f"{props['label']}", categorical_options[var], index=None)
                else:
                    user_data[var] = st.number_input(f"{props['label']}", value=None, step=0.1, format="%.2f")

    # Calculate score
    if st.button("Calculate"):
        total_variables = 0
        within_limit = 0

        for var, props in variables.items():
            value = user_data[var]
            upper_limit = props['default']
            if value is not None:  # Exclude variables with None values
                if var in categorical_options:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1  # Count significant variables twice
                    if value == upper_limit:  # Check if categorical value matches the correct option
                        within_limit += 1
                        if var in significant_variables:
                            within_limit += 1  # Count significant variables twice
                else:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1  # Count significant variables twice
                    if var in higher_or_equal_variables:
                        if value >= upper_limit:
                            within_limit += 1
                            if var in significant_variables:
                                within_limit += 1
                    else:
                        if value <= upper_limit:
                            within_limit += 1
                            if var in significant_variables:
                                within_limit += 1

        if total_variables > 0:
            final_score = within_limit / total_variables
            st.success(f"The final score is: {final_score:.2f}")
            st.info(f"Total within limit: {within_limit}")
            st.info(f"Total variables considered: {total_variables}")
        else:
            st.warning("No variables included in the calculation.")

if __name__ == "__main__":
    main()
