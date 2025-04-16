from flask import Flask, jsonify
from flask_cors import CORS
import nbformat

app = Flask(__name__)
CORS(app)  # Enables CORS for frontend requests

def extract_outputs(notebook_path):
    """Extracts output from a Jupyter Notebook (.ipynb) file and formats it properly."""
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        outputs = []
        for cell in notebook.cells:
            if cell.cell_type == "code":
                for output in cell.get("outputs", []):
                    if "text" in output:
                        text_output = output["text"]
                        outputs.append(text_output.strip())  # Preserve formatting
        
        return outputs

    except Exception as e:
        return [f"Error reading notebook: {str(e)}"]

@app.route('/get-notebook-output', methods=['GET'])
def get_notebook_output():
    """API endpoint to return formatted notebook outputs in JSON format."""
    notebook_path = "KubeAI2.ipynb"  # Ensure the correct notebook path
    outputs = extract_outputs(notebook_path)
    
    # Returning formatted JSON response
    response = {
        "outputs": outputs
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Runs server on port 5000
