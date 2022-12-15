"""
	Program to extract a bucketed sentences from a list of sentences
	with exclusions
"""
import sys, random, re

# Make sure we get the same results every time
random.seed(42)
buckets = {} # Length based buckets
include = {} 
exclude = []

# Require three command line arguments:
# python3 sample.py new_file.tsv old_file.tsv > exclusions.tsv
if len(sys.argv) == 3:
	# Create list of sentences that have already been checked
	# and determined as invalid
	for line in open(sys.argv[2]).read().split('\n'):
		if line.strip() == '':
			continue
		(k, v) = line.split('\t')
		exclude.append(v)

	# Create list of sentences in a bucket that have not been checked 
	# and not excluded as invalid
	for line in open(sys.argv[1]).read().split('\n'):
		if line.strip() == '':
			continue
		(k, v) = line.split('\t')
		if v in exclude:
			continue
		k = int(k)
		if k not in include:
			include[k] = []
		include[k].append(v)

# For each sentence in standard input
for line in sys.stdin:
	bucket = line.count(' ') + 1 # Assign to a bucket based on number of spaces
	sentence = line.strip().strip('"') # Remove leading and trailing spaces and double quotes

	# If our sentence is empty, skip it
	if len(sentence) == 0:
 		continue

	# If the sentence has no capital letters, skip it 
	if sentence[0] == sentence[0].lower():
		continue

	# Calculate the number of capital letters
	n_caps = len(re.findall('[A-Z]', sentence))

	# If we have more than two capital letters or if 
	# we have 2 and the bucket size is 2, skip it
	if n_caps > 2 or n_caps == 2 and bucket == 2:
		continue

	# If we already reviewed and excluded the sentence, 
	# skip it
	if sentence in exclude:
		continue

	# If we haven't seen a bucket of this size already:
	if bucket not in buckets:
		buckets[bucket] = []

	# Add the sentence to the current bucket
	buckets[bucket].append(sentence)

n_buckets = 10 # The number of sentence buckets (by length)
for bucket in range(1, n_buckets+1):
	# Remove duplicates

	buckets[bucket] = list(set(buckets[bucket]))
	per_bucket = 1200//n_buckets # This is the max number of sentences per bucket 

	print(bucket, len(buckets[bucket]), file=sys.stderr)

	# Check if a bucket is already full
	if bucket in include:
		for sentence in include[bucket]:
			print('%d\t%s' % (bucket, sentence))
		per_bucket = per_bucket - len(include[bucket])
		if len(include[bucket]) == 100: # The bucket is full (there are 100 sentences), so skip this bucket
			continue

	# If what we have is more than the max, set the max to what we have
	# TODO: Remember, why do we do this?
	if per_bucket > len(buckets[bucket]):
		per_bucket = len(buckets[bucket])

	# Randomly sample from the bucket
	sample = random.sample(buckets[bucket], per_bucket)

	# Debugging output
	if bucket in include:
		print(bucket, '|', len(include[bucket]),'|',per_bucket,'|', sample[0:3], file=sys.stderr)
	else:
		print(bucket, '|', 0,'|',per_bucket,'|', sample[0:3], file=sys.stderr)

	# For each of the randomly sampled sentences from the bucket
	for sentence in sample:
		# If we have not already checked it, add them with an
		# asterisk, so they can be checked
		if bucket in include:
			print('*%d\t%s' % (bucket, sentence))
		else:
		# If we have already checked it, then add it as is, 
		# does not need to be rechecked
			print('%d\t%s' % (bucket, sentence))
