import streamlit as st
from supabase import create_client
from datetime import datetime

# ✅ Page setup
st.set_page_config(page_title="CRM Intelligence", layout="wide")

st.title("🧠 CRM Intelligence System")
st.write("Manage your customers and learn how to win them.")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏢 Companies",
        "👤 Contacts",
        "✅ Tasks",
        "📞 Interactions",
        "📊 Analytics",
    ],
)
# ✅ Supabase connection
SUPABASE_URL = "https://qqfbxcvyiqaffzkdmbyl.supabase.co"
SUPABASE_KEY = "sb_publishable_h8hgAkyRWyC4Sh9QnrDbwQ_MNjeuShu"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
sales_users = supabase.table("sales_users").select("*").order("name").execute()
companies = supabase.table("companies").select("*").order("name").execute()


# ✅ Helper for formatting
def format_text(text):
    if text:
        return text.replace("\n", "  \n")
    return ""


if page == "🏢 Companies":
    # =========================================
    # ✅ COMPANIES
    # =========================================

    st.header("🏢 Companies")
    company_list = supabase.table("companies").select("*").order("name").execute()

    if company_list.data:

        st.subheader("Company Directory")

        for company in company_list.data:

            owner_name = next(
                (
                    u["name"]
                    for u in sales_users.data
                    if u["id"] == company.get("owner_id")
                ),
                "Unassigned",
            )

            st.markdown(f"""
    **{company['name']}**

    Industry: {company.get('industry') or 'Not set'}

    City: {company.get('city') or 'Not set'}

    Owner: {owner_name}
    """)

            st.markdown("---")
    with st.form("add_company_form"):

        company_name = st.text_input("Company Name")

        industry = st.text_input("Industry")

        city = st.text_input("City")

        owner_names = [u["name"] for u in sales_users.data]

        selected_owner = st.selectbox("Account Owner", owner_names)

        save_company = st.form_submit_button("✅ Save Company")

        if save_company and company_name:

            owner = next(u for u in sales_users.data if u["name"] == selected_owner)

            supabase.table("companies").insert(
                {
                    "name": company_name,
                    "industry": industry,
                    "city": city,
                    "owner_id": owner["id"],
                }
            ).execute()

            st.success("✅ Company saved")
            st.rerun()
    company_names = [c["name"] for c in companies.data]

    selected_company_name = st.selectbox("Select Company", company_names)
    selected_company = next(
        c for c in companies.data if c["name"] == selected_company_name
    )
    st.subheader("🏢 Company Profile")

    owner_name = next(
        (
            u["name"]
            for u in sales_users.data
            if u["id"] == selected_company.get("owner_id")
        ),
        "Unassigned",
    )

    st.write(f"**Company:** {selected_company['name']}")
    st.write(f"**Industry:** {selected_company.get('industry') or 'Not set'}")
    st.write(f"**City:** {selected_company.get('city') or 'Not set'}")
    st.write(f"**Owner:** {owner_name}")
    company_contacts = (
        supabase.table("contacts")
        .select("*")
        .eq("company_id", selected_company["id"])
        .execute()
    )
    st.subheader("📊 Company Metrics")

    company_contact_ids = (
        [c["id"] for c in company_contacts.data] if company_contacts.data else []
    )

    contact_count = len(company_contact_ids)

    open_tasks = 0
    completed_tasks = 0
    interaction_count = 0
    total_distance = 0
    total_expenses = 0

    if company_contact_ids:

        tasks = (
            supabase.table("tasks")
            .select("*")
            .in_("contact_id", company_contact_ids)
            .execute()
        )

        interactions = (
            supabase.table("interactions")
            .select("*")
            .in_("contact_id", company_contact_ids)
            .execute()
        )

        if tasks.data:

            open_tasks = len([t for t in tasks.data if t["status"] == "Open"])

            completed_tasks = len([t for t in tasks.data if t["status"] == "Completed"])

        if interactions.data:

            interaction_count = len(interactions.data)

            total_distance = sum(i.get("distance_km") or 0 for i in interactions.data)

            total_expenses = sum(
                (i.get("transportation_cost") or 0)
                + (i.get("parking_cost") or 0)
                + (i.get("other_expenses") or 0)
                for i in interactions.data
            )

    st.write(f"**Contacts:** {contact_count}")
    st.write(f"**Open Tasks:** {open_tasks}")
    st.write(f"**Completed Tasks:** {completed_tasks}")
    st.write(f"**Interactions:** {interaction_count}")
    st.write(f"**Total Distance:** {total_distance:.1f} KM")
    st.write(f"**Total Expenses:** {total_expenses:.2f}")

    st.subheader("👥 Company Contacts")

    if company_contacts.data:

        for contact in company_contacts.data:

            st.write(f"• {contact['name']} " f"({contact.get('role') or 'No role'})")

    else:
        st.info("No contacts assigned")
