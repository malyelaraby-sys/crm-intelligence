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

# ✅ Helper to preserve formatting
def format_text(text):
    if text:
        return text.replace("\n", "  \n")
    return ""

# =========================================
# ✅ VIEW CONTACTS + PROFILE
# =========================================

st.header("📋 Contacts")

contacts_response = supabase.table("contacts").select("*").execute()

if contacts_response.data:

    contact_names = [c["name"] for c in contacts_response.data]
    selected_name = st.selectbox("Select a contact", contact_names)

    selected_contact = next(c for c in contacts_response.data if c["name"] == selected_name)

    st.markdown("---")

    # ✅ Basic Info
    st.subheader("👤 Basic Information")
    st.write(f"**Name:** {selected_contact['name']}")
    st.write(f"**Company:** {selected_contact['company']}")
    st.write(f"**Role:** {selected_contact['role']}")
    st.write(f"**Phone:** {selected_contact['phone']}")
    st.write(f"**Email:** {selected_contact['email']}")

    st.markdown("---")

    # ✅ Intelligence
    st.subheader("🧠 Customer Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Communication Style**")
        st.markdown(format_text(selected_contact["communication_style"]))

        st.write("**Personality Traits**")
        st.markdown(format_text(selected_contact["personality_traits"]))

    with col2:
        st.write("**Preferences**")
        st.markdown(format_text(selected_contact["preferences"]))

        st.write("**Lifestyle Notes**")
        st.markdown(format_text(selected_contact["lifestyle_notes"]))

    st.markdown("---")

    # ✅ Negotiation
    st.subheader("💼 Negotiation Style")
    st.markdown(format_text(selected_contact["negotiation_notes"]))

    st.markdown("---")

    # ✅ Relationship
    st.subheader("📌 Relationship Summary")
    st.markdown(format_text(selected_contact["relationship_summary"]))

    st.markdown("---")

    # ✅ Playbook
    st.subheader("🔥 How to Win This Client")
    st.success(format_text(selected_contact["playbook"]))

    st.markdown("---")

    # =========================================
    # ✅ INTERACTION HISTORY
    # =========================================

    st.subheader("📜 Interaction History")

    interactions = supabase.table("interactions") \
        .select("*") \
        .eq("contact_id", selected_contact["id"]) \
        .order("created_at", desc=True) \
        .execute()

    if interactions.data:
        for interaction in interactions.data:
            st.markdown(f"**{interaction['type']}**")
            st.markdown(f"📝 {format_text(interaction['notes'])}")
            st.markdown(f"🧠 Insight: {format_text(interaction['insights_learned'])}")
            st.write("---")
    else:
        st.info("No interactions yet")

    # =========================================
    # ✅ DERIVED INSIGHTS (NEW ✅)
    # =========================================

    st.markdown("---")
    st.subheader("🧠 Derived Insights (Auto-generated)")

    if interactions.data:

        all_insights = [
            i["insights_learned"]
            for i in interactions.data
            if i["insights_learned"]
        ]

        if all_insights:
            combined_insights = "\n\n".join(all_insights)
            st.markdown(format_text(combined_insights))
        else:
            st.info("No insights captured yet")

    else:
        st.info("No interaction data yet")

    st.markdown("---")

    # =========================================
    # ✅ ADD INTERACTION
    # =========================================

    st.subheader("➕ Log Interaction")

    with st.form("interaction_form"):

        interaction_type = st.selectbox("Type", ["Call", "Meeting", "WhatsApp", "Email"])

        notes = st.text_area("What happened?")

        insights = st.text_area(
            "What did you learn about this client?",
            placeholder="Capture behavior, preferences, reactions..."
        )

        submitted_interaction = st.form_submit_button("Save Interaction")

        if submitted_interaction:
            supabase.table("interactions").insert({
                "contact_id": selected_contact["id"],
                "type": interaction_type,
                "notes": notes,
                "insights_learned": insights
            }).execute()

            st.success("✅ Interaction saved!")
            st.rerun()

else:
    st.info("No contacts yet")


# =========================================
# ✅ ADD CONTACT (BOTTOM CONTROLLED UX)
# =========================================

st.markdown("---")
st.header("➕ Add Contact")

if "show_form" not in st.session_state:
    st.session_state.show_form = False

col1, col2 = st.columns([1, 5])

with col1:
    if st.button("➕ Add"):
        st.session_state.show_form = True

with col2:
    if st.session_state.show_form:
        if st.button("❌ Cancel"):
            st.session_state.show_form = False

if st.session_state.show_form:

    with st.form("add_contact_form"):

        name = st.text_input("Name")
        company = st.text_input("Company")
        role = st.text_input("Role")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        st.subheader("🧠 Customer Intelligence")

        col1, col2 = st.columns(2)

        with col1:
            communication_style = st.text_area("Communication Style")
            personality_traits = st.text_area("Personality Traits")

        with col2:
            preferences = st.text_area("Preferences")
            lifestyle_notes = st.text_area("Lifestyle Notes")

        negotiation_notes = st.text_area("Negotiation Style")
        relationship_summary = st.text_area("Relationship Summary")
        playbook = st.text_area("🔥 How to Win This Client (PLAYBOOK)")

        submitted = st.form_submit_button("✅ Save Contact")

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

            st.session_state.show_form = False
            st.rerun()