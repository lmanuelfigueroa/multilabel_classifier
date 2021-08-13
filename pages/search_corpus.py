import streamlit as st

screen_tags = ['','aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def app() -> None:
    st.title("Search Corpus")
    main = st.form("current")
    selected_tag = main.selectbox("Select Tag to Search Documents",screen_tags)
    #st.session_state.tag = selected_tag
    number = main.number_input("Enter a percentage: ex: 50",min_value = 0, max_value = 100, value = 50)
    #st.session_state.percentage = number
    submit_button = main.form_submit_button("Submit")
    if submit_button:
        st.write(selected_tag + " and "+ str(number))