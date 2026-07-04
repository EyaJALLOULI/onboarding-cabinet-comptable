# Onboarding Cabinet Comptable

Automatisation n8n pour l'onboarding client d'un cabinet comptable : réception des documents par email, vérification antivirus, extraction de texte (OCR), et classement automatique dans Google Drive.

## Fonctionnement général

1. Un email avec pièce jointe arrive dans la boîte du cabinet
2. Le fichier est scanné par **ClamAV** avant tout traitement
3. Si le fichier est sain, il passe par le service **OCR** pour extraire le texte (utile pour les PDF scannés ou images)
4. Le workflow n8n classe et archive automatiquement le document dans le bon dossier client (Google Drive)
5. Des notifications sont envoyées (email) en fonction du résultat

## Services

### 🔍 OCR — port `9001`
Récupère une pièce jointe Gmail via son `messageId` et `attachmentId`, puis en extrait le texte avec Tesseract (supporte les images et les PDF multi-pages).

**Endpoint** : `POST /ocr`
```json
{
  "messageId": "...",
  "attachmentId": "...",
  "userEmail": "me",
  "mimeType": "application/pdf"
}
```

### 🛡️ ClamAV — port `9000`
Scanne un fichier envoyé en `POST` pour détecter d'éventuels malwares avant traitement.

**Endpoint** : `POST /scan` (form-data, champ `file`)

Réponse type :
```json
{ "malware": false, "description": null }
```

## Installation

### Prérequis
- Docker et Docker Compose installés
- Une instance n8n (locale ou cloud) pour importer les workflows

### Lancer les services

```bash
docker-compose build
docker-compose up -d
```

Vérifier que tout tourne :
```bash
docker ps
```

### Import des workflows dans n8n

Dans l'interface n8n : **Workflows → Import from file**, puis sélectionner chaque fichier du dossier `workflows/` un par un (commencer par `main.json`).

## ⚠️ Sécurité

Ce dépôt contient des clés/identifiants en clair (compte Google partagé). À ne pas rendre public sans les avoir retirés au préalable.