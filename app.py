import streamlit as st
from supabase import create_client

# ✅ Page setup
st.set_page_config(page_title="CRM Intelligence", layout="wide")

st.title("🧠 CRM Intelligence System")
st.write("Manage your customers and learn how to win them.")

# ✅ Supabase connection
SUPABASE_URL = "https://qqfbxcvyiqaffzkdmbyl.supabase.co"
SUPABASE_KEY = "sb_publishable_h8hgAkyRWyC4Sh9QnrDbwQ_MNjeuShu"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================================
# ✅ ADD CONTACT FORM
# =========================================

st.header("➕ Add New Contact")

with st.form("add_contact_form"):

    # Basic Info
    name = st.text_input("Name")
    company = st.text_input("Company")
    role = st.text_input("Role")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    st.subheader("🧠 Customer Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        communication_style = st.text_area(
            "Communication Style",
            placeholder="Formal, direct, prefers WhatsApp..."
        )

        personality_traits = st.text_area(
            "Personality Traits",
            placeholder="Friendly, analytical..."
        )

    with col2:
        preferences = st.text_area(
            "Preferences",
            placeholder="Short meetings, morning calls..."
        )

        lifestyle_notes = st.text_area(
            "Lifestyle Notes",
            placeholder="Smoker, football fan..."
        )

    negotiation_notes = st.text_area(
        "Negotiation Style",
        placeholder="Price sensitive, needs time..."
    )

    relationship_summary = st.text_area("Relationship Summary")

    playbook = st.text_area(
        "🔥 How to Win This Client (PLAYBOOK)",
        placeholder="DO: ... / DON'T: ..."
    )

    submitted = st.form_submit_button("Save Contact")

    if submitted:
        supabase.table("contacts").insert({
            "name": name,
            "company": company,
            "role": role,
            "email": email,
            "phone": phone,
            "communication_style": communication_style,
            "personality_traits": personality_traits,
            "preferences": preferences,
            "lifestyle_notes": lifestyle_notes,
            "negotiation_notes": negotiation_notes,
            "relationship_summary": relationship_summary,
            "playbook": playbook
        }).execute()

        st.success("✅ Contact saved successfully!")


# =========================================
# ✅ VIEW CONTACT PROFILE (CORE FEATURE)
# =========================================

st.header("📋 Contacts")

response = supabase.table("contacts").select("*").execute()

if response.data:

    # ✅ Select contact
    contact_names = [c["name"] for c in response.data]
    selected_name = st.selectbox("Select a contact", contact_names)

    # ✅ Get selected contact
    selected_contact = next(c for c in response.data if c["name"] == selected_name)

    st.markdown("---")

    # ✅ BASIC INFO
    st.subheader("👤 Basic Information")
    st.write(f"**Name:** {selected_contact['name']}")
    st.write(f"**Company:** {selected_contact['company']}")
    st.write(f"**Role:** {selected_contact['role']}")
    st.write(f"**Phone:** {selected_contact['phone']}")
    st.write(f"**Email:** {selected_contact['email']}")

    st.markdown("---")

    # ✅ CUSTOMER INTELLIGENCE
    st.subheader("🧠 Customer Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Communication Style**")
        st.write(selected_contact["communication_style"])

        st.write("**Personality Traits**")
        st.write(selected_contact["personality_traits"])

    with col2:
        st.write("**Preferences**")
        st.write(selected_contact["preferences"])

        st.write("**Lifestyle Notes**")
        st.write(selected_contact["lifestyle_notes"])

    st.markdown("---")

    # ✅ NEGOTIATION
    st.subheader("💼 Negotiation Style")
    st.write(selected_contact["negotiation_notes"])

    st.markdown("---")

    # ✅ RELATIONSHIP
    st.subheader("📌 Relationship Summary")
    st.write(selected_contact["relationship_summary"])

    st.markdown("---")

    # ✅ PLAYBOOK (HIGHLIGHTED)
    st.subheader("🔥 How to Win This Client")
    st.success(selected_contact["playbook"])

else:
    st.info("No contacts yet")