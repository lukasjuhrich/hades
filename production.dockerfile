FROM hades-base
MAINTAINER Sebastian Schrader <sebastian.schrader@agdsn.de>

COPY src /build/
RUN cd /build \
    && bower install --allow-root \
    && python3 setup.py install \
    && python3 setup.py compile_catalog -d hades/portal/translations \
    && python3 setup.py clean
ENTRYPOINT ["/usr/local/bin/hades"]
