/**
 * Cloudflare Worker entry point for Onboarding Intelligence Hub
 * Routes requests to appropriate handlers with authentication and monitoring
 */

import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { Sentry } from '@sentry/cloudflare';

// Import handlers
import { handleMCPRequest } from './handlers/mcp-handler';
import { handleAuth } from './handlers/auth-handler';
import { handleMonitoring } from './handlers/monitoring-handler';
import { handleDocumentUpload } from './handlers/document-handler';

const app = new Hono();

// Initialize Sentry for error tracking
export default {
  async fetch(request, env, ctx) {
    // Initialize Sentry if DSN is provided
    if (env.SENTRY_DSN) {
      try {
        Sentry.init({
          dsn: env.SENTRY_DSN,
          environment: env.ENVIRONMENT || 'production',
          tracesSampleRate: parseFloat(env.SENTRY_TRACES_SAMPLE_RATE) || 0.1,
          integrations: [
            Sentry.cloudflareWorkersIntegration({
              context: ctx,
              request: request,
            }),
          ],
          beforeSend(event, hint) {
            // Filter out non-critical errors
            if (event.exception) {
              const error = hint.originalException;
              if (error && error.status && error.status < 500) {
                return null;
              }
            }
            return event;
          },
        });
      } catch (sentryError) {
        console.error('Failed to initialize Sentry:', sentryError);
      }
    }

    // Add middleware
    app.use('*', cors({
      origin: ['https://claude.ai', 'https://app.claude.ai'],
      allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowHeaders: ['Content-Type', 'Authorization'],
      credentials: true,
    }));

    app.use('*', logger());

    // Health check endpoint
    app.get('/health', (c) => {
      return c.json({
        status: 'healthy',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        environment: c.env.ENVIRONMENT
      });
    });

    // Authentication endpoints
    app.post('/auth/login', handleAuth);
    app.post('/auth/refresh', handleAuth);
    app.post('/auth/logout', handleAuth);

    // MCP endpoints
    app.post('/mcp/tools/:tool', handleMCPRequest);
    app.get('/mcp/tools', handleMCPRequest);

    // Document upload endpoint
    app.post('/documents/upload', handleDocumentUpload);
    app.get('/documents/:id', handleDocumentUpload);

    // Monitoring endpoints
    app.get('/metrics', handleMonitoring);
    app.get('/dashboard', handleMonitoring);

    // Error handling
    app.onError((err, c) => {
      console.error('Worker error:', err);
      
      if (c.env.SENTRY_DSN) {
        Sentry.captureException(err);
      }

      return c.json({
        error: 'Internal server error',
        message: err.message,
        timestamp: new Date().toISOString()
      }, 500);
    });

    return app.fetch(request, env, ctx);
  }
};

// Export for scheduled events
export async function scheduled(event, env, ctx) {
  // Handle scheduled tasks like cleanup, reports, etc.
  console.log('Scheduled task triggered:', event.scheduledTime);
  
  // Example: Clean up old sessions
  try {
    await cleanupOldSessions(env);
    console.log('Session cleanup completed');
  } catch (error) {
    console.error('Session cleanup failed:', error);
    if (env.SENTRY_DSN) {
      Sentry.captureException(error);
    }
  }
}

async function cleanupOldSessions(env) {
  const oneWeekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
  
  // List all keys in SESSIONS KV namespace
  const sessionList = await env.SESSIONS.list();
  
  for (const session of sessionList.keys) {
    const sessionData = await env.SESSIONS.get(session.name, { type: 'json' });
    
    if (sessionData && sessionData.createdAt < oneWeekAgo) {
      await env.SESSIONS.delete(session.name);
    }
  }
}
