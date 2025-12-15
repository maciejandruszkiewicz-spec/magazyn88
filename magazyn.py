import streamlit as st

def main():
    # --- Inicjalizacja listy towarów w stanie sesji Streamlit ---
    # Streamlit przechowuje stan aplikacji w 'st.session_state'.
    # Jeśli klucz 'inventory' nie istnieje, tworzymy go jako pustą listę.
    if 'inventory' not in st.session_state:
        st.session_state.inventory = []

    st.title("📦 Prosty Magazyn (Streamlit)")
    st.markdown("---")

    # --- Sekcja Dodawania Towaru ---
    st.header("➕ Dodaj Nowy Towar")

    # Używamy formularza (st.form) do grupowania elementów wejściowych,
    # co pozwala na wysłanie danych jednym przyciskiem.
    with st.form("add_item_form", clear_on_submit=True):
        item_name = st.text_input("Nazwa Towaru", key="item_name_input")
        item_quantity = st.number_input("Ilość", min_value=1, value=1, step=1, key="item_quantity_input")

        submitted = st.form_submit_button("Dodaj do Magazynu")

        if submitted and item_name:
            # Tworzymy nowy element jako słownik
            new_item = {
                "name": item_name.strip(),
                "quantity": item_quantity
            }
            # Dodajemy element do listy w stanie sesji
            st.session_state.inventory.append(new_item)
            st.success(f"Dodano: {item_quantity}x {item_name.strip()} do magazynu!")
        elif submitted and not item_name:
            st.error("Wprowadź nazwę towaru, aby go dodać.")

    st.markdown("---")

    # --- Sekcja Wyświetlania Magazynu ---
    st.header("📋 Aktualny Stan Magazynu")

    if not st.session_state.inventory:
        st.info("Magazyn jest pusty. Dodaj nowy towar powyżej!")
    else:
        # Konwertujemy listę słowników na format, który Streamlit może łatwo wyświetlić (np. DataFrame)
        # Aby zachować prostotę, wyświetlimy to jako tabelę.
        st.dataframe(st.session_state.inventory, use_container_width=True)

        # --- Sekcja Usuwania Towaru ---
        st.subheader("🗑️ Usuń Towar")

        # Tworzymy listę nazw towarów do wyboru w liście rozwijanej
        item_names = [item['name'] for item in st.session_state.inventory]

        # Wybieramy towar do usunięcia
        item_to_remove_name = st.selectbox(
            "Wybierz towar do usunięcia",
            options=item_names,
            index=0 if item_names else None
        )

        if st.button("Usuń Wybrany Towar"):
            if item_to_remove_name:
                # W Streamlit zazwyczaj łatwiej jest stworzyć nową listę bez elementu,
                # niż modyfikować listę w miejscu.
                st.session_state.inventory = [
                    item for item in st.session_state.inventory
                    if item['name'] != item_to_remove_name
                ]
                st.warning(f"Usunięto wszystkie pozycje dla: {item_to_remove_name}")
                # Po usunięciu warto ponownie uruchomić aplikację, aby odświeżyć widok,
                # chociaż Streamlit powinien to zrobić automatycznie po zmianie session_state.
                st.experimental_rerun()
            else:
                st.error("Nie wybrano towaru do usunięcia.")


if __name__ == "__main__":
    main()
