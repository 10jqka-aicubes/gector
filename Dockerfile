FROM 10jqkaaicubes/cuda:11.0-py3.8.5

COPY ./ /home/jovyan/gector 

RUN cd /home/jovyan/gector  && \
    python -m pip install -r requirements.txt 