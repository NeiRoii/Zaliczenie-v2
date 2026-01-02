# components.py
import streamlit as st

def show_header():
    """Wyświetla główny nagłówek strony."""
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 3rem; margin-bottom: 2rem;'>
            Stwórz swój budżet do zera na podstawie zasady 6 słoików
        </h1>
        """,
        unsafe_allow_html=True
    )

def show_income_input():
    """Wyświetla pole do wprowadzania dochodu i zwraca podaną wartość."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 💸 Wpisz swój miesięczny dochód (netto)")
        income = st.number_input(
            label="Kwota w PLN",
            min_value=0.0,
            value=4666.0,
            step=100.0,
            format="%.2f",
            help="Wpisz kwotę, którą dysponujesz w tym miesiącu."
        )
    st.markdown("---")
    return income

def show_footer():
    """Wyświetla stopkę z informacjami o autorach."""
    st.markdown("---")
    st.caption("Aplikacja stworzona w Pythonie. Dane wykresu przetworzone przez SQL (SQLite)."
               " Stworzone na potrzeby zaliczenia przez Piotra Pietrasińskiego i Oliwię Kowalik")