import streamlit as st
import pandas as pd
import math
from io import StringIO

# ==============================================================================
# EquiCut v1.0b
# Entropy-Based Optimal Cutoff Analysis Tool
#
# Implements the method described in:
# Marleau, J., & Garvie, P. (2026). Use of an entropy measure to dichotomize
# a variable. Journal of Psychometric Research, 4(1), 17-25.
# ==============================================================================

# ==============================================================================
# 1. CALCULATION FUNCTIONS (Core logic)
# These functions implement the entropy-based analysis.
# The main function "analyze_data" RETURNS results rather than PRINTING them,
# so they can be displayed through the Streamlit interface.
# ==============================================================================

def calculate_shannon_entropy_and_equitability(counts):
    """
    Calculates the Shannon entropy (H) and equitability (E) for a list of counts.
    
    Parameters:
        counts (list): A list of integer frequency counts per category.
    
    Returns:
        tuple: (shannon_h, equitability_e)
    """
    total_count = sum(counts)
    if total_count == 0:
        return 0, 0

    num_categories = len(counts)
    shannon_h = 0

    for count in counts:
        if count > 0:
            proportion = count / total_count
            shannon_h -= proportion * math.log(proportion)

    if num_categories <= 1:
        equitability_e = 0
    else:
        equitability_e = shannon_h / math.log(num_categories)

    return shannon_h, equitability_e


def analyze_data(data_counts):
    """
    Analyzes the data to find the optimal cutoff point.
    Iterates over all possible dichotomization points and identifies the one
    whose equitability most closely matches the global equitability.

    Parameters:
        data_counts (list): A list of integer frequency counts, one per category,
                            ordered from category 0 upward.

    Returns:
        dict: A dictionary containing global metrics, per-cutoff details,
              and the optimal cutoff result. Returns None on invalid input.
    """
    if not data_counts or len(data_counts) < 2:
        st.error("Error: Data must contain at least two categories for analysis.")
        return None

    num_original_categories = len(data_counts)

    # Calculate global entropy and equitability
    h_global, e_global = calculate_shannon_entropy_and_equitability(data_counts)

    results = []
    # Iterate through all possible cutoff points
    for cutoff_value in range(num_original_categories - 1):
        count_low = sum(data_counts[i] for i in range(cutoff_value + 1))
        count_high = sum(data_counts[i] for i in range(cutoff_value + 1, num_original_categories))

        dichotomized_counts = [count_low, count_high]

        if count_low == 0 or count_high == 0:
            h_cutoff, e_cutoff = 0, 0
        else:
            h_cutoff, e_cutoff = calculate_shannon_entropy_and_equitability(dichotomized_counts)

        absolute_difference = abs(e_global - e_cutoff)

        results.append({
            "Cutoff Point": f"{cutoff_value}/{cutoff_value + 1}",
            "H (Cutoff)": h_cutoff,
            "E (Cutoff)": e_cutoff,
            "Absolute Difference (E)": absolute_difference
        })

    # Find the optimal cutoff point (minimum absolute difference)
    optimal_result = min(results, key=lambda x: x["Absolute Difference (E)"])

    # Return a dictionary containing all results
    return {
        "num_categories": num_original_categories,
        "h_global": h_global,
        "e_global": e_global,
        "detailed_results": results,
        "optimal_result": optimal_result
    }


# ==============================================================================
# 2. STREAMLIT USER INTERFACE
# Builds the interactive web page for EquiCut v1.0b.
# ==============================================================================

st.set_page_config(layout="wide", page_title="EquiCut v1.0b — Entropy Analysis")

st.title("EquiCut v1.0b — Equitability-Entropy-Based Optimal Cutoff Analysis Tool")
st.markdown("""
This application implements the method described in:
*Marleau, J., & Garvie, P. (2026). Use of an entropy measure to dichotomize a variable.
Journal of Psychometric Research, 4(1), 17–25.*

It determines the optimal cutoff point for an ordinal variable using information theory.
""")

