import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import gemini_pro_response

working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the diabetes prediction model
diabetes_model = pickle.load(open(os.path.join(working_dir, 'saved_models/diabetes_model.sav'), 'rb'))

# Streamlit page configuration
st.set_page_config(
    page_title="DiaPredict",
    page_icon="🏥",
    layout="centered",
)

# Sidebar menu
with st.sidebar:
    selected = option_menu('DiaPredict',
                           ['Prediksi Diabetes', 'Tanyakan Apapun'],
                           menu_icon='hospital-fill', 
                           icons=['activity', 'patch-question-fill'],
                           default_index=0
                           )

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "asisten" if user_role == "model" else user_role

# Halaman Prediksi Diabetes
if selected == 'Prediksi Diabetes':
    st.title('Prediksi Diabetes')

    # Mendapatkan data input dari pengguna
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Jumlah Kehamilan')

    with col2:
        Glucose = st.text_input('Tingkat Glukosa')

    with col3:
        BloodPressure = st.text_input('Nilai Tekanan Darah')

    with col1:
        SkinThickness = st.text_input('Nilai Ketebalan Kulit')

    with col2:
        Insulin = st.text_input('Tingkat Insulin')

    with col3:
        BMI = st.text_input('Nilai BMI (Indeks Massa Tubuh)')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Nilai Fungsi Silsilah Diabetes')

    with col2:
        Age = st.text_input('Usia Orang tersebut')

    # Kode untuk Prediksi
    diab_diagnosis = ''

    # Membuat tombol untuk Prediksi
    if st.button('Hasil Tes Diabetes'):
        try:
            user_input = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), float(Insulin),
                          float(BMI), float(DiabetesPedigreeFunction), float(Age)]
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                diab_diagnosis = 'Orang tersebut menderita diabetes'
            else:
                diab_diagnosis = 'Orang tersebut tidak menderita diabetes'
        except ValueError:
            diab_diagnosis = 'Harap masukkan nilai numerik yang valid untuk semua bidang.'

    st.success(diab_diagnosis)

# Model embedding teks
if selected == "Tanyakan Apapun":
    st.title("❓ Tanya AI")

    # Kotak teks untuk memasukkan prompt
    user_prompt = st.text_area(label='', placeholder="Tanyakan apapun padaku...")

    if st.button("Tanya"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)