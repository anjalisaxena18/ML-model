from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity

def compute_cosine_similarity(embedding1, embedding2):
    """Computes cosine similarity between two embeddings."""
    return cosine_similarity([embedding1], [embedding2])[0][0]

def compute_similarity_report(processed_data):
    """Generates a similarity report for processed image data."""
    results = []
    flagged_images = []
    image_paths = list(processed_data.keys())

    for combo in combinations(image_paths, 3):
        img1, img2, img3 = combo
        emb1, emb2, emb3 = [processed_data[img]['embedding'] for img in combo]
        sim12, sim13, sim23 = (
            compute_cosine_similarity(emb1, emb2),
            compute_cosine_similarity(emb1, emb3),
            compute_cosine_similarity(emb2, emb3),
        )

        if sim12 == 1.0 and sim13 == 1.0 and sim23 == 1.0:
            flagged_images.append(combo)

        results.append({
            "images": combo,
            "similarities": {
                "img1-img2": sim12,
                "img1-img3": sim13,
                "img2-img3": sim23
            }
        })

    return {"results": results, "flagged_images": flagged_images}
