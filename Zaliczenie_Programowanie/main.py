# main.py
import streamlit as st
import pandas as pd
import datetime

# Import modułów
import components
import logic
import history_manager

# ---------------------------------------------------------
# 1. KONFIGURACJA I INICJALIZACJA
# ---------------------------------------------------------
st.set_page_config(page_title="Budżet 6 Słoików", page_icon="💰", layout="wide")

# Inicjalizacja stanu historii
history_manager.init_session_state()

# Obsługa resetowania (Nowy Budżet)
if 'reset_trigger' not in st.session_state:
    st.session_state['reset_trigger'] = 0

def reset_app():
    """Zwiększa licznik, co wymusi przerysowanie widgetów z nowymi kluczami (czyste pola)"""
    st.session_state['reset_trigger'] += 1

# ---------------------------------------------------------
# 2. REJESTRACJA (Wymagana)
# ---------------------------------------------------------
components.show_header()

st.info("🔒 **Rejestracja Budżetu** - Wypełnij dane, aby odblokować kalkulator.")

# Kontener na formularz rejestracji
with st.container(border=True):
    col_reg1, col_reg2, col_reg3 = st.columns(3)

    # Używamy klucza z reset_trigger, aby wyczyścić pola po kliknięciu "Zarejestruj nowy budżet"
    key_suffix = str(st.session_state['reset_trigger'])

    with col_reg1:
        first_name = st.text_input("Imię *", key=f"fname_{key_suffix}")
    with col_reg2:
        last_name = st.text_input("Nazwisko *", key=f"lname_{key_suffix}")
    with col_reg3:
        budget_date = st.date_input("Data rejestracji budżetu *", value=datetime.date.today(), key=f"date_{key_suffix}")

# Walidacja: Czy dane są wpisane?
is_registered = first_name and last_name and budget_date

if not is_registered:
    st.warning("⚠️ Proszę podać Imię i Nazwisko, aby przystąpić do tworzenia budżetu.")
    st.stop()  # Zatrzymuje ładowanie reszty strony do momentu wpisania danych

# ---------------------------------------------------------
# 3. APLIKACJA GŁÓWNA (Widoczna po rejestracji)
# ---------------------------------------------------------
st.divider()
st.success(f"Witaj, **{first_name} {last_name}**! Tworzysz budżet na dzień: **{budget_date}**")

# Pobranie dochodu
income = components.show_income_input()

col_left, col_right = st.columns([1, 1])

with col_left:
    # Render tabeli edycji (z logic.py)
    df_budget = logic.render_budget_table(income)

with col_right:
    # Render wykresu (z logic.py)
    if df_budget is not None:
        logic.render_chart_with_sql(df_budget, income)

# ---------------------------------------------------------
# 4. ZAPISYWANIE I PODSUMOWANIE
# ---------------------------------------------------------
st.markdown("---")
st.subheader("💾 Zapis i Podsumowanie")

# Przycisk zapisu bieżącej konfiguracji
# Sprawdzamy, czy df_budget jest poprawny (suma 100%)
can_save = df_budget is not None and not df_budget.empty

if st.button("📥 Zapisz moją rejestrację (Dodaj do tabeli)", disabled=not can_save, type="primary"):
    history_manager.add_entry(first_name, last_name, budget_date, income, df_budget)
    st.success("✅ Dodano wpis do tabeli podsumowania!")

# Wyświetlanie tabeli podsumowania (jeśli istnieje)
history_df = history_manager.get_history()

if not history_df.empty:
    st.markdown("### 📋 Tabela Podsumowania")

    # Formatowanie tabeli dla lepszego wyglądu
    st.dataframe(
        history_df.style.format(precision=2),
        use_container_width=True,
        hide_index=True
    )

    # Sekcja przycisków pod tabelą
    col_btn1, col_btn2 = st.columns([1, 4])

    with col_btn1:
        # Przycisk: Zarejestruj nowy budżet (Resetuje formularz góry, zostawia tabelę)
        if st.button("🔄 Zarejestruj nowy budżet"):
            reset_app()
            st.rerun()

    with col_btn2:
        # Przycisk: Eksport do Excela
        excel_data = history_manager.convert_df_to_excel(history_df)
        st.download_button(
            label="📊 Pobierz tabelę jako Excel (.xlsx)",
            data=excel_data,
            file_name=f'budzet_podsumowanie_{datetime.date.today()}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
else:
    st.info("Twoja tabela podsumowania jest pusta. Kliknij 'Zapisz moją rejestrację' powyżej.")

# ---------------------------------------------------------
# 5. STOPKA
# ---------------------------------------------------------
components.show_footer()