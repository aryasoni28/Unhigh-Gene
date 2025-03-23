import streamlit as st
import base64
import pandas as pd
from pathlib import Path
import re

# Define function to generate complementary strand
def generate_complementary_strand(dna_strand):
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complementary_strand = ''
    
    for base in dna_strand:
        complementary_strand += complement_dict.get(base, base)
    
    return complementary_strand[::-1]

# Define function to read txt file and clean the DNA sequence
def read_txt_file(file):
    if isinstance(file, str):
        with open(file, 'r') as f:
            sequence = f.read().strip()
    else:
        sequence = file.getvalue().decode('utf-8').strip()
    return sequence

# Define function to predict results based on genetic sequences and selected disease
def predict_results(disease, father_sequence, mother_sequence, paternal_grandfather_sequence, paternal_grandmother_sequence, maternal_grandfather_sequence, maternal_grandmother_sequence):
    # Placeholder prediction logic
    if disease == "Huntington's Disease":
        prediction = "Prediction Placeholder for Huntington's Disease"
    elif disease == "Sickle Cell Anemia":
        prediction = "Prediction Placeholder for Sickle Cell Anemia"
    elif disease == "Muscular Dystrophy":
        prediction = "Prediction Placeholder for Muscular Dystrophy"
    else:
        prediction = "Prediction Placeholder for other diseases"

    return prediction