# --- Sidebar Instructions ---
st.sidebar.header("Instructions")
st.sidebar.info(
    """
    1. **Prepare your data file**: It must be a plain text file (`.txt`) containing
       a single column of integers. Each line represents the number of cases (frequency)
       for one category, starting from category 0.
    2. **Upload the file** using the button below.
    3. **Click "Run Analysis"**.
    4. **Review the results** displayed on the page.
    5. **Download the results** using the button that appears at the bottom of the page.
    """
)

# --- Step A: File Upload ---
uploaded_file = st.file_uploader("1. Choose your data file (.txt)", type="txt")

if uploaded_file is not None:
    try:
        # Read and validate the data
        string_data = uploaded_file.getvalue().decode("utf-8")
        lines = string_data.strip().split('\n')
        counts = [int(line.strip()) for line in lines if line.strip()]

        st.success(f"File uploaded successfully. {len(counts)} categories detected.")

        # Preview the raw uploaded data
        with st.expander("Show raw uploaded data"):
            st.text(string_data)

        # --- Step B: Analysis Button ---
        if st.button("2. Run Analysis", type="primary"):

            # --- Step C: Run analysis and display results ---
            analysis_results = analyze_data(counts)

            if analysis_results:
                st.header("Analysis Results")

                # Global results
                st.subheader("Global Results")
                col1, col2, col3 = st.columns(3)
                col1.metric("Number of Categories", f"{analysis_results['num_categories']}")
                col2.metric("Global Entropy (H)", f"{analysis_results['h_global']:.4f}")
                col3.metric("Global Equitability (E)", f"{analysis_results['e_global']:.4f}")

                # Optimal cutoff result
                st.subheader("Optimal Cutoff Point")
                optimal = analysis_results['optimal_result']
                st.success(f"**The optimal cutoff point is: {optimal['Cutoff Point']}**")

                col_opt1, col_opt2 = st.columns(2)
                col_opt1.metric("Equitability at This Cutoff", f"{optimal['E (Cutoff)']:.4f}")
                col_opt2.metric("Minimum Absolute Difference from Global Equitability", f"{optimal['Absolute Difference (E)']:.4f}")

                # Detailed results table
                st.subheader("Details for Each Cutoff Point")
                results_df = pd.DataFrame(analysis_results['detailed_results'])
                st.dataframe(results_df.style.highlight_min(subset=['Absolute Difference (E)'], color='lightgreen'))

                # --- Step D: Download Option ---
                st.header("Download Results")

                # Prepare the text file content for download
                output_string = StringIO()
                output_string.write("EQUICUT v1.0b — ENTROPY-BASED OPTIMAL CUTOFF ANALYSIS\n")
                output_string.write("=" * 55 + "\n\n")
                output_string.write("GLOBAL RESULTS\n")
                output_string.write(f"Number of original categories: {analysis_results['num_categories']}\n")
                output_string.write(f"Global Entropy (H): {analysis_results['h_global']:.4f}\n")
                output_string.write(f"Global Equitability (E): {analysis_results['e_global']:.4f}\n\n")
                output_string.write("OPTIMAL CUTOFF POINT\n")
                output_string.write(f"Cutoff point: {optimal['Cutoff Point']}\n")
                output_string.write(f"Equitability at this cutoff: {optimal['E (Cutoff)']:.4f}\n")
                output_string.write(f"Minimum absolute difference: {optimal['Absolute Difference (E)']:.4f}\n\n")
                output_string.write("FULL DETAILS\n")
                results_df.to_csv(output_string, index=False, sep='\t')

                st.download_button(
                    label="📥 Download results file (.txt)",
                    data=output_string.getvalue().encode('utf-8'),
                    file_name="equicut_analysis_results.txt",
                    mime="text/plain"
                )

    except Exception as e:
        st.error(
            f"Error reading or processing the file. Please verify your file format. "
            f"Error details: {e}"
        )
