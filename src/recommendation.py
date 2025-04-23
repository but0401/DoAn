from collections import defaultdict

def generate_recommendations(frequent_itemsets, min_confidence=0.5):
    """Generate recommendations from frequent itemsets"""
    recommendations = []
    
    # Convert frozensets to lists for easier processing
    itemsets = [(list(itemset), count) for itemset, count in frequent_itemsets.items()]
    
    # Sort by count (descending)
    itemsets.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 10 itemsets as recommendations
    return itemsets[:10]

def generate_recommendations_from_sequences(sequences, target_item=None):
    """Generate product recommendations based on a target item"""
    recommendations = defaultdict(float)
    
    if target_item is None:
        # If no target item, return the top 20 items from frequent sequences
        for seq, support in sequences:
            if len(seq) == 1:
                recommendations[seq[0]] = max(recommendations[seq[0]], support)
        
        # Sort by support (descending)
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return sorted_recs[:20]
    
    # If target item is specified, find sequences containing the target item
    for seq, support in sequences:
        if target_item in seq:
            # Find position of target item in sequence
            pos = seq.index(target_item)
            
            # Get items that appear after the target item
            for i in range(pos+1, len(seq)):
                next_item = seq[i]
                if next_item != target_item:  # Don't recommend the same item
                    recommendations[next_item] = max(recommendations[next_item], support)
    
    # Sort by support (descending)
    sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    return sorted_recs[:20]  # Return top 20 recommendations