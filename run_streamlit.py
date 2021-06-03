import subprocess
import shlex

subprocess.call(shlex.split("streamlit run app.py"), shell=True)