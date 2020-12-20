FROM lambci/lambda:python3.8

WORKDIR /var/task

ADD ./functions/fx_auto_trading .
ADD ./requirements.txt .

RUN pip3 install -r requirements.txt -t /var/task
RUN zip -9 deploy_package.zip lambda_function.py
RUN zip -r9 deploy_package.zip .

# RUN pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/
# RUN zip -r deploy.zip ./python > /dev/null

# RUN zip -9 deploy_package.zip lambda_function.py
# RUN zip -r9 deploy_package.zip *

# CMD zip -9 deploy_package.zip ./functions/docker_test/lambda_function.py && \
#   zip -r9 deploy_package.zip *
# CMD pip install -r /var/task/requirements.txt -t /opt
# CMD pip install -r requirements.txt -t /var/task && \
#   zip -9 deploy_package.zip lambda_function.py && \
#   zip -r9 deploy_package.zip * && \
#   python lambda_function.py




CMD python -c "import lambda_function; lambda_function.lambda_handler({}, None)"

# CMD zip -9 deploy_package.zip lambda_function.py && \
#   zip -r9 deploy_package.zip * && \
#   python -c "import lambda_function; lambda_function.lambda_handler({}, None)"

# CMD zip -9 deploy_package.zip lambda_function.py && \
#   zip -r9 deploy_package.zip * && \
#   python -c "import lambda_function; lambda_function.lambda_handler({}, None)"
  # python -c "import main; main.lambda_handler({}, None)"



# CMD pip3 install -r requirements.txt -t /var/task && \
  # chmod -R 755 /var/task/ && \
  # zip -9 deploy_package.zip lambda_function.py && \
  # zip -r9 ../deploy_package.zip *
# CMD pip install -r requirements.txt -t python/lib/python3.8/site-packages/ && \
#   zip -9 deploy_package.zip lambda_function.py && \
#   zip -r ../deploy_package.zip ./python ./*