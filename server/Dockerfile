FROM python:3.9.7-slim
COPY server /
RUN python -m unittest tests/test_common.py
CMD ["/bin/sh"]
