class VectorAnalyzer:
    def __init__(self, vector_manager):
        self.vector_manager = vector_manager

    def find_most_similar(self, key, candidates):
        """Найти наиболее похожий вектор из списка кандидатов."""
        similarities = {
            candidate: self.vector_manager.calculate_similarity(key, candidate)
            for candidate in candidates
        }
        return max(similarities, key=similarities.get, default=None)
