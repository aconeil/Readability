import sys, random

random.seed(42)
buckets = {}

for line in sys.stdin:
	bucket = line.count(' ') + 1
	sentence = line.strip().strip('"')

	if len(sentence) == 0:
		continue

	if sentence[0] == sentence[0].lower():
		continue

	if bucket not in buckets:
		buckets[bucket] = []

	buckets[bucket].append(sentence)

remaining = 0
n_buckets = 10 
for bucket in range(1, 10):
	buckets[bucket] = list(set(buckets[bucket]))
	per_bucket = 1200//10
	print(bucket, len(buckets[bucket]), file=sys.stderr)
	
	if per_bucket > len(buckets[bucket]):
		per_bucket = len(buckets[bucket])

	sample = random.sample(buckets[bucket], per_bucket)

	print(bucket, per_bucket, sample[0:3], file=sys.stderr)
	for sentence in sample:
		print('%d\t%s' % (bucket, sentence))
