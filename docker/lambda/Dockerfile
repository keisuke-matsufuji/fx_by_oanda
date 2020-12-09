FROM lambci/lambda:python3.8

WORKDIR /var/task
# COPY ./functions/docker_test/requirements.txt /var/task
# COPY requirements.txt /var/task 
# COPY ./functions/docker_test /var/task
# COPY . .
# COPY ./functions/docker_test /var/task

# ADD ./functions/docker_test/requirements.txt ./var/task 
# ADD ./functions/docker_test /var/task
# ADD ./requirements.txt .
ADD ./functions/deploy_test .

# CMD ls

# RUN /bin/cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
#   pip install -r requirements.txt -t /var/task
# RUN pip install -r requirements.txt -t /var/task
# RUN zip -r pandas-1.0.3.zip ./python > /dev/null
# RUN chmod +x docker-entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]
# COPY docker-node-entrypoint.sh /entrypoint.sh
# RUN chmod +x entrypoint.sh 
# ENTRYPOINT ["/entrypoint.sh"] 
# RUN pip install -r requirements.txt -t .

RUN pip3 install -r requirements.txt -t /var/task
# RUN zip -9 deploy_package.zip lambda_function.py
# RUN zip -r9 deploy_package.zip .

# CMD zip -9 deploy_package.zip ./functions/docker_test/lambda_function.py && \
#   zip -r9 deploy_package.zip *
# CMD pip install -r /var/task/requirements.txt -t /opt
# CMD pip install -r requirements.txt -t /var/task && \
#   zip -9 deploy_package.zip lambda_function.py && \
#   zip -r9 deploy_package.zip * && \
#   python lambda_function.py
CMD zip -9 deploy_package.zip lambda_function.py && \
  zip -r9 deploy_package.zip * && \
  python -c "import lambda_function; lambda_function.lambda_handler({}, None)"
# CMD pip3 install -r requirements.txt -t /var/task && \
  # chmod -R 755 /var/task/ && \
  # zip -9 deploy_package.zip lambda_function.py && \
  # zip -r9 ../deploy_package.zip *
# CMD pip install -r requirements.txt -t python/lib/python3.8/site-packages/ && \
#   zip -9 deploy_package.zip lambda_function.py && \
#   zip -r ../deploy_package.zip ./python ./*