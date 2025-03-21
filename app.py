from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    if request.method == 'POST':
        # Get the GitHub webhook payload
        payload = request.get_json()
        
        # Event type (should be 'push')
        event = request.headers.get('X-GitHub-Event')
        
        if event != 'push':
            return jsonify({'status': 'not a push event'}), 400
        
        # Get the branch name from the payload
        ref = payload.get('ref', '')  # e.g., 'refs/heads/feature-branch'
        
        if ref:
            branch_name = ref.split('/')[-1]  # Extract the branch name after 'refs/heads/'
            return jsonify({'status': 'success', 'branch': branch_name}), 200
        
        else:
            return jsonify({'status': 'error', 'message': 'Branch info not found in payload'}), 400
    else:
        return 'Invalid Method', 405


if __name__ == '__main__':
    app.run(debug=True, host='sapqlaunch.wal-mart.com', port=5000)