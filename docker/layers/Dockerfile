FROM lambci/lambda:build-python3.8

WORKDIR /opt
ADD ./requirements.txt .
# RUN echo "before pip install"
RUN pip3 install -r requirements.txt -t ./python
# RUN echo "$(pwd)"
CMD zip -r layers.zip ./python > /dev/null
