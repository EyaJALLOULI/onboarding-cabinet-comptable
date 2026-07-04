from flask import Flask, request, jsonify
import subprocess, tempfile, os

app = Flask(__name__)
CLAMD = "clamscan"

@app.route('/scan', methods=['POST'])
def scan():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file'}), 400
    
    # delete=False + fermeture manuelle avant scan
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.tmp')
    try:
        file.save(tmp.name)
        tmp.close()  # ferme avant de lancer clamscan
        
        result = subprocess.run(
            [CLAMD, '--no-summary', tmp.name],
            capture_output=True, text=True
        )
    finally:
        try:
            os.unlink(tmp.name)  # supprime après scan
        except:
            pass
    
    infected = result.returncode == 1
    threat = None
    if infected:
        for line in result.stdout.splitlines():
            if 'FOUND' in line:
                threat = line.split(':')[1].strip().replace(' FOUND', '')
    
    return jsonify({
        'malware': infected,
        'description': threat
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)