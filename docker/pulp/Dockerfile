FROM centos:8

ENV LANG=en_US.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PULP_CODE=/code \
    PULP_VENV=/venv \
    PULP_SETTINGS=/etc/pulp/settings.py \
    DJANGO_SETTINGS_MODULE=pulpcore.app.settings \
    ANSIBLE_TEST_VENV=/venv_ansible_test \
    BUILDAH_ISOLATION=chroot


RUN mkdir -p /var/lib/shared/overlay-images /var/lib/shared/overlay-layers; \
       touch /var/lib/shared/overlay-images/images.lock; \
       touch /var/lib/shared/overlay-layers/layers.lock

COPY docker/pulp/storage.conf /etc/containers/storage.conf
COPY docker/pulp/rpm/* /tmp/

RUN sed -i -e 's|^#mount_program|mount_program|g' -e '/additionalimage.*/a "/var/lib/shared",' -e 's|^mountopt[[:space:]]*=.*$|mountopt = "nodev,fsync=0"|g' /etc/containers/storage.conf
RUN dnf -y install  /tmp/runc-1.0.0-67.rc10.el7_8.1.x86_64.rpm /tmp/buildah-1.11.6-8.el8.x86_64.rpm --exclude container-selinux
RUN useradd build; \
       dnf -y update; \
       dnf -y reinstall shadow-utils; \
       dnf -y install fuse-overlayfs; \
       rm -rf /var/cache /var/log/dnf* /var/log/yum.*

RUN dnf install -y \
        glibc-langpack-en \
        git-core \
        gcc \
        python3 \
        python3-devel \
        libpq \
        libpq-devel \
        sudo \
        openssl \
    && dnf -y clean all

RUN mkdir -p /var/run/pulp \
    /var/lib/pulp/tmp \
    "${ANSIBLE_TEST_VENV}"

COPY docker/pulp/constraints.txt /tmp/constraints.txt
COPY docker/pulp/requirements_ansible_test.txt /tmp/ansible_test/
COPY pulp_ansible/ "${PULP_CODE}/pulp_ansible"

RUN python3 -m venv "${ANSIBLE_TEST_VENV}" \
    && source "${ANSIBLE_TEST_VENV}/bin/activate" \
    && pip --no-cache-dir install -U \
        'pip>=20.0,<21.0' \
    && cd /tmp/ansible_test \
    && pip install \
        --no-cache-dir \
        --default-timeout 100 \
        -r requirements_ansible_test.txt \
    && chmod -R a+rwX "${ANSIBLE_TEST_VENV}"/lib64/python*

RUN python3 -m venv "${PULP_VENV}" \
    && source "${PULP_VENV}/bin/activate" \
    && pip install --no-cache-dir -U \
        'pip>=20.0,<21.0' \
    && pip --no-cache-dir install \
        pulp-container \
    && pip --no-cache-dir install \
        -c /tmp/constraints.txt \
        -e "${PULP_CODE}/pulp_ansible"

ENV PATH="${PULP_VENV}/bin:${PATH}"

COPY docker/pulp/settings.py /etc/pulp/settings.py
COPY docker/pulp/ansible.cfg /etc/ansible/ansible.cfg

RUN openssl ecparam -genkey -name prime256v1 -noout -out /tmp/private_key.pem \
    && openssl ec -in /tmp/private_key.pem -pubout -out /tmp/public_key.pem \
    && echo "TOKEN_SERVER = 'http://localhost:24816/token'" >> /etc/pulp/settings.py \
    && echo "TOKEN_SIGNATURE_ALGORITHM = 'E256'" >> /etc/pulp/settings.py \
    && echo "PUBLIC_KEY_PATH = '/tmp/public_key.pem'" >> /etc/pulp/settings.py \
    && echo "PRIVATE_KEY_PATH = '/tmp/private_key.pem'" >> /etc/pulp/settings.py

ENV PATH="/venv/bin:/usr/bin:$PATH"

COPY docker/pulp/entrypoint.sh /entrypoint


VOLUME /data/
WORKDIR /code/
ENTRYPOINT [ "/entrypoint" ]
