# Semantic Product Search

An intelligent AI-powered product recommendation system that uses semantic search and natural language processing to help users find products through conversational queries. Instead of traditional keyword matching, this application understands the meaning and intent behind user requests, delivering more relevant and contextual product recommendations.

## 🚀 Features

- **Natural Language Search**: Chat-based interface for intuitive product discovery
- **Semantic Understanding**: Powered by DistilBERT embeddings for intelligent matching
- **Fast Similarity Search**: FAISS-powered vector search for instant results
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Real-time Recommendations**: Get instant product suggestions with similarity scores

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **ML/AI**: Hugging Face Transformers (DistilBERT), FAISS
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas, NumPy

## 📋 Prerequisites

- Python 3.8+
- pip

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/semantic-product-search.git
cd semantic-product-search
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

1. Prepare your product data in CSV format with columns: `product_id`, `name`, `description`, `price`, `category`, `image_url`

2. Place your CSV file in the `data/` directory (or update the path in `app.py`)

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5001`

5. Start searching! Try queries like:
   - "I need running shoes"
   - "Show me electronics under $100"
   - "Looking for a gift for my friend"

## 📁 Project Structure

```
semantic-product-search/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── data/                  # Product data directory
│   └── sample_products.csv
├── utils/                  # Utility modules
│   ├── data_pipeline.py   # Data loading and preprocessing
│   ├── model.py           # Embedding generation
│   └── recommendation.py  # FAISS index and recommendations
├── templates/             # HTML templates
│   └── index.html
├── static/               # Static files
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── README.md
```

## 🔍 How It Works

1. **Embedding Generation**: Product descriptions are converted to dense vector representations using DistilBERT
2. **Index Building**: FAISS creates an efficient similarity search index
3. **Query Processing**: User queries are embedded and compared against product embeddings
4. **Ranking**: Results are ranked by semantic similarity and returned with scores

## 🎨 Features in Detail

- **Semantic Search**: Understands context and meaning, not just keywords
- **Similarity Scoring**: See how well products match your query
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Error Handling**: Graceful error handling with user-friendly messages
- **Health Check**: Built-in health endpoint for monitoring

## 📝 API Endpoints

- `GET /` - Main application interface
- `POST /chat` - Submit search queries and get recommendations
- `GET /health` - Health check endpoint

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for the Transformers library
- Facebook AI Research for FAISS
- Flask community for the excellent framework

---

