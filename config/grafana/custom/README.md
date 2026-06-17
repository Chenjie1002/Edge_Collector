# Grafana Custom Font

Replace `grafana-custom.ttf` with another `.ttf` file and restart Grafana:

```bash
cd /opt/edge-mes-demo
docker-compose restart grafana
```

The stylesheet is injected into Grafana at container startup and applies the
font family `EdgeMESCustom` globally.
