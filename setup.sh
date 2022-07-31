mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yila22@lehigh.edu\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml