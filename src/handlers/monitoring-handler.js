import { Context } from 'hono';
import { Prometheus } from 'hono-prometheus';

const { KERNEL_VERSION, STARTUP_TIME } = Prometheus.Metrics;

export const handleMonitoring = async (c: Context) => {
    const metrics = Prometheus.getMetrics();
    return c.text(metrics);
};

export const registerMonitoring = (app) => {
    KERNEL_VERSION.labels('1.0.0').set(1);
    STARTUP_TIME.set(Date.now());

    app.use('/metrics', handleMonitoring);
    app.get('/healthz', (c) => c.text('OK'));
}
