import streamlit as st

from helpers.variables import Variables


def inject_css(html):
    st.markdown(html,unsafe_allow_html=True)

def dummy():
    pass

def get_df_from_query_with_error(query):
    try:
        cur = Variables.snowflake_conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
        return df

    except Exception as ex:
        return None
        print(ex.__str__())