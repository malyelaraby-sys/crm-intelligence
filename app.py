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

# ✅ Helper for formatting
def format_text(text):
    if text:
        return text.replace("\n", "  \n")
    return ""

# =========================================
# ✅ CONTACTS + PROFILE
# =========================================

st.header("📋 Contacts")

contacts_response = supabase.table("contacts").select("*").execute()

if contacts_response.data:

    contact_names = [c["name"] for c in contacts_response.data]

    if "selected_contact_name" not in st.session_state:
        st.session_state.selected_contact_name = contact_names[0]

    selected_name = st.selectbox(
        "Select a contact",
        contact_names,
        key="selected_contact_name"
    )

    selected_contact = next(
        c for c in contacts_response.data
        if c["name"] == selected_name
    )

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
    # ✅ STRUCTURED PLAYBOOK
    # =========================================

    st.subheader("🎯 Structured Playbook")

    sp_col1, sp_col2, sp_col3 = st.columns(3)

    with sp_col1:
        st.markdown("### Communication")
        st.write(f"**Formality:** {selected_contact.get('formality') or 'Not set'}")
        st.write(f"**Preferred Channel:** {selected_contact.get('preferred_channel') or 'Not set'}")
        st.write(f"**Meeting Style:** {selected_contact.get('meeting_style') or 'Not set'}")

    with sp_col2:
        st.markdown("### Decision Making")
        st.write(f"**Decision Speed:** {selected_contact.get('decision_speed') or 'Not set'}")
        st.write(f"**Price Sensitivity:** {selected_contact.get('price_sensitivity') or 'Not set'}")
        st.write(f"**Approval Process:** {selected_contact.get('approval_process') or 'Not set'}")

    with sp_col3:
        st.markdown("### Relationship")
        st.write(f"**Trust Level:** {selected_contact.get('trust_level') or 'Not set'}")
        st.write(f"**Relationship Stage:** {selected_contact.get('relationship_stage') or 'Not set'}")

    st.markdown("---")

    # =========================================
    # ✅ EDIT STRUCTURED PLAYBOOK
    # =========================================

    st.subheader("✏️ Edit Structured Playbook")

    with st.form("structured_playbook_form"):

        st.markdown("### Communication")

        formality_options = ["", "Formal", "Balanced", "Informal"]
        channel_options = ["", "Email", "Phone", "WhatsApp", "Face-to-face"]
        meeting_options = ["", "Short", "Detailed", "Structured", "Informal"]

        sp_formality = st.selectbox(
            "Formality",
            formality_options,
            index=formality_options.index(selected_contact["formality"])
            if selected_contact.get("formality") in formality_options
            else 0
        )

        sp_channel = st.selectbox(
            "Preferred Channel",
            channel_options,
            index=channel_options.index(selected_contact["preferred_channel"])
            if selected_contact.get("preferred_channel") in channel_options
            else 0
        )

        sp_meeting = st.selectbox(
            "Meeting Style",
            meeting_options,
            index=meeting_options.index(selected_contact["meeting_style"])
            if selected_contact.get("meeting_style") in meeting_options
            else 0
        )

        st.markdown("### Decision Making")

        decision_options = ["", "Fast", "Medium", "Slow"]
        price_options = ["", "Low", "Medium", "High"]
        approval_options = ["", "Individual", "Team", "Board", "Multi-level"]

        sp_decision = st.selectbox(
            "Decision Speed",
            decision_options,
            index=decision_options.index(selected_contact["decision_speed"])
            if selected_contact.get("decision_speed") in decision_options
            else 0
        )

        sp_price = st.selectbox(
            "Price Sensitivity",
            price_options,
            index=price_options.index(selected_contact["price_sensitivity"])
            if selected_contact.get("price_sensitivity") in price_options
            else 0
        )

        sp_approval = st.selectbox(
            "Approval Process",
            approval_options,
            index=approval_options.index(selected_contact["approval_process"])
            if selected_contact.get("approval_process") in approval_options
            else 0
        )

        st.markdown("### Relationship")

        trust_options = ["", "Low", "Medium", "High"]
        stage_options = ["", "New", "Developing", "Established", "Strategic"]

        sp_trust = st.selectbox(
            "Trust Level",
            trust_options,
            index=trust_options.index(selected_contact["trust_level"])
            if selected_contact.get("trust_level") in trust_options
            else 0
        )

        sp_stage = st.selectbox(
            "Relationship Stage",
            stage_options,
            index=stage_options.index(selected_contact["relationship_stage"])
            if selected_contact.get("relationship_stage") in stage_options
            else 0
        )

        save_playbook = st.form_submit_button("💾 Save Structured Playbook")

        if save_playbook:

            supabase.table("contacts").update({
                "formality": sp_formality or None,
                "preferred_channel": sp_channel or None,
                "meeting_style": sp_meeting or None,
                "decision_speed": sp_decision or None,
                "price_sensitivity": sp_price or None,
                "approval_process": sp_approval or None,
                "trust_level": sp_trust or None,
                "relationship_stage": sp_stage or None
            }).eq("id", selected_contact["id"]).execute()

            st.success("✅ Structured Playbook saved successfully")
            st.rerun()

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
    # ✅ DERIVED INSIGHTS
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

    # =========================================
    # ✅ IMPROVED KEY PATTERNS (FIXED ✅)
    # =========================================

    st.markdown("---")
    st.subheader("📊 Key Patterns")

    combined_text = ""

    # ✅ Add interaction insights
    if interactions.data:
        combined_text += " ".join([
            i["insights_learned"].lower()
            for i in interactions.data
            if i["insights_learned"]
        ])

    # ✅ Add contact profile fields
    combined_text += " " + (selected_contact.get("communication_style") or "").lower()
    combined_text += " " + (selected_contact.get("personality_traits") or "").lower()
    combined_text += " " + (selected_contact.get("preferences") or "").lower()

    patterns = []

    if "price" in combined_text or "expensive" in combined_text:
        patterns.append("💰 Price sensitive")

    if "slow" in combined_text or "takes time" in combined_text:
        patterns.append("⏳ Slow decision maker")

    if "fast" in combined_text:
        patterns.append("⚡ Fast decision maker")

    if "friendly" in combined_text:
        patterns.append("😊 Responds well to friendly tone")

    if "formal" in combined_text:
        patterns.append("🏢 Prefers formal communication")

    if patterns:
        for p in patterns:
            st.write(f"- {p}")
    else:
        st.info("No clear patterns detected yet")

    st.markdown("---")

    # =========================================
    # ✅ SUGGESTED STRUCTURED PLAYBOOK UPDATES
    # =========================================

    st.markdown("---")
    st.subheader("💡 Suggested Structured Playbook Updates")

    suggestions = {}
    suggestion_reasons = {}

    if "💰 Price sensitive" in patterns:
        if not selected_contact.get("price_sensitivity"):
            suggestions["price_sensitivity"] = "High"
            suggestion_reasons["price_sensitivity"] = "💰 Price sensitive"
    if "⏳ Slow decision maker" in patterns:
        if not selected_contact.get("decision_speed"):
            suggestions["decision_speed"] = "Slow"
            suggestion_reasons["decision_speed"] = "⏳ Slow decision maker"
    if "⚡ Fast decision maker" in patterns:
        if not selected_contact.get("decision_speed"):
            suggestions["decision_speed"] = "Fast"
            suggestion_reasons["decision_speed"] = "⚡ Fast decision maker"
    if "🏢 Prefers formal communication" in patterns:
        if not selected_contact.get("formality"):
            suggestions["formality"] = "Formal"
            suggestion_reasons["formality"] = "🏢 Prefers formal communication"
    if "😊 Responds well to friendly tone" in patterns:
        if not selected_contact.get("formality"):
            suggestions["formality"] = "Balanced"
            suggestion_reasons["formality"] = "😊 Responds well to friendly tone"
    if suggestions:

        for field, value in suggestions.items():

            st.markdown(
                f"✅ **{field.replace('_', ' ').title()}** → **{value}**"
            )

            st.caption(
                f"Reason: {suggestion_reasons.get(field, 'Pattern detected')}"
            )

        if st.button("⚡ Apply Suggestions"):

            supabase.table("contacts").update(
                suggestions
            ).eq(
                "id",
                selected_contact["id"]
            ).execute()

            st.success("✅ Suggestions applied")
            st.rerun()

    else:
        st.info("No suggestions available")
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
# ✅ ADD CONTACT (BOTTOM UX)
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