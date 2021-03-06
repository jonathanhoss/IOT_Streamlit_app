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
    if st.button('Zeige Geo-Karte'):
        st.write("""
        ## Letze Daten von Messtationen
        """)
        p = bokeh_map_test.create_map()
        st.bokeh_chart(p, use_container_width=True)

    ## Auswahl der Daten nach Namen
    name_list= database_conn.querry_names()
    name = st.selectbox('Select name', name_list, index=8)

    st.write(f"""
    ## Datensätze von {name}
    """)
    df = pd.DataFrame(database_conn.get_values(name), columns=['Time','Ort','Temperatur','Feuchte','Druck'])
    st.dataframe(df.sort_index(ascending=False))
    # DOWNLOAD
    st.markdown(my_code_snippets.get_table_download_link(df, name), unsafe_allow_html=True)
    
    st.write(f"""
    ## Chronologisches Diagramm der Wetterdaten von {name}
    """)
    new_df = df[df.Time > pd.to_datetime("23/5/2021")] #Dataframe nur mit Daten seit diesem Jahr 

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Temperatur, name='Temperatur'), row=1, col=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Feuchte, name='Feuchte'), row=1, col=1)
    fig.add_trace(go.Scatter(x=new_df.Time, y=new_df.Druck, name='Druck'), row=2, col=1)
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    ## Graph mit ID als X-Achse
    Falls die Zeitdaten nicht richtig erfasst wurden kann es vorkommen, dass der obere Graph nicht angezeigt wird. Dann kann hier der Graph mit der ID anstatt der Zeit als X-Achse ausgegeben werden.
    """)
    if st.button('Hier anzeigen'):
        import matplotlib.pyplot as plt
        plt.plot(df.index, df.Temperatur, label='Temperatur [°C]')
        plt.plot(df.index, df.Feuchte, label='Feuchte [%]')
        #plt.plot(new_df.index, new_df.Druck, label='Druck')
        plt.legend(loc='upper left')
        plt.title(f"Termeraturverlauf von {name}")
        plt.xlabel("ID")
        st.pyplot(plt)

if __name__ == "__main__":
    main()


