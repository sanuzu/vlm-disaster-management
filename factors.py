import streamlit as st
import os

def manage_factors():
    st.set_page_config(page_title="Manage Assessment Factors")
    st.title("Disseverity Assessment Factors Management")
    
    # Initialize factors file
    if not os.path.exists("factors.txt"):
        with open("factors.txt", "w") as f:
            f.write("Visible structural damage\nPresence of injured humans\nFlood water level\nFire/smoke presence")
    
    # Load factors
    with open("factors.txt") as f:
        factors = [line.strip() for line in f if line.strip()]
    
    # Add factor
    with st.form("add_factor"):
        st.subheader("Add New Factor")
        new_factor = st.text_input("Enter new assessment factor:")
        if st.form_submit_button("➕ Add Factor"):
            if new_factor and new_factor not in factors:
                with open("factors.txt", "a") as f:
                    f.write(f"\n{new_factor}")
                st.success("Factor added!")
                st.rerun()
    
    # Delete factors
    with st.form("delete_factor"):
        st.subheader("Remove Existing Factors")
        to_delete = st.multiselect(
            "Select factors to remove:",
            options=factors
        )
        if st.form_submit_button("🗑️ Remove Selected"):
            if to_delete:
                updated = [f for f in factors if f not in to_delete]
                with open("factors.txt", "w") as f:
                    f.write("\n".join(updated))
                st.success(f"Removed {len(to_delete)} factors")
                st.rerun()
    
    # Display current factors
    st.subheader("Current Assessment Factors")
    if factors:
        for i, factor in enumerate(factors, 1):
            st.write(f"{i}. {factor}")
    else:
        st.warning("No factors defined")

if __name__ == "__main__":
    manage_factors()