# Define function to check Huntingtin sequence
def check_huntingtin_sequence(sequence):
    cleaned_sequence = sequence.upper().replace(" ", "")
    
    # Find all occurrences of consecutive CAG repeats
    cag_counts = [len(match.group(0)) // 3 for match in re.finditer(r'(CAG)+', cleaned_sequence)]
    
    # Return the maximum count
    c_count = max(cag_counts, default=0)
    if c_count > 35:
        return 1
    elif c_count < 35:
        return 0

# Define function to check Duchenne Muscular Dystrophy sequence
def check_dmd_sequence(sequence):
    """
    Checks if the given DNA sequence is associated with Duchenne Muscular Dystrophy (DMD).

    Args:
        sequence (str): The DNA sequence.

    Returns:
        bool: True if the sequence is associated with DMD, False otherwise.
    """
    # Remove any spaces or special characters from the sequence
    cleaned_sequence = sequence.upper().replace(" ", "")

    # Check for nonsense mutations (stop codons)
    for i in range(0, len(cleaned_sequence), 3):
        codon = cleaned_sequence[i:i+3]
        if codon == "TGA" or codon == "TAG" or codon == "TAA":
            return 1

    # Check for deletions
    deletion_pattern = "---"
    if deletion_pattern in cleaned_sequence:
        return 1

    # Check for insertions
    prev_len = len(cleaned_sequence)
    cleaned_sequence = cleaned_sequence.replace("+", "")
    if len(cleaned_sequence) != prev_len:
        return 1

    # If no matches found, return False
    return 0

# Define function to check Sickle Cell Anemia sequence
def check_sickle_cell_sequence(genetic_sequence):
    # Find the index of the first occurrence of ATG
    start_index = genetic_sequence.find("ATG")
    
    # Check if ATG is found
    if start_index != -1:
        # Calculate the position of the 17th nucleotide after ATG
        target_position = start_index + 14  # ATG counts as the first triplet
        
        # Check if the sequence is long enough to reach the target position
        if len(genetic_sequence) > target_position:
            nucleotide = genetic_sequence[target_position]
            if nucleotide=='T':
                return 1
            else:
                return 0
    return 0

def generate_punnett_square(parent1, parent2):
    punnett_square = []
    for gene1 in parent1:
        for gene2 in parent2:
            punnett_square.append(gene1 + gene2)
    return punnett_square


def homepage():
    #st.set_page_config(page_title="Unhigh-Gene", page_icon=":dna:", layout="wide")

    # Add background image
    current_dir = Path(__file__).parent
    background_image = current_dir / "background.jpg"
    with open(background_image, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode()

    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
    }}
    .stMarkdown, .stTitle {{
        color: white; /* Set text color to white */
    }}
    .stButton > button {{
        color: orange; /* Set button text color to orange */
    }}
    </style>
    """

    st.markdown(background_style, unsafe_allow_html=True)
    st.markdown('<h1 style="color:white;">Welcome to Unhigh-Gene</h1>', unsafe_allow_html=True)

    # Website description
    description = "Unhigh-Gene analyzes both parental and grandparental genetic data and provides comprehensive disease predictions, empowering couples to make informed decisions about family planning and prevent the transmission of genetic disorders to their offspring."
    st.markdown(f'<p style="color:white; text-align:center;">{description}</p>', unsafe_allow_html=True)

    # Button to redirect to the main page
    if st.button("Unhigh-Gene"):
        st.session_state['page'] = 'gene'
    
    st.video("Unhigh-Gene.mp4")

def gene():
    st.set_page_config(page_title="Unhigh-Gene", page_icon=":dna:", layout="wide")
    st.markdown('<h1 style="color:white;">Welcome to Unhigh-Gene</h1>', unsafe_allow_html=True)

    # Add background image
    current_dir = Path(__file__).parent
    background_image = current_dir / "background.jpg"
    with open(background_image, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode()

    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
    }}
    .stMarkdown, .stTitle, .stFileUploader > div > div > div > div {{
        color: white; /* Set text color to white */
    }}
    .stFileUploader > div > div > div > div {{
        color: black; /* Set input text color to black */
    }}
    </style>
    """

    st.markdown(background_style, unsafe_allow_html=True)

    show_predictions = False

    # Predictions page
    if not show_predictions:
        st.write("Welcome to the Unhigh-Gene Prediction tool. Please select the disease and upload the genetic sequences of the father, mother, and all four grandparents below.")

        # Dropdown for disease selection
        disease_options = ["Huntington's Disease", "Sickle Cell Anemia", "Muscular Dystrophy"]
        disease = st.selectbox("Select Disease:", disease_options)

        # File uploader for genetic sequences
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write("Upload Father's Genetic Sequence:")
                father_sequence_file = st.file_uploader("Upload file", type=['txt'], key="father_sequence")
                if father_sequence_file is not None:
                    father_sequence = read_txt_file(father_sequence_file)
                    father_complement = generate_complementary_strand(father_sequence)
                    st.write("Father's Complementary Sequence:", father_complement)
            with col2:
                st.write("Upload Mother's Genetic Sequence:")
                mother_sequence_file = st.file_uploader("Upload file", type=['txt'], key="mother_sequence")
                if mother_sequence_file is not None:
                    mother_sequence = read_txt_file(mother_sequence_file)
                    mother_complement = generate_complementary_strand(mother_sequence)
                    st.write("Mother's Complementary Sequence:", mother_complement)
        
        with st.container():
            col3, col4 = st.columns(2)
            with col3:
                st.write("Upload Paternal Grandfather's Genetic Sequence:")
                paternal_grandfather_sequence_file = st.file_uploader("Upload file", type=['txt'], key="paternal_grandfather_sequence")
                if paternal_grandfather_sequence_file is not None:
                    paternal_grandfather_sequence = read_txt_file(paternal_grandfather_sequence_file)
                    paternal_grandfather_complement = generate_complementary_strand(paternal_grandfather_sequence)
                    st.write("Paternal Grandfather's Complementary Sequence:", paternal_grandfather_complement)
                st.write("Upload Paternal Grandmother's Genetic Sequence:")
                paternal_grandmother_sequence_file = st.file_uploader("Upload file", type=['txt'], key="paternal_grandmother_sequence")
                if paternal_grandmother_sequence_file is not None:
                    paternal_grandmother_sequence = read_txt_file(paternal_grandmother_sequence_file)
                    paternal_grandmother_complement = generate_complementary_strand(paternal_grandmother_sequence)
                    st.write("Paternal Grandmother's Complementary Sequence:", paternal_grandmother_complement)
            with col4:
                st.write("Upload Maternal Grandfather's Genetic Sequence:")
                maternal_grandfather_sequence_file = st.file_uploader("Upload file", type=['txt'], key="maternal_grandfather_sequence")
                if maternal_grandfather_sequence_file is not None:
                    maternal_grandfather_sequence = read_txt_file(maternal_grandfather_sequence_file)
                    maternal_grandfather_complement = generate_complementary_strand(maternal_grandfather_sequence)
                    st.write("Maternal Grandfather's Complementary Sequence:", maternal_grandfather_complement)
                st.write("Upload Maternal Grandmother's Genetic Sequence:")
                maternal_grandmother_sequence_file = st.file_uploader("Upload file", type=['txt'], key="maternal_grandmother_sequence")
                if maternal_grandmother_sequence_file is not None:
                    maternal_grandmother_sequence = read_txt_file(maternal_grandmother_sequence_file)
                    maternal_grandmother_complement = generate_complementary_strand(maternal_grandmother_sequence)
                    st.write("Maternal Grandmother's Complementary Sequence:", maternal_grandmother_complement)

        if all([father_sequence_file, mother_sequence_file, paternal_grandfather_sequence_file, paternal_grandmother_sequence_file, maternal_grandfather_sequence_file, maternal_grandmother_sequence_file]):
            show_predictions = True

    # Predictions
    if show_predictions:
        st.markdown('<h1 style="color:white;">Unhigh-Gene Prediction</h1>', unsafe_allow_html=True)

        # Button to trigger prediction
        if st.button("Predict Results"):
            prediction = predict_results(disease, father_sequence, mother_sequence, paternal_grandfather_sequence, paternal_grandmother_sequence, maternal_grandfather_sequence, maternal_grandmother_sequence)
            st.write("Prediction:", prediction)

            # Store data in a CSV file
            data = {
                "Disease": disease,
                "Father's Gene": father_sequence,
                "Father's Complement": father_complement,
                "Mother's Gene": mother_sequence,
                "Mother's Complement": mother_complement,
                "Paternal Grandfather's Gene": paternal_grandfather_sequence,
                "Paternal Grandfather's Complement": paternal_grandfather_complement,
                "Paternal Grandmother's Gene": paternal_grandmother_sequence,
                "Paternal Grandmother's Complement": paternal_grandmother_complement,
                "Maternal Grandfather's Gene": maternal_grandfather_sequence,
                "Maternal Grandfather's Complement": maternal_grandfather_complement,
                "Maternal Grandmother's Gene": maternal_grandmother_sequence,
                "Maternal Grandmother's Complement": maternal_grandmother_complement
            }
            df = pd.DataFrame(data, index=[0])

            # Append to existing CSV if it exists
            csv_file_path = "genetic_data.csv"
            if Path(csv_file_path).is_file():
                existing_df = pd.read_csv(csv_file_path)
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_csv(csv_file_path, index=False)

        # Button to view results
        if st.button("View Results"):
            # Read the CSV file
            csv_file_path = "genetic_data.csv"
            if Path(csv_file_path).is_file():
                df = pd.read_csv(csv_file_path)

                # Check the disease for the last row
                if not df.empty:
                    last_row = df.iloc[-1]

                    # Initialize the results string
                    results = ""

                    # Apply corresponding disease checking function to each genetic sequence
                    if last_row['Disease'] == "Huntington's Disease":
                        # Apply the disease checking function to each gene sequence and its complement and append to results
                        results += str(check_huntingtin_sequence(last_row["Father's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Father's Complement"]))
                        results += str(check_huntingtin_sequence(last_row["Mother's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Mother's Complement"]))
                        results += str(check_huntingtin_sequence(last_row["Paternal Grandfather's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Paternal Grandfather's Complement"]))
                        results += str(check_huntingtin_sequence(last_row["Paternal Grandmother's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Paternal Grandmother's Complement"]))
                        results += str(check_huntingtin_sequence(last_row["Maternal Grandfather's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Maternal Grandfather's Complement"]))
                        results += str(check_huntingtin_sequence(last_row["Maternal Grandmother's Gene"]))
                        results += str(check_huntingtin_sequence(last_row["Maternal Grandmother's Complement"]))
                    
                    elif last_row['Disease'] == "Sickle Cell Anemia":
                        # Apply the disease checking function to each gene sequence and its complement and append to results
                        results += str(check_sickle_cell_sequence(last_row["Father's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Father's Complement"]))
                        results += str(check_sickle_cell_sequence(last_row["Mother's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Mother's Complement"]))
                        results += str(check_sickle_cell_sequence(last_row["Paternal Grandfather's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Paternal Grandfather's Complement"]))
                        results += str(check_sickle_cell_sequence(last_row["Paternal Grandmother's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Paternal Grandmother's Complement"]))
                        results += str(check_sickle_cell_sequence(last_row["Maternal Grandfather's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Maternal Grandfather's Complement"]))
                        results += str(check_sickle_cell_sequence(last_row["Maternal Grandmother's Gene"]))
                        results += str(check_sickle_cell_sequence(last_row["Maternal Grandmother's Complement"]))

                    # Add more conditions for other diseases if needed
                    elif last_row['Disease'] == "Muscular Dystrophy":
                        # Apply the disease checking function to each gene sequence and its complement and append to results
                        results += str(check_dmd_sequence(last_row["Father's Gene"]))
                        results += str(check_dmd_sequence(last_row["Father's Complement"]))
                        results += str(check_dmd_sequence(last_row["Mother's Gene"]))
                        results += str(check_dmd_sequence(last_row["Mother's Complement"]))
                        results += str(check_dmd_sequence(last_row["Paternal Grandfather's Gene"]))
                        results += str(check_dmd_sequence(last_row["Paternal Grandfather's Complement"]))
                        results += str(check_dmd_sequence(last_row["Paternal Grandmother's Gene"]))
                        results += str(check_dmd_sequence(last_row["Paternal Grandmother's Complement"]))
                        results += str(check_dmd_sequence(last_row["Maternal Grandfather's Gene"]))
                        results += str(check_dmd_sequence(last_row["Maternal Grandfather's Complement"]))
                        results += str(check_dmd_sequence(last_row["Maternal Grandmother's Gene"]))
                        results += str(check_dmd_sequence(last_row["Maternal Grandmother's Complement"]))

                    # Add the results to the DataFrame
                    df.loc[df.index[-1], 'Results'] = results

                    # Display the updated DataFrame
                    st.write(df)

                    # Generate Punnett squares
                    st.write("\nPunnett Squares:")
                    father_genotype = results[:2]
                    mother_genotype = results[2:4]
                    paternal_grandfather_genotype = results[4:6]
                    paternal_grandmother_genotype = results[6:8]
                    maternal_grandfather_genotype = results[8:10]
                    maternal_grandmother_genotype = results[10:]

                    father_mother_square = generate_punnett_square(father_genotype, mother_genotype)
                    paternal_grandfather_paternal_grandmother_square = generate_punnett_square(paternal_grandfather_genotype, paternal_grandmother_genotype)
                    maternal_grandfather_maternal_grandmother_square = generate_punnett_square(maternal_grandfather_genotype, maternal_grandmother_genotype)

                    st.write("Punnett Square for Father and Mother:")
                    for row in range(2):
                        row_elements = ""
                        for col in range(2):
                            row_elements += father_mother_square[row * 2 + col] + "\t"
                        st.write(row_elements)

                    st.write("\nPunnett Square for Paternal Grandfather and Paternal Grandmother:")
                    for row in range(2):
                        row_elements = ""
                        for col in range(2):
                            row_elements += paternal_grandfather_paternal_grandmother_square[row * 2 + col] + "\t"
                        st.write(row_elements)

                    st.write("\nPunnett Square for Maternal Grandfather and Maternal Grandmother:")
                    for row in range(2):
                        row_elements = ""
                        for col in range(2):
                            row_elements += maternal_grandfather_maternal_grandmother_square[row * 2 + col] + "\t"
                        st.write(row_elements)

            else:
                st.write("No data available.")
        
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    if st.session_state['page'] == 'home':
        homepage()

    elif st.session_state['page'] == 'gene':
        gene()

if __name__ == "__main__":
    main()
