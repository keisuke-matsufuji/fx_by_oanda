FROM lambci/lambda:python3.8
# FROM lambci/lambda:build-python3.8

# WORKDIR /var/task
WORKDIR /opt

ADD ./functions/fx_auto_trading .
ADD ./requirements.txt .

# RUN pip3 install -r requirements.txt -t /var/task
# RUN zip -9 deploy_package.zip lambda_function.py
# RUN zip -r9 deploy_package.zip .

RUN pip3 install -r requirements.txt -t ./python
RUN zip -9 deploy_package.zip lambda_function.py
RUN zip -r9 deploy_package.zip .

# CMD python -c "import lambda_function; lambda_function.lambda_handler({}, None)"
