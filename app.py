# app.py
from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import logging

from utils.data_pipeline import load_product_data
from utils.model import get_embedding
from utils.recommendation import build_faiss_index, get_recommendations

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load data and compute embeddings on startup
try:
    logger.info("Loading product data...")
    data_path = os.path.join('data', 'sample_products.csv')
    df = load_product_data(data_path)
    
    logger.info("Generating embeddings for products...")
    # Generate embeddings for all product descriptions
    df['embedding'] = df['description'].apply(lambda x: get_embedding(x))
    product_embeddings = np.vstack(df['embedding'].values).astype('float32')
    
    # Build FAISS index for fast similarity search
    logger.info("Building FAISS index...")
    faiss_index = build_faiss_index(product_embeddings)
    logger.info(f"✅ Ready! Loaded {len(df)} products.")
except Exception as e:
    logger.error(f"Error during startup: {e}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400
            
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        logger.info(f"Processing query: {user_message}")
        
        # Get recommendations
        recommendations = get_recommendations(user_message, faiss_index, df, k=6)
        
        # Remove embeddings from the response
        for rec in recommendations:
            rec.pop('embedding', None)
        
        # Generate contextual response
        if recommendations:
            response_message = f"✨ I found {len(recommendations)} great products for you!"
        else:
            response_message = "🤔 I couldn't find exact matches, but here are some suggestions:"
            # Fallback: return top products
            recommendations = df.head(6).to_dict(orient='records')
            for rec in recommendations:
                rec.pop('embedding', None)
        
        return jsonify({
            "reply": response_message,
            "recommendations": recommendations
        })
        
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "products_loaded": len(df)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
    
