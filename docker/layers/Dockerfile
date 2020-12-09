FROM lambci/lambda:build-python3.8

WORKDIR /opt
ADD ./requirements.txt .
ADD ./functions/deploy_test .
# ADD . .

# CMD ls

# RUN /bin/cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
#   pip install -r requirements.txt -t /var/task
# RUN pip install -r requirements.txt -t /var/task
# RUN pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/
RUN pip3 install -r requirements.txt -t ./python

# CMD zip -9 deploy_package.zip ./functions/docker_test/lambda_function.py && \
#   zip -r9 deploy_package.zip *
# CMD pip install -r requirements.txt && \
#   zip -9 deploy_package.zip main.py && \
#   zip -r9 deploy_package.zip *
# CMD zip -r layers.zip ./python > /dev/null
# CMD zip -r layers.zip ./python

CMD zip -9 layers.zip main.py && \
  zip -r9 layers.zip *