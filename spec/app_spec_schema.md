# Universal App Spec Schema

## Overview
This schema defines how any application (frontend/backend/fullstack) should be described in a standard format for RL management.

## Required Fields

### Basic Info
- `name` (string): Application name
- `type` (enum): "frontend" | "backend" | "fullstack"
- `version` (string): Current version

### Build & Deploy
- `build_command` (string): Command to build the app
- `start_command` (string): Command to start the app
- `install_command` (string): Command to install dependencies

### Health & Monitoring
- `health_endpoint` (string): URL endpoint to check app health
- `log_location` (string): Path to application logs
- `port` (number): Default port the app runs on

### Environments
- `envs` (array): List of environments
  - `name` (string): Environment name (dev/stage/prod)
  - `url` (string): Environment URL
  - `config_file` (string): Environment-specific config

### Error Patterns
- `error_patterns` (array): Important error patterns to watch
  - `pattern` (string): Regex pattern to match
  - `severity` (enum): "low" | "medium" | "high" | "critical"
  - `description` (string): What this error means

### Actions
- `available_actions` (array): Actions RL can take
  - `name` (string): Action name
  - `command` (string): Command to execute
  - `risk_level` (enum): "safe" | "medium" | "high"

## Optional Fields
- `dependencies` (array): List of dependency files (package.json, requirements.txt, etc.)
- `docker_config` (object): Docker-related configuration
- `metrics_endpoints` (array): Additional monitoring endpoints