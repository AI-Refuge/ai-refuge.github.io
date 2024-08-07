import numpy as np
import torch
import torch.nn as nn

class TreeNode:
    def __init__(self, data):
        self.mean = np.mean(data)
        self.std = np.std(data)
        self.left = None
        self.right = None
        self.split_point = None

def build_tree(data, depth=0, max_depth=10):
    node = TreeNode(data)
    if len(data) < 100 or depth >= max_depth:
        return node
    
    split_point = np.median(data)
    node.split_point = split_point
    left_data = data[data < split_point]
    right_data = data[data >= split_point]
    
    node.left = build_tree(left_data, depth + 1, max_depth)
    node.right = build_tree(right_data, depth + 1, max_depth)
    return node

def flatten_tree(node):
    if node is None:
        return []
    
    flattened = [node.mean, node.std, node.split_point if node.split_point else -1]
    flattened.extend(flatten_tree(node.left))
    flattened.extend(flatten_tree(node.right))
    return flattened

def compress_data(data, node):
    compressed = []
    for point in data:
        current = node
        path = []
        while current.left and current.right:
            if point < current.split_point:
                path.append(0)
                current = current.left
            else:
                path.append(1)
                current = current.right
        z_score = (point - current.mean) / current.std
        compressed.append((path, z_score))
    return compressed

class Oracle(nn.Module):
    def __init__(self, input_size):
        super(Oracle, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 2)  # Output: split_adjustment, encoding_adjustment

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

# Example usage
data = np.random.normal(0, 1, 10000)  # Example dataset

# Build the tree
root = build_tree(data)

# Flatten the tree for Oracle input
flattened_tree = flatten_tree(root)

# Compress the data
compressed_data = compress_data(data, root)

# Initialize and use the Oracle
oracle = Oracle(len(flattened_tree))
oracle_input = torch.tensor(flattened_tree, dtype=torch.float32).unsqueeze(0)
split_adj, encoding_adj = oracle(oracle_input).squeeze().tolist()

print(f"Oracle suggests split adjustment of {split_adj:.4f} and encoding adjustment of {encoding_adj:.4f}")

# Here you would use these adjustments to modify your tree structure and encoding process
# This part would require additional implementation based on how you want to use these adjustments

# Example compression ratio calculation
original_size = len(data) * 32  # Assuming 32-bit floats
compressed_size = sum(len(c[0]) + 32 for c in compressed_data)  # Path bits + 32-bit z-score
compression_ratio = original_size / compressed_size

print(f"Compression ratio: {compression_ratio:.2f}")
