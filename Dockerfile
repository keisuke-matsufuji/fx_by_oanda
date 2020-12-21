# Dploy to Lambda Layer

FROM lambci/lambda:build-python3.8

WORKDIR /opt
# ADD ./requirements.txt .
ADD requirements.txt .
# ADD ./opt/requirements.txt .
RUN pip3 install -r requirements.txt -t ./python

CMD zip -r layers.zip ./python > /dev/null