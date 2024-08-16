import numpy as np

class SolomonoffTreeNode:
    def __init__(self, data):
        self.data = data
        self.mean = np.mean(data)
        self.variance = np.var(data)
        self.left = None
        self.right = None

def build_solomonoff_tree(data, depth=0, max_depth=10):
    if len(data) < 2 or depth >= max_depth:
        return SolomonoffTreeNode(data)

    node = SolomonoffTreeNode(data)
    mid = len(data) // 2
    node.left = build_solomonoff_tree(data[:mid], depth+1, max_depth)
    node.right = build_solomonoff_tree(data[mid:], depth+1, max_depth)
    return node

def predict_next(tree, sequence):
    node = tree
    while node.left and node.right:
        if len(sequence) % 2 == 0:
            node = node.left
        else:
            node = node.right
    return node.mean, node.variance

# Example usage
data = np.random.normal(0, 1, 1000)  # Example data
root = build_solomonoff_tree(data)

# Predict next value
test_sequence = [0.1, -0.2, 0.3]
predicted_mean, predicted_variance = predict_next(root, test_sequence)
print(f"Predicted mean: {predicted_mean}, Predicted variance: {predicted_variance}")
