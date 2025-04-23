from collections import defaultdict

class SPADEAlgorithm:
    def __init__(self, min_support=0.01):
        self.min_support = min_support
        self.frequent_sequences = []
        self.sequence_db = defaultdict(list)
        self.vertical_db = defaultdict(list)
        self.sequence_count = 0
        
    def preprocess_data(self, df):
        """
        Convert transactions to sequence database format
        """
        # Group by CustomerID and sort by InvoiceDate
        df_sorted = df.sort_values(by=['CustomerID', 'InvoiceDate'])
        
        # Create sequence database
        for customer_id, group in df_sorted.groupby('CustomerID'):
            sequence = []
            prev_invoice = None
            
            for _, row in group.iterrows():
                invoice = row['InvoiceNo']
                item = row['StockCode']
                
                # If new invoice, create new itemset
                if invoice != prev_invoice:
                    sequence.append([item])
                    prev_invoice = invoice
                else:
                    # Add item to current itemset if not already there
                    if item not in sequence[-1]:
                        sequence[-1].append(item)
            
            self.sequence_db[customer_id] = sequence
        
        self.sequence_count = len(self.sequence_db)
        
        # Create vertical database (id-lists)
        for seq_id, sequence in self.sequence_db.items():
            for pos, itemset in enumerate(sequence):
                for item in itemset:
                    self.vertical_db[item].append((seq_id, pos))
    
    def find_frequent_items(self):
        """Find frequent 1-sequences"""
        frequent_items = {}
        min_support_count = self.min_support * self.sequence_count
        
        for item, id_list in self.vertical_db.items():
            # Count unique sequences containing the item
            unique_seqs = len(set(seq_id for seq_id, _ in id_list))
            
            if unique_seqs >= min_support_count:
                frequent_items[item] = unique_seqs / self.sequence_count
                self.frequent_sequences.append(([item], unique_seqs / self.sequence_count))
        
        # Filter vertical database to keep only frequent items
        self.vertical_db = {item: id_list for item, id_list in self.vertical_db.items() 
                            if item in frequent_items}
        
        return frequent_items
    
    def id_list_join(self, id_list1, id_list2):
        """Join two id-lists to form a new sequence"""
        result = []
        
        # Convert first id-list to dictionary for faster lookup
        seq_pos_dict = defaultdict(list)
        for seq_id, pos in id_list1:
            seq_pos_dict[seq_id].append(pos)
        
        # Join with second id-list where positions are properly ordered
        for seq_id, pos2 in id_list2:
            if seq_id in seq_pos_dict:
                for pos1 in seq_pos_dict[seq_id]:
                    if pos1 < pos2:  # Ensure proper sequence ordering
                        result.append((seq_id, pos2))
                        break
        
        return result
    
    def generate_candidate_sequences(self, frequent_items, k):
        """Generate candidate k-sequences from frequent (k-1)-sequences"""
        candidates = {}
        
        # Get all (k-1)-sequences
        k_minus_1_sequences = [seq for seq, _ in self.frequent_sequences if len(seq) == k-1]
        
        # Generate k-sequences by joining (k-1)-sequences
        for i, seq1 in enumerate(k_minus_1_sequences):
            for j in range(i, len(k_minus_1_sequences)):
                seq2 = k_minus_1_sequences[j]
                
                # Check if prefixes match (all but last element)
                if seq1[:-1] == seq2[:-1]:
                    # Create new candidate sequence
                    new_seq = seq1 + [seq2[-1]]
                    
                    # Get id-lists for the last items of both sequences
                    id_list1 = self.vertical_db[seq1[-1]]
                    id_list2 = self.vertical_db[seq2[-1]]
                    
                    # Join id-lists
                    joined_id_list = self.id_list_join(id_list1, id_list2)
                    
                    # Calculate support
                    support = len(set(seq_id for seq_id, _ in joined_id_list)) / self.sequence_count
                    
                    # If support meets minimum threshold, add to candidates
                    if support >= self.min_support:
                        candidates[tuple(new_seq)] = joined_id_list
                        self.vertical_db[tuple(new_seq)] = joined_id_list
                        self.frequent_sequences.append((new_seq, support))
        
        return candidates
    
    def find_frequent_sequences(self):
        """Main method to find all frequent sequences"""
        # Find frequent 1-sequences
        frequent_items = self.find_frequent_items()
        
        k = 2
        # Continue until no more frequent sequences can be found
        while True:
            candidates = self.generate_candidate_sequences(frequent_items, k)
            if not candidates:
                break
            k += 1
        
        # Sort frequent sequences by support (descending)
        self.frequent_sequences.sort(key=lambda x: x[1], reverse=True)
        return self.frequent_sequences

# Legacy functions to maintain compatibility with existing code
def prepare_transactions(df):
    transactions = defaultdict(list)
    for _, row in df.iterrows():
        transactions[row['InvoiceNo']].append(row['StockCode'])
    return list(transactions.values())

def find_frequent_itemsets(transactions, minsup):
    # Count occurrences of each itemset
    itemsets = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            itemsets[frozenset([item])] += 1
    
    # Filter itemsets by minsup
    total_transactions = len(transactions)
    frequent_itemsets = {itemset: count for itemset, count in itemsets.items() if count / total_transactions >= minsup}
    
    return frequent_itemsets