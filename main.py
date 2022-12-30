import imp
import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import altair as alt
from PIL import Image
import base64
import tarfile
import os
import requests
from backend import *

st.set_page_config(page_title="arXiv2Latex Downloader", page_icon=":page_with_curl:", layout="wide", initial_sidebar_state="expanded", menu_items={
    "About": "Download the source latex code of multiple arXiv paper with one click"
})

# title
st.title("arXiv2Latex Downloader")

# input arxiv links to download
pdf_links_input = st.text_area("Please input the paper links you want to download following the format (Currently supports up to 10 links).", "")
st.markdown("""
            Input example:
            ```Plain Text
            https://arxiv.org/abs/1512.03385
            https://arxiv.org/abs/1706.03762
            https://arxiv.org/abs/2009.09724
            """)
## one click download
crawling_or_not = st.button("Crawling the latex Code")
if crawling_or_not:
    print("Crawling...")
    pdf_lists = pdf_links_input.split("\n")
    print(pdf_lists)
    # cleaning the pdf lists
    pdf_lists = [i.strip() for i in pdf_lists if len(i) > 0]
    # TODO: limit the number of paper up to 10 since I am not sure that whether base64 support large file download
    try: 
        if len(pdf_lists) > 10:
            st.warning("Currently only support up to 10 papers. Please input less than 10 papers.")
        else:
            # parsing
            base='./download/'
            project_name = get_timestamp().replace(" ","-")
            base = os.path.join(base,project_name)
            make_dir_if_not_exist(base)
            
            # st.write(download_status)
            with st.spinner("Downloading papers..."):
                # progress bar
                bar = st.progress(0)
                download_status = st.empty()
                N = len(pdf_lists)
                for i, pdf_link in tqdm(enumerate(pdf_lists)):
                    title = get_name_from_arvix(pdf_link)
                    file_stamp = pdf_link.split("/")[-1]
                    source_link = "https://arxiv.org/e-print/"+file_stamp
                    inp = os.path.join(base,'input')
                    make_dir_if_not_exist(inp)
                    out = os.path.join(base,'output')
                    make_dir_if_not_exist(out)
                    response = requests.get(source_link)
                    filename = file_stamp+".tar.gz"
                    filepath = os.path.join(inp,filename)
                    open(filepath, "wb").write(response.content)
                    outpath = os.path.join(out,title)
                    untar(filepath,outpath)
                    
                    # finish one paper
                    bar.progress((i+1)/N)
                    download_status.text(f"Iteration [{i+1}/{N}]: Finish Downloading of "+title)
            
            with st.spinner("Archiving as Zip Files..."):
                # save it as zip file
                filepath = archive_dir(out,os.path.join(base,project_name))

                # download
                b64 = ToBase64(filepath).decode()
            href = f"<a href='data:file/csv;base64,{b64}' download='arxiv2latex-output-{datetime.datetime.now()}.zip' color='red'>Click here to Download the Output Latex Zip Files</a>"
            st.markdown(href, unsafe_allow_html=True)
                
            # 状态
            st.success("Finished")
    except Exception as e:
        st.error("Something goes wrong. Please check the input or concat me to fix this bug. Error message: \n"+str(e))
