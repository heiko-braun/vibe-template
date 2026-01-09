// PM2 ecosystem config for vibe-template
// Save this file as: template.ecosystem.config.cjs
// Location: root of vibe-template repository

module.exports = {
  apps: [{
    name: "nuxt-frontend",
    script: "npm",
    args: "run dev -- --host 0.0.0.0 --port 3000",
    cwd: "/tmp/project/frontend",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "1G",
    env: {
      NODE_ENV: "development"
    }
  }, {
    name: "fastapi-backend",
    script: "uv",
    args: "run uvicorn main:app --host 0.0.0.0 --port 5000 --reload",
    cwd: "/tmp/project/backend",
    interpreter: "none", // Don't use Node.js interpreter for Python
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "512M",
    env: {
      PYTHONUNBUFFERED: "1" // Ensure Python output isn't buffered
    }
  }]
};

