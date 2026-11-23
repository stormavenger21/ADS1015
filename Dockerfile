FROM alpine:3.18.3

#RUN apt update && apt install -y python3 python3-venv python3-pip

RUN apk add --no-cache \
    nginx \
    python3 \
    py3-pip \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir Flask smbus2

# Nginx configuration
COPY files/nginx.conf /etc/nginx/nginx.conf

# Web interface and Cockpit registration
RUN mkdir -p /ADS1015
RUN mkdir -p /ADS1015/files
COPY files/register_service /ADS1015/files/register_service


# Python sensor driver and API
RUN mkdir -p /ADS1015/app
COPY app/ /ADS1015/app

# Startup script
COPY files/entrypoint.sh /ADS1015/files/entrypoint.sh
RUN chmod +x /ADS1015/files/entrypoint.sh

WORKDIR /ADS1015/app

#Host port is dynamically assigned
#Container port is 80
LABEL permissions='{\
  "ExposedPorts": {\
    "5000/tcp": {}\
  },\
  "HostConfig": {\
    "CpuPeriod":100000,\
    "CpuQuota":20000,\
    "Memory":209715200,\
    "PortBindings": {\
      "5000/tcp": [\
        {\
          "HostPort": "5000/tcp"\ 
        }\
      ]\
    },\
    "Devices": [\
      {\
        "PathOnHost": "/dev/i2c-1",\
        "PathInContainer": "/dev/i2c-1",\
        "CgroupPermissions": "rw"\
      }\
    ]\
  }\
}'

LABEL authors='[{"name":"stormavenger21"}]'
LABEL readme="https://github.com/stormavenger21/ADS1015/blob/main/README.md"

ENTRYPOINT ["/ADS1015/files/entrypoint.sh"]
