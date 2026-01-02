# history_manager.py
import streamlit as st
import pandas as pd
import io

def init_session_state():
    """Inicjalizuje historię w sesji, jeśli jeszcze nie istnieje."""
    if 'history_df' not in st.session_state:
        # Tworzymy pusty DataFrame z odpowiednimi kolumnami na start
        st.session_state['history_df'] = pd.DataFrame()

def add_entry(first_name, last_name, date, income, budget_df):
    """
    Dodaje nowy wiersz do historii budżetów.
    Łączy dane osobowe, dochód i wyliczone kwoty ze słoików.
    """
    # 1. Przygotuj słownik z podstawowymi danymi
    new_record = {
        "Data Budżetu": date,
        "Imię": first_name,
        "Nazwisko": last_name,
        "Dochód (PLN)": income
    }

    # 2. Wyciągnij dane ze słoików (z logic.py df_budget)
    # budget_df ma kolumny: Słoik, Procent, Kwota, Opis
    for index, row in budget_df.iterrows():
        col_name = row['Słoik'].replace("<br>", " ") # Usuwamy HTML z nazw kolumn
        new_record[col_name] = round(row['Kwota'], 2)

    # 3. Dodaj do DataFrame w sesji
    new_row_df = pd.DataFrame([new_record])

    if st.session_state['history_df'].empty:
        st.session_state['history_df'] = new_row_df
    else:
        st.session_state['history_df'] = pd.concat(
            [st.session_state['history_df'], new_row_df],
            ignore_index=True
        )

def get_history():
    """Zwraca aktualną tabelę historii."""
    return st.session_state.get('history_df', pd.DataFrame())

def clear_current_form():
    """
    Funkcja callback do resetowania formularza (wymuszenie nowej rejestracji),
    ale ZACHOWANIE historii w tabeli.
    """
    # Czyścimy klucze widgetów rejestracji, by wymusić puste pola
    # Uwaga: w Streamlit resetowanie widgetów robi się najlepiej przez zmianę klucza
    # lub ręczne czyszczenie, jeśli używamy st.session_state[key].
    # Tutaj zastosujemy prosty trick: rerunning z wyczyszczeniem inputów nie jest trywialny
    # bez session_state, więc w main.py użyjemy kluczy dynamicznych lub formularza.
    pass # Logika resetu będzie obsłużona w main.py poprzez st.rerun() i flagi.

def convert_df_to_excel(df):
    """Konwertuje DataFrame do pliku Excel w pamięci."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Podsumowanie')
    return output.getvalue()