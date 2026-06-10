import streamlit as st
import requests

API_URL = "http://localhost:5000"


def api_get(path):
    try:
        response = requests.get(url=f"{API_URL}{path}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure py run.py is running.")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_post(path, data):
    try:
        response = requests.post(url=f"{API_URL}{path}", json=data, timeout=5)
        if response.status_code in (200, 201):
            return response.json()
        else:
            error = response.json().get("error", "Unknown error")
            st.error(f"Error: {error}")
            return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_delete(path):
    try:
        response = requests.delete(url=f"{API_URL}{path}", timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"API error: {e}")
        return False


def modifier_str(mod):
    return f"+{mod}" if mod >= 0 else str(mod)


def format_bounty(bounty: int) -> str:
    if bounty == 0:
        return "None"
    return f"{bounty:,} Berry"


st.set_page_config(
    page_title="One Piece Character Builder",
    page_icon="☠️",
    layout="wide",
)

st.sidebar.title("☠️ One Piece Builder")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    label="Navigate",
    options=["My Crew", "Create Character", "Classes & Races"],
)

# ── My Crew ──────────────────────────────────────────────────────────────────
if page == "My Crew":
    st.title("🏴‍☠️ My Crew")

    characters = api_get("/characters/")

    if characters is None:
        st.stop()

    if len(characters) == 0:
        st.info("No crew members yet. Go to Create Character to make your first one!")

    for char in characters:
        with st.expander(
                f"{char['name']} — Level {char['level']} "
                f"{char['race']} {char['character_class']}"
        ):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric(label="Max HP", value=char["computed"]["max_hit_points"])
            col2.metric(label="Armour Class", value=char["computed"]["armour_class"])
            col3.metric(label="Proficiency", value=f"+{char['computed']['proficiency_bonus']}")
            col4.metric(label="Level", value=char["level"])
            col5.metric(label="🏴 Bounty", value=format_bounty(char["bounty"]))

            st.markdown("---")

            stats = char["stats"]
            cols = st.columns(6)
            for i, (stat_name, values) in enumerate(stats.items()):
                cols[i].metric(
                    stat_name.capitalize(),
                    values["base"],
                    modifier_str(values["modifier"]),
                )

            if char.get("backstory"):
                st.markdown("---")
                st.markdown(f"*{char['backstory']}*")

            if st.button(label="Delete", key=f"del_{char['id']}"):
                if api_delete(f"/characters/{char['id']}"):
                    st.success(f"{char['name']} deleted.")
                    st.rerun()

# ── Create Character ─────────────────────────────────────────────────────────
elif page == "Create Character":
    st.title("⚓ Create Your Character")

    classes_data = api_get("/classes/")
    races_data = api_get("/races/")

    if classes_data is None or races_data is None:
        st.stop()

    class_names = [c["name"] for c in classes_data]
    race_names = [r["name"] for r in races_data]
    class_map = {c["name"]: c for c in classes_data}
    race_map = {r["name"]: r for r in races_data}

    st.markdown("### Basic Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Character Name")
    with col2:
        chosen_class = st.selectbox(label="Class", options=class_names)
    with col3:
        chosen_race = st.selectbox(label="Race", options=race_names)

    level = st.slider(label="Level", min_value=1, max_value=20, value=1)

    col_a, col_b = st.columns(2)
    with col_a:
        cls = class_map[chosen_class]
        st.info(f"**{cls['name']}** — {cls['description']}")
    with col_b:
        race = race_map[chosen_race]
        bonuses = [
            f"{k.capitalize()} +{v}" for k, v in race["bonuses"].items() if v > 0
        ]
        st.info(f"**{race['name']}** — {race['description']}")

    st.markdown("### Stats")


    race = race_map[chosen_race]
    cls = class_map[chosen_class]
    bonuses = {k: v for k, v in race["bonuses"].items() if v != 0}

    if st.button("Roll Random Stats"):
        rolled = api_get("/characters/roll")
        if rolled:
            for stat, value in rolled.items():
                st.session_state[f"stat_{stat}"] = value

    stat_names = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    stat_values = {}
    cols = st.columns(6)
    for i, stat in enumerate(stat_names):
        with cols[i]:
            default = st.session_state.get(f"stat_{stat}", 10)
            base = st.number_input(
                stat.capitalize(),
                min_value=1,
                max_value=20,
                value=default,
                key=f"input_{stat}",
            )
            stat_values[stat] = base
            bonus = bonuses.get(stat, 0)
            total = base + bonus
            modifier = (total - 10) // 2
            mod_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            if bonus != 0:
                bonus_str = f"+{bonus}" if bonus > 0 else str(bonus)
                st.caption(f"Race: {bonus_str} → Total: {total} ({mod_str})")
            else:
                st.caption(f"Total: {total} ({mod_str})")

    st.markdown("### Bounty")
    bounty = st.number_input(
        "Starting Bounty (Berry)",
        min_value=0,
        max_value=5_000_000_000,
        value=0,
        step=1_000_000,
        help="How much is your pirate worth? Most start at 0.",
    )

    st.markdown("### Backstory (optional)")
    backstory = st.text_area(
        label="Your character's history",
        height=100,
        placeholder="A pirate sailing the Grand Line in search of the One Piece.",
    )

    st.markdown("---")

    if st.button("Create Character"):
        if not name.strip():
            st.error("Your character needs a name!")
        else:
            result = api_post(
                path="/characters/",
                data={
                    "name": name.strip(),
                    "class_name": chosen_class,
                    "race_name": chosen_race,
                    "level": level,
                    "backstory": backstory,
                    "bounty": bounty,
                    **stat_values,
                },
            )
            if result:
                st.success(
                    f"{result['name']} created! "
                    f"HP: {result['computed']['max_hit_points']} | "
                    f"AC: {result['computed']['armour_class']} | "
                    f"Bounty: {format_bounty(result['bounty'])}"
                )
                st.balloons()

# ── Classes & Races ───────────────────────────────────────────────────────────
elif page == "Classes & Races":
    st.title("📖 Classes & Races")

    tab1, tab2 = st.tabs(["Classes", "Races"])

    with tab1:
        classes_data = api_get("/classes/")
        if classes_data:
            for cls in classes_data:
                with st.expander(f"{cls['name']} — d{cls['hit_die']}"):
                    st.write(cls["description"])
                    st.caption(f"Primary stat: {cls['primary_stat'].capitalize()}")

    with tab2:
        races_data = api_get("/races/")
        if races_data:
            for race in races_data:
                with st.expander(race["name"]):
                    st.write(race["description"])
                    bonuses = [
                        f"{k.capitalize()} +{v}" for k, v in race["bonuses"].items() if v > 0
                    ]
                    if bonuses:
                        st.success("Bonuses: " + " | ".join(bonuses))