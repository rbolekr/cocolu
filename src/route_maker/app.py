import streamlit as st
from st_click_detector import click_detector
from resources import generate_wall_cards, load_wall_svgs

st.set_page_config(layout="wide")
st.title("Climbing Route Maker")

# We use a 'wizard'-like interface here which is not a native concept in Streamlit. It's something that can be accomplished by using session_state
# variables which then manage which bits of the UI are turned on and off in turn. Streamlit runs all the code over an over on user input so normal
# variables always get reset but session_state is magical and persists for the duration of the app's execution.
#
# It's always possible to log to the console a variable you're interested in with code like this:
#
# print(f"[DEBUG] clicked: {clicked}")
#
# However, this snippet here below add the contents of the session_state to the (expandable) sidebar.
@st.fragment
def debug_sidebar():
    with st.sidebar:
        st.subheader("Session State")
        st.json(dict(st.session_state), expanded=False)
        if st.button("Clear state"):
            st.session_state.clear()
            st.rerun()

debug_sidebar()

if 'selected_wall' not in st.session_state:
    st.divider()
    st.markdown("""**Please select a wall:**""")

    # The routing algorithms need some properties of the wall. Since we already have svg files to represent the walls, I am going to use them to
    # store the extra data. At the moment that extra data is just default width and height but in a real application you could have a lot more
    # geometry data to describe the real wall. Then the more appropriate place would be a database or perhaps just JSON files.
    #
    # So what is going on here is the svg files are loaded and the 'metadata' is read in together with the svg visual data. Then, when the
    # click_detector returns the id of the selected wall, that id is used to look up the metadata. Since that's the only thing we care
    svgs = load_wall_svgs()
    clicked = click_detector(generate_wall_cards(svgs))

    if clicked:
        st.session_state.selected_wall = clicked
        st.session_state.wall_metadata = svgs[clicked]["metadata"]

        # Here we force a manual rerun of the logic which gets us in the next page of the wizard.
        st.rerun()

elif 'selected_algo' not in st.session_state:
    st.divider()
    st.markdown("""**Please select a routing algorithm:**""")