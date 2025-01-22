import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

@st.dialog("Wishlist")
def wishlist_dialog():
    st.write("part1")
    st.write("part2")
    new_search_term = st.text_input("Add search term", placeholder="part3")
    if new_search_term:
        st.info(f"Inserting {new_search_term} to the database")

@st.dialog("Auth")
def login_dialog():
    tab1, tab2, tab3 = st.tabs(["Login", "New Client", "Forget Password"])

    # doc: https://github.com/mkhorasani/Streamlit-Authenticator?ref=blog.streamlit.io
    authenticator = st.session_state.authenticator
    with tab1:
        try:
            # authenticator.login(location='main', captcha=True)
            authenticator.login(location='main')
        except Exception as e:
            st.error(e)
    with tab2:
        st.write("DISABLED")
        # try:
        #     email_of_registered_user, \
        #     username_of_registered_user, \
        #     name_of_registered_user = authenticator.register_user(
        #         pre_authorized=config['pre-authorized']['emails'],
        #         merge_username_email=True,
        #         )
        #     if email_of_registered_user:
        #         st.success('User registered successfully')
        # except Exception as e:
        #     st.error(e)
    with tab3:
        st.write("DISABLED")
        # try:
        #     username_of_forgotten_password, \
        #     email_of_forgotten_password, \
        #     new_random_password = authenticator.forgot_password()
        #     if username_of_forgotten_password:
        #         st.success('New password to be sent securely')
        #         # The developer should securely transfer the new password to the user.
        #     elif username_of_forgotten_password == False:
        #         st.error('Username not found')
        # except Exception as e:
        #     st.error(e)
    
    if st.session_state['authentication_status']:
        # authenticator.logout()
        # authenticator.logout(location='sidebar') # cannot write to outside container
        # st.toast(f'Welcome *{st.session_state["name"]}*', icon='😍')
        st.rerun()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

def header():
    # init the authenticator if not yet
    if "authenticator" not in st.session_state:
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        st.session_state.authenticator = authenticator
    if st.session_state['authentication_status'] is None:
        st.sidebar.write("STATUS NONE")
        st.sidebar.button("Login", on_click=login_dialog)
        # name, authentication_status, username = st.session_state.authenticator.login(location='sidebar')
    elif st.session_state['authentication_status'] is False:
        st.sidebar.write("STATUS FALSE")
        if st.session_state["name"]:
            st.toast(f'*{st.session_state["name"]}* signed out', icon='😍')
        st.sidebar.button("Login", on_click=login_dialog)
    elif st.session_state['authentication_status'] is True:
        st.sidebar.write("STATUS TRUE")
        if "admin" in st.session_state["roles"]:
            st.sidebar.write(st.session_state)
        st.session_state.authenticator.logout(location='sidebar')
        # st.session_state.authenticator.logout(location='sidebar', callback=logout)
        # st.toast(f'Welcome *{st.session_state["name"]}*', icon='😍')

    if st.session_state['authentication_status'] is True:
        st.toast(f'Welcome *{st.session_state["name"]}*', icon='😍')
        st.sidebar.button("Wishlist", on_click=wishlist_dialog)