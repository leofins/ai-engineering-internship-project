import "dotenv/config";
import express from "express";
import { createServer, request as httpRequest } from "http";
import net from "net";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { registerOAuthRoutes } from "./oauth";
import { appRouter } from "../routers";
import { createContext } from "./context";
import { serveStatic, setupVite } from "./vite";

// Proxy para o backend Python (FastAPI + RAG)
const PYTHON_BACKEND = process.env.PYTHON_API_URL ?? "http://127.0.0.1:8000";

function createPythonProxy(app: express.Application) {
  const PYTHON_ROUTES = ["/api/chat", "/api/upload", "/api/search", "/api/documents", "/health"];
  const url = new URL(PYTHON_BACKEND);

  app.use(PYTHON_ROUTES, (req, res) => {
    const options = {
      hostname: url.hostname,
      port: Number(url.port) || 8000,
      path: req.originalUrl,
      method: req.method,
      headers: { ...req.headers, host: `${url.hostname}:${url.port || 8000}` },
    };

    const proxy = httpRequest(options, (proxyRes) => {
      res.writeHead(proxyRes.statusCode ?? 502, proxyRes.headers);
      proxyRes.pipe(res);
    });

    proxy.on("error", () => {
      res.status(502).json({ error: "Python backend indisponível. Está rodando na porta 8000?" });
    });

    req.pipe(proxy);
  });
}

function isPortAvailable(port: number): Promise<boolean> {
  return new Promise(resolve => {
    const server = net.createServer();
    server.listen(port, () => {
      server.close(() => resolve(true));
    });
    server.on("error", () => resolve(false));
  });
}

async function findAvailablePort(startPort: number = 3000): Promise<number> {
  for (let port = startPort; port < startPort + 20; port++) {
    if (await isPortAvailable(port)) {
      return port;
    }
  }
  throw new Error(`No available port found starting from ${startPort}`);
}

async function startServer() {
  const app = express();
  const server = createServer(app);
  // Configure body parser with larger size limit for file uploads
  app.use(express.json({ limit: "50mb" }));
  app.use(express.urlencoded({ limit: "50mb", extended: true }));
  // Proxy para Python backend (RAG)
  createPythonProxy(app);
  // OAuth callback under /api/oauth/callback
  registerOAuthRoutes(app);
  // tRPC API
  app.use(
    "/api/trpc",
    createExpressMiddleware({
      router: appRouter,
      createContext,
    })
  );
  // development mode uses Vite, production mode uses static files
  if (process.env.NODE_ENV === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  const preferredPort = parseInt(process.env.PORT || "3000");
  const port = await findAvailablePort(preferredPort);

  if (port !== preferredPort) {
    console.log(`Port ${preferredPort} is busy, using port ${port} instead`);
  }

  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}/`);
  });
}

startServer().catch(console.error);
