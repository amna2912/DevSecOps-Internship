FROM grafana/promtail:latest


COPY promtail-config.yaml /etc/promtail/config.yml

CMD ["-config.file=/etc/promtail/config.yml"]
