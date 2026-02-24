# Configuration Files

This directory contains configuration files for the project.

## Files

| File | Purpose |
|------|---------|
| `settings.example.json` | Example application settings (copy to `settings.json`) |

## Usage

1. Copy example files removing `.example` suffix
2. Update values for your environment
3. Never commit files with real credentials

## Environment-Specific Configs

Create environment-specific files as needed:
- `settings.development.json`
- `settings.staging.json`
- `settings.production.json`

## Security

- All sensitive values should use environment variables: `${VAR_NAME}`
- Never commit real passwords, API keys, or secrets
- Add actual config files to `.gitignore`
