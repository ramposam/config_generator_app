import streamlit as st

from helpers.variables import Variables


def inject_css(html):
    st.markdown(html,unsafe_allow_html=True)

def dummy():
    pass

def get_df_from_query_with_error(query):
    try:
        if Variables.snowflake_conn is None:
            return None
        cur = Variables.snowflake_conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
        return df

    except Exception as ex:
        print(ex.__str__())
        return None