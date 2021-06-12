#from os import name
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Meine Imports
import database_conn
import my_code_snippets
import bokeh_map_test

#print(st.__version__) ## ==> 0.82.0 ist wichtig für Bokeh Link: https://github.com/streamlit/streamlit/issues/1226
def main():
    st.write("""
    # WI4Future Database
    """)

    ## Interaktive Karte
    if st.button('Zeige Karte'):
        st.write("""
        # Letzen Daten von Messtationen
        """)
        p = bokeh_map_test.create_map()
        st.bokeh_chart(p, use_container_width=True)

    ## Auswahl der Daten nach Namen
    name_list= database_conn.querry_names()
    name = st.selectbox('Select name', name_list, index=8)

    df = pd.DataFrame(database_conn.get_values(name), columns=['Time','Ort','Temperatur','Feuchte','Druck'])
    st.dataframe(df)
    st.markdown(my_code_snippets.get_table_download_link(df), unsafe_allow_html=True)

    new_df = df[df.Time > pd.to_datetime("23/5/2021")] #Dataframe nur mit Daten seit diesem Jahr 

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Temperatur, name='Temperatur'), row=1, col=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Feuchte, name='Feuchte'), row=1, col=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Druck, name='Feuchte'), row=2, col=1)
    st.plotly_chart(fig, use_container_width=True)

    import matplotlib.pyplot as plt
    plt.plot(df.index, df.Temperatur, label='Temperatur')
    plt.plot(df.index, df.Feuchte, label='Feuchte')
    #plt.plot(new_df.index, new_df.Druck, label='Druck')
    plt.legend(loc='upper left')
    plt.title(f"Termeraturverlauf von {name}")
    st.pyplot(plt)

if __name__ == "__main__":
    main()


