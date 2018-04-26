FROM daocloud.io/library/centos:7.3.1611
MAINTAINER DSP
ENV PORT TRUE

RUN yum -y install epel-release && \
    yum -y install python-pip && \
    pip install Flask && \
    pip install simplejson &&\
    pip install flask-restful
