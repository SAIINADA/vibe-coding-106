from highlight import similarity_color

def explain_source(file, page, similarity):
    return {
        "file": file,
        "page": page,
        "similarity": similarity,
        "color": similarity_color(similarity)
    }
