def similarity_color(sim):
    if sim >= 80:
        return "red"
    elif sim >= 60:
        return "orange"
    else:
        return "green"

def overall_color(percent):
    if percent >= 50:
        return "red"
    elif percent >= 30:
        return "orange"
    else:
        return "green"