if page == "👤 Contacts":
    # =========================================
    # ✅ CONTACTS + PROFILE
    # =========================================

    st.header("📋 Contacts")
    company_names = [c["name"] for c in companies.data]

    selected_company_name = st.selectbox(
        "🏢 Company", company_names, key="contacts_company"
    )

    selected_company = next(
        c for c in companies.data if c["name"] == selected_company_name
    )

    owner_filter_options = ["All"] + [user["name"] for user in sales_users.data]

    selected_owner_filter = st.selectbox("👤 Salesperson Filter", owner_filter_options)

    contacts_response = supabase.table("contacts").select("*").execute()

    if contacts_response.data:

        filtered_contacts = [
            c
            for c in contacts_response.data
            if c.get("company_id") == selected_company["id"]
        ]

        if selected_owner_filter != "All":

            selected_user = next(
                u for u in sales_users.data if u["name"] == selected_owner_filter
            )

            filtered_contacts = [
                c for c in filtered_contacts if c.get("owner_id") == selected_user["id"]
            ]

        contact_names = [c["name"] for c in filtered_contacts]
        if not contact_names:
            st.warning(f"No contacts assigned to {selected_owner_filter}")
            st.stop()

        if (
            "selected_contact_name" not in st.session_state
            or st.session_state.selected_contact_name not in contact_names
        ):
            st.session_state.selected_contact_name = contact_names[0]

        selected_name = st.selectbox(
            "Select a contact", contact_names, key="selected_contact_name"
        )

        selected_contact = next(
            c for c in filtered_contacts if c["name"] == selected_name
        )

        st.markdown("---")

        # ✅ Basic Info
        st.subheader("👤 Basic Information")
        st.write(f"**Name:** {selected_contact['name']}")
        company_name = selected_contact.get("company", "Not Assigned")

    if selected_contact.get("company_id"):

        company_record = next(
            (c for c in companies.data if c["id"] == selected_contact["company_id"]),
            None,
        )

        if company_record:
            company_name = company_record["name"]

        st.write(f"**Company:** {company_name}")
        st.write(f"**Role:** {selected_contact['role']}")
        st.write(f"**Phone:** {selected_contact['phone']}")
        st.write(f"**Email:** {selected_contact['email']}")
        owner_name = "Not Assigned"

        if selected_contact.get("owner_id"):

            owner_record = next(
                (
                    u
                    for u in sales_users.data
                    if u["id"] == selected_contact["owner_id"]
                ),
                None,
            )

            if owner_record:
                owner_name = owner_record["name"]

        st.write(f"**Account Owner:** {owner_name}")

        st.markdown("---")

        # =========================================
        # ✅ CLIENT CLASSIFICATION
        # =========================================

        st.subheader("🏷 Client Classification")

        class_col1, class_col2 = st.columns(2)

        with class_col1:
            st.write(
                f"**Status:** {selected_contact.get('client_status') or 'Prospect'}"
            )

        with class_col2:
            st.write(f"**Tier:** {selected_contact.get('tier') or 'Not set'}")
            st.markdown("---")

        st.subheader("✏️ Edit Classification")

        with st.form("classification_form"):

            status_options = ["Prospect", "Active", "Strategic", "Dormant", "Lost"]

            tier_options = ["", "A", "B", "C"]

            current_status = selected_contact.get("client_status") or "Prospect"

            current_tier = selected_contact.get("tier") or ""

            client_status = st.selectbox(
                "Client Status",
                status_options,
                index=status_options.index(current_status),
            )

            tier = st.selectbox(
                "Client Tier", tier_options, index=tier_options.index(current_tier)
            )

            save_classification = st.form_submit_button("💾 Save Classification")

            if save_classification:

                supabase.table("contacts").update(
                    {"client_status": client_status, "tier": tier or None}
                ).eq("id", selected_contact["id"]).execute()

                st.success("✅ Classification saved")
                st.rerun()
        st.markdown("---")

        st.subheader("👤 Account Owner")

        current_owner_id = selected_contact.get("owner_id")

        owner_options = {user["name"]: user["id"] for user in sales_users.data}

        owner_names = list(owner_options.keys())

        current_owner_name = None

        for user in sales_users.data:
            if user["id"] == current_owner_id:
                current_owner_name = user["name"]
                break

        selected_owner_name = st.selectbox(
            "Owner",
            owner_names,
            index=(
                owner_names.index(current_owner_name)
                if current_owner_name in owner_names
                else 0
            ),
        )

        if st.button("💾 Save Owner"):

            supabase.table("contacts").update(
                {"owner_id": owner_options[selected_owner_name]}
            ).eq("id", selected_contact["id"]).execute()

            st.success("✅ Owner updated")

            st.rerun()
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
            st.write(
                f"**Preferred Channel:** {selected_contact.get('preferred_channel') or 'Not set'}"
            )
            st.write(
                f"**Meeting Style:** {selected_contact.get('meeting_style') or 'Not set'}"
            )

        with sp_col2:
            st.markdown("### Decision Making")
            st.write(
                f"**Decision Speed:** {selected_contact.get('decision_speed') or 'Not set'}"
            )
            st.write(
                f"**Price Sensitivity:** {selected_contact.get('price_sensitivity') or 'Not set'}"
            )
            st.write(
                f"**Approval Process:** {selected_contact.get('approval_process') or 'Not set'}"
            )

        with sp_col3:
            st.markdown("### Relationship")
            st.write(
                f"**Trust Level:** {selected_contact.get('trust_level') or 'Not set'}"
            )
            st.write(
                f"**Relationship Stage:** {selected_contact.get('relationship_stage') or 'Not set'}"
            )

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
                index=(
                    formality_options.index(selected_contact["formality"])
                    if selected_contact.get("formality") in formality_options
                    else 0
                ),
            )

            sp_channel = st.selectbox(
                "Preferred Channel",
                channel_options,
                index=(
                    channel_options.index(selected_contact["preferred_channel"])
                    if selected_contact.get("preferred_channel") in channel_options
                    else 0
                ),
            )

            sp_meeting = st.selectbox(
                "Meeting Style",
                meeting_options,
                index=(
                    meeting_options.index(selected_contact["meeting_style"])
                    if selected_contact.get("meeting_style") in meeting_options
                    else 0
                ),
            )

            st.markdown("### Decision Making")

            decision_options = ["", "Fast", "Medium", "Slow"]
            price_options = ["", "Low", "Medium", "High"]
            approval_options = ["", "Individual", "Team", "Board", "Multi-level"]

            sp_decision = st.selectbox(
                "Decision Speed",
                decision_options,
                index=(
                    decision_options.index(selected_contact["decision_speed"])
                    if selected_contact.get("decision_speed") in decision_options
                    else 0
                ),
            )

            sp_price = st.selectbox(
                "Price Sensitivity",
                price_options,
                index=(
                    price_options.index(selected_contact["price_sensitivity"])
                    if selected_contact.get("price_sensitivity") in price_options
                    else 0
                ),
            )

            sp_approval = st.selectbox(
                "Approval Process",
                approval_options,
                index=(
                    approval_options.index(selected_contact["approval_process"])
                    if selected_contact.get("approval_process") in approval_options
                    else 0
                ),
            )

            st.markdown("### Relationship")

            trust_options = ["", "Low", "Medium", "High"]
            stage_options = ["", "New", "Developing", "Established", "Strategic"]

            sp_trust = st.selectbox(
                "Trust Level",
                trust_options,
                index=(
                    trust_options.index(selected_contact["trust_level"])
                    if selected_contact.get("trust_level") in trust_options
                    else 0
                ),
            )

            sp_stage = st.selectbox(
                "Relationship Stage",
                stage_options,
                index=(
                    stage_options.index(selected_contact["relationship_stage"])
                    if selected_contact.get("relationship_stage") in stage_options
                    else 0
                ),
            )

            save_playbook = st.form_submit_button("💾 Save Structured Playbook")

            if save_playbook:

                supabase.table("contacts").update(
                    {
                        "formality": sp_formality or None,
                        "preferred_channel": sp_channel or None,
                        "meeting_style": sp_meeting or None,
                        "decision_speed": sp_decision or None,
                        "price_sensitivity": sp_price or None,
                        "approval_process": sp_approval or None,
                        "trust_level": sp_trust or None,
                        "relationship_stage": sp_stage or None,
                    }
                ).eq("id", selected_contact["id"]).execute()

                st.success("✅ Structured Playbook saved successfully")
                st.rerun()

    else:
        st.info("No contacts yet")
if page == "✅ Tasks":

    st.header("✅ Tasks")

    company_names = [c["name"] for c in companies.data]

    selected_company_name = st.selectbox(
        "🏢 Company",
        company_names,
        key="tasks_company",
    )

    selected_company = next(
        c for c in companies.data if c["name"] == selected_company_name
    )

    contacts_response = (
        supabase.table("contacts")
        .select("*")
        .eq("company_id", selected_company["id"])
        .execute()
    )

    contact_names = [c["name"] for c in contacts_response.data]

    if not contact_names:
        st.info("No contacts found for this company")
        st.stop()

    selected_name = st.selectbox(
        "👤 Contact",
        contact_names,
        key="tasks_contact",
    )

    selected_contact = next(
        c for c in contacts_response.data if c["name"] == selected_name
    )

    # =========================================
    # ✅ CLIENT TASKS
    # =========================================

    st.subheader("✅ Client Tasks")

    tasks = (
        supabase.table("tasks")
        .select("*")
        .eq("contact_id", selected_contact["id"])
        .order("created_at", desc=True)
        .execute()
    )

    if tasks.data:

        for task in tasks.data:

            status_icon = "✅" if task["status"] == "Completed" else "⬜"

            task_text = (
                f"{status_icon} {task['title']} "
                f"(Due: {task['due_date'] or 'No due date'})"
            )

            if task.get("completed_at"):
                task_text += f" | Completed: {task['completed_at'][:10]}"

            st.write(task_text)

            task_owner = next(
                (
                    u["name"]
                    for u in sales_users.data
                    if u["id"] == task.get("owner_id")
                ),
                "Unassigned",
            )

            st.caption(f"👤 Owner: {task_owner}")

            if task["status"] == "Open":

                completion_date = st.date_input(
                    f"Completion Date #{task['id']}",
                    key=f"completion_date_{task['id']}",
                )

                if st.button(
                    f"✔ Complete Task #{task['id']}",
                    key=f"complete_task_{task['id']}",
                ):

                    supabase.table("tasks").update(
                        {
                            "status": "Completed",
                            "completed_at": completion_date.isoformat(),
                        }
                    ).eq("id", task["id"]).execute()

                    st.success("✅ Task completed")
                    st.rerun()

    else:
        st.info("No tasks for this client yet")

    st.markdown("---")

    # =========================================
    # ✅ ADD TASK
    # =========================================

    st.subheader("➕ Add Task")

    if "task_form_version" not in st.session_state:
        st.session_state.task_form_version = 0

    with st.form(f"add_task_form_{st.session_state.task_form_version}"):

        task_title = st.text_input(
            "Task",
            placeholder="Send proposal, schedule follow-up...",
        )

        due_date = st.date_input("Due Date")

        save_task = st.form_submit_button("Save Task")

        if save_task and task_title:

            supabase.table("tasks").insert(
                {
                    "contact_id": selected_contact["id"],
                    "title": task_title,
                    "owner_id": selected_contact.get("owner_id"),
                    "due_date": str(due_date),
                    "status": "Open",
                }
            ).execute()

            st.success("✅ Task created")
            st.rerun()
if page == "📞 Interactions":

    st.header("📞 Interactions")

    company_names = [c["name"] for c in companies.data]

    selected_company_name = st.selectbox(
        "🏢 Company",
        company_names,
        key="interactions_company",
    )

    selected_company = next(
        c for c in companies.data if c["name"] == selected_company_name
    )

    contacts_response = (
        supabase.table("contacts")
        .select("*")
        .eq("company_id", selected_company["id"])
        .execute()
    )

    contact_names = [c["name"] for c in contacts_response.data]

    if not contact_names:
        st.info("No contacts found for this company")
        st.stop()

    selected_name = st.selectbox(
        "👤 Contact",
        contact_names,
        key="interactions_contact",
    )

    selected_contact = next(
        c for c in contacts_response.data if c["name"] == selected_name
    )

    # =========================================
    # ✅ INTERACTION HISTORY
    # =========================================

    st.subheader("📜 Interaction History")

    interactions = (
        supabase.table("interactions")
        .select("*")
        .eq("contact_id", selected_contact["id"])
        .order("created_at", desc=True)
        .execute()
    )

    if interactions.data:

        for interaction in interactions.data:

            transport = interaction.get("transportation_cost") or 0
            parking = interaction.get("parking_cost") or 0
            other = interaction.get("other_expenses") or 0

            total_expense = transport + parking + other

            st.markdown(f"### {interaction['type']}")

            interaction_owner = next(
                (
                    u["name"]
                    for u in sales_users.data
                    if u["id"] == interaction.get("owner_id")
                ),
                "Unassigned",
            )

            st.caption(f"👤 Owner: {interaction_owner}")

            st.write(f"📅 Date: {interaction.get('interaction_date', 'Not set')}")

            if interaction.get("from_location") or interaction.get("to_location"):
                st.write(
                    f"📍 {interaction.get('from_location', '')} → "
                    f"{interaction.get('to_location', '')}"
                )

            if interaction.get("distance_km"):
                st.write(f"🚗 Distance: {interaction.get('distance_km')} KM")

            if total_expense:
                st.write(f"💰 Total Expense: {total_expense:.2f}")

            if interaction.get("notes"):
                st.markdown(f"📝 {format_text(interaction['notes'])}")

            if interaction.get("insights_learned"):
                st.markdown(
                    f"🧠 Insight: " f"{format_text(interaction['insights_learned'])}"
                )

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
            i["insights_learned"] for i in interactions.data if i["insights_learned"]
        ]

        if all_insights:

            combined_insights = "\n\n".join(all_insights)

            st.markdown(format_text(combined_insights))

        else:
            st.info("No insights captured yet")

    else:
        st.info("No interaction data yet")

    # =========================================
    # ✅ KEY PATTERNS
    # =========================================

    st.markdown("---")
    st.subheader("📊 Key Patterns")

    combined_text = ""

    if interactions.data:
        combined_text += " ".join(
            [
                i["insights_learned"].lower()
                for i in interactions.data
                if i["insights_learned"]
            ]
        )

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

            st.markdown(f"✅ **{field.replace('_', ' ').title()}** → **{value}**")

            st.caption(f"Reason: {suggestion_reasons.get(field, 'Pattern detected')}")

        if st.button("⚡ Apply Suggestions"):

            supabase.table("contacts").update(suggestions).eq(
                "id", selected_contact["id"]
            ).execute()

            st.success("✅ Suggestions applied")
            st.rerun()

    else:
        st.info("No suggestions available")

    # =========================================
    # ✅ ADD INTERACTION
    # =========================================

    st.subheader("➕ Log Interaction")

    if "interaction_form_version" not in st.session_state:
        st.session_state.interaction_form_version = 0

    with st.form(f"interaction_form_{st.session_state.interaction_form_version}"):

        interaction_type = st.selectbox(
            "Type",
            ["Call", "Meeting", "WhatsApp", "Email"],
        )

        interaction_date = st.date_input("Interaction Date")

        st.markdown("### 🚗 Travel & Expenses")

        from_location = st.text_input("From Location")

        to_location = st.text_input("To Location")

        distance_km = st.number_input(
            "Distance (KM)",
            min_value=0.0,
            step=1.0,
        )

        transportation_cost = st.number_input(
            "Transportation Cost",
            min_value=0.0,
            step=10.0,
        )

        parking_cost = st.number_input(
            "Parking Cost",
            min_value=0.0,
            step=5.0,
        )

        other_expenses = st.number_input(
            "Other Expenses",
            min_value=0.0,
            step=5.0,
        )

        total_expense = transportation_cost + parking_cost + other_expenses

        st.info(f"💰 Total Expense: {total_expense:.2f}")

        notes = st.text_area("What happened?")

        insights = st.text_area(
            "What did you learn about this client?",
            placeholder="Capture behavior, preferences, reactions...",
        )

        submitted_interaction = st.form_submit_button("Save Interaction")

        if submitted_interaction:

            supabase.table("interactions").insert(
                {
                    "contact_id": selected_contact["id"],
                    "owner_id": selected_contact.get("owner_id"),
                    "type": interaction_type,
                    "interaction_date": str(interaction_date),
                    "from_location": from_location,
                    "to_location": to_location,
                    "distance_km": distance_km,
                    "transportation_cost": transportation_cost,
                    "parking_cost": parking_cost,
                    "other_expenses": other_expenses,
                    "notes": notes,
                    "insights_learned": insights,
                }
            ).execute()

            st.success("✅ Interaction saved!")
            st.session_state.interaction_form_version += 1
            st.rerun()
if page == "👤 Contacts":
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

            company_names = [c["name"] for c in companies.data]

            selected_company = st.selectbox("Company", company_names)

            selected_company_record = next(
                c for c in companies.data if c["name"] == selected_company
            )

            company_owner = next(
                (
                    u["name"]
                    for u in sales_users.data
                    if u["id"] == selected_company_record.get("owner_id")
                ),
                "Unassigned",
            )

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
                owner_id = selected_company_record["owner_id"]
                company_record = next(
                    c for c in companies.data if c["name"] == selected_company
                )
                supabase.table("contacts").insert(
                    {
                        "name": name,
                        "company": selected_company,
                        "company_id": company_record["id"],
                        "role": role,
                        "email": email,
                        "phone": phone,
                        "communication_style": communication_style,
                        "owner_id": owner_id,
                        "personality_traits": personality_traits,
                        "preferences": preferences,
                        "lifestyle_notes": lifestyle_notes,
                        "negotiation_notes": negotiation_notes,
                        "relationship_summary": relationship_summary,
                        "playbook": playbook,
                    }
                ).execute()

                st.success("✅ Contact saved successfully!")

                st.session_state.show_form = False
                st.rerun()
