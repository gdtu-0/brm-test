FROM python:3.13-alpine

# Update and upgrade system
RUN apk -U upgrade

# Install development packages
RUN apk add gcc make rust cargo libpq-dev

# Install base dagster modules
RUN pip install --upgrade pip && pip install dagster dagster-webserver

# Create dagster home dir
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
COPY dagster/dagster.yaml $DAGSTER_HOME

# Create dagster app dir and copy workspace.yaml config file
ENV DAGSTER_APP=/opt/dagster/app
RUN mkdir -p $DAGSTER_APP
COPY dagster/workspace.yaml $DAGSTER_APP
WORKDIR $DAGSTER_APP

# Install requirements
COPY dagster/requirements.txt $DAGSTER_HOME/requirements.txt
RUN pip install -r $DAGSTER_HOME/requirements.txt

# Expose dagster webserver port
EXPOSE 3000

# Start everything
ENTRYPOINT ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]