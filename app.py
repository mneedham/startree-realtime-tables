import pandas as pd
import streamlit as st
from pinotdb import connect
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import plotly.express as px

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=10000, key="fizzbuzzcounter")


# st.set_page_config(layout="wide", page_title="Wikipedia Updates")
st.title("Wikipedia events")

now = datetime.now()
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.write(f"Last update: {dt_string}")

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')

query = """
select user, count(user) AS count
from wikievents 
group by user
order by count DESC
LIMIT 10
"""

curs = conn.cursor()
curs.execute(query)
df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

st.header("Users making changes")
st.markdown("""
<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.table(df.style.format({"count(*)": "{:,}"}))

with right:
    fig = px.bar(df, x="user", y="count", color_discrete_sequence =['#0b263f']*len(df),)
    st.write(fig)

query = """
select count(*) 
from wikievents 
where wikievents."timestamp" > cast(ago('PT3H') as long) / 1000
"""

curs = conn.cursor()
curs.execute(query)
df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])


st.header("Events in the last 3 hours")
st.table(df.style.format({"count(*)": "{:,}"}))