# Configuration Kubernetes - Stack de Logging

Ce dossier contient les configurations Kubernetes pour:

## 📁 Structure
- `promtail/` - Agent de collecte de logs
- `loki/` - Système de stockage de logs
- `grafana/` - Dashboard de visualisation
- `flask-app/` - Application exemple Flask
- `coredns/` - Configuration DNS

## 🚀 Déploiement
Déployer dans l'ordre:
1. `loki/`
2. `promtail/`
3. `grafana/`
4. `flask-app/`
5. `coredns/`

## 📋 Pré-requis
- Kubernetes cluster
- kubectl configuré
- Helm (pour certaines configurations)

## 🔧 Notes
Les configurations sont pour un environnement de développement.
Adapter pour la production.

