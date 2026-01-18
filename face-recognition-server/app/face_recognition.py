from deepface import DeepFace
from typing import List, Optional, Tuple
import numpy as np


def init_model():
    """Pre-load ArcFace model at startup"""
    try:
        # Force model download and initialization
        DeepFace.build_model("ArcFace")
        print("✓ ArcFace model initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize ArcFace model: {e}")
        raise


def get_embedding(image_path: str) -> List[float]:
    """
    Extract face embedding with quality checks.
    Raises ValueError if quality issues detected.
    """
    try:
        result = DeepFace.represent(
            img_path=image_path,
            model_name="ArcFace",
            detector_backend="retinaface",
            enforce_detection=True,
            align=True
        )

        # DeepFace returns list of dicts for each face
        if not result or len(result) == 0:
            raise ValueError("No face detected")

        if len(result) > 1:
            raise ValueError("Multiple faces detected. Please ensure only one face is visible.")

        embedding = result[0]["embedding"]

        # Quality check: embedding should be 512-dimensional for ArcFace
        if len(embedding) != 512:
            raise ValueError("Invalid embedding dimension")

        return embedding

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Embedding extraction failed: {str(e)}")


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings"""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    return float(dot_product / (norm1 * norm2))


def find_matching_user(
    new_embedding: List[float],
    all_users: List[Tuple[int, str, List[float]]],
    threshold: float = 0.55
) -> Optional[Tuple[int, str, float]]:
    """
    Check if new embedding matches any existing user.

    Args:
        new_embedding: Embedding to check
        all_users: List of (user_id, email, embedding) tuples
        threshold: Similarity threshold (0.55 for ArcFace)

    Returns:
        (user_id, email, similarity) if match found, None otherwise
    """
    for user_id, email, stored_embedding in all_users:
        similarity = cosine_similarity(new_embedding, stored_embedding)
        if similarity >= threshold:
            return (user_id, email, similarity)

    return None
