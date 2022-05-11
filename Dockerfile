FROM ubuntu:18.04

# RUN apt-get update -y \
# 	&& apt-get install -y python3-pip python3-dev
# RUN pip3 install --upgrade pip

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# (...)

# Python package management and basic dependencies
RUN apt-get install -y curl python3.7 python3.7-dev python3.7-distutils

# Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

# Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.7

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

COPY ./ /

EXPOSE 8866
RUN pip3 install -r requirements.txt
RUN /usr/bin/python3.7 -m nltk.downloader floresta
#RUN sed -i "s/% len(self._regexps)/% len(self._regexs)/g" /usr/local/lib/python3.7/dist-packages/nltk/tag/sequential.py

RUN sed -i "s/for regexp, tag in self._regexps/for regexp, tag in self._regexs/g" /usr/local/lib/python3.7/dist-packages/nltk/tag/sequential.py
RUN sed -i "s/len(self._regexps)/len(self._regexs)/g" /usr/local/lib/python3.7/dist-packages/nltk/tag/sequential.py


CMD ["/usr/bin/python3.7", "serve.py"]