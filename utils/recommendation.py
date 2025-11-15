# utils/recommendation.py
import numpy as np
import faiss
from utils.model import get_embedding

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)  # L2 similarity search
    index.add(embeddings)
    return index

def get_recommendations(query, index, df, k=6, threshold=None):
    """
    Get product recommendations based on semantic similarity.
    
    Args:
        query: User's search query
        index: FAISS index with product embeddings
        df: DataFrame with product data
        k: Number of recommendations to return
        threshold: Optional distance threshold (auto-calculated if None)
    
    Returns:
        List of recommended products as dictionaries
    """
    query_embedding = get_embedding(query)
    query_embedding = np.array([query_embedding]).astype('float32')
    
    # Search for more candidates to filter
    search_k = min(k * 2, len(df))
    distances, indices = index.search(query_embedding, search_k)
    
    # Auto-calculate threshold based on distance distribution if not provided
    if threshold is None:
        # Use median distance as threshold, but ensure we get at least k results
        median_dist = np.median(distances[0])
        threshold = min(median_dist * 1.5, distances[0][k-1] if len(distances[0]) >= k else float('inf'))
    
    # Filter and rank results
    filtered_recs = []
    seen_indices = set()
    
    for i, idx in enumerate(indices[0]):
        if idx in seen_indices:
            continue
        if distances[0][i] <= threshold or len(filtered_recs) < k:
            rec = df.iloc[idx].to_dict()
            rec['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity
            filtered_recs.append(rec)
            seen_indices.add(idx)
        if len(filtered_recs) >= k:
            break
    
    # Sort by similarity score (highest first)
    filtered_recs.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
    
    return filtered_recs[:k]
