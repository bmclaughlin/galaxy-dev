# Stage 1: Build galaxy-pulp from openapi spec
FROM openapitools/openapi-generator-cli AS galaxy-pulp

COPY galaxy-api/bindings/openapi.yaml /local/openapi.yaml
RUN docker-entrypoint.sh generate \
    -i /local/openapi.yaml \
    -g python \
    -o /local/galaxy-pulp \
    --skip-validate-spec \
    --additional-properties=packageName=galaxy_pulp,projectName=galaxy-pulp

# Stage 2: Build galaxy image
FROM centos:7

ENV PYTHONUNBUFFERED=1 \
    LANG=en_US.UTF-8 \
    GALAXY_CODE=/code \
    GALAXY_VENV=/venv \
    DJANGO_SETTINGS_MODULE=galaxy_api.settings

RUN yum -y install epel-release \
    && yum -y install \
        git \
        python36 \
        python36-devel \
    && yum -y clean all


COPY galaxy-api/Pipfile \
    galaxy-api/Pipfile.lock \
    /tmp/galaxy-api/

RUN python3.6 -m venv "${GALAXY_VENV}" \
    && source "${GALAXY_VENV}/bin/activate" \
    && pip --no-cache-dir install -U \
        'pip<19.0' \
        wheel \
        pipenv \
    && cd /tmp/galaxy-api \
    && PIPENV_VERBOSITY=-1 pipenv install --ignore-pipfile

COPY --from=galaxy-pulp /local/galaxy-pulp /tmp/galaxy-pulp
RUN source "${GALAXY_VENV}/bin/activate" \
    && pip install /tmp/galaxy-pulp

WORKDIR /code/

ENV PATH="/venv/bin:$PATH"

COPY docker/galaxy-api/entrypoint.sh /entrypoint
ENTRYPOINT [ "/entrypoint" ]
CMD [ "run" ]
