import base64
def get_table_download_link(df, name):
    #https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/2
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}_wi4future.csv">CSV-Datei Herunterladen</a>'
    return href