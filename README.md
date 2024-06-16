# Arris DG860 Metrics Exporter

This project provides a Dockerized solution to obtain real-time downstream metrics, power levels, and SNR (Signal-to-Noise Ratio) from the Arris DG860 cable modem.

## Usage

1. **Build Docker Image:**
   ```bash
   docker build -t arris_DG860_exporter .
   ```

2. **Navigate to Docker Directory:**
   ```bash
   cd docker
   ```

3. **Start Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Access Grafana Dashboard:**
   Open your web browser and go to [http://localhost:3030](http://localhost:3030)

## Grafana Dashboard

Once the Docker containers are up and running, you can visualize the metrics using Grafana by accessing the provided localhost link.

## Notes

- Ensure your Docker environment is properly configured.
- Grafana should be configured to connect to the metrics endpoint exposed by the exporter.

## Credits

This project was created to facilitate monitoring of Arris DG860 cable modem metrics in real-time.
