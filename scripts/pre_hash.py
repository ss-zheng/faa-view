import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

with open('../auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
out = stauth.Hasher.hash_passwords(config['credentials'])
print(out)

hashed_passwords = stauth.Hasher(['ABC', 'def']).generate()