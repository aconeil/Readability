import sys, random, re

random.seed(42)
buckets = {}
include = {}
exclude = []

if len(sys.argv) == 3:
	for line in open(sys.argv[2]).read().split('\n'):
		if line.strip() == '':
			continue
		(k, v) = line.split('\t')
		exclude.append(v)

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

for line in sys.stdin:
	bucket = line.count(' ') + 1
	sentence = line.strip().strip('"')

	if len(sentence) == 0:
		continue

	if sentence[0] == sentence[0].lower():
		continue

	n_caps = len(re.findall('[A-Z]', sentence))
	if n_caps > 2 or n_caps == 2 and bucket == 2:
		continue

	if sentence in exclude:
		continue

	if bucket not in buckets:
		buckets[bucket] = []

	buckets[bucket].append(sentence)

remaining = 0
n_buckets = 10 
for bucket in range(1, n_buckets+1):
	buckets[bucket] = list(set(buckets[bucket]))
	per_bucket = 1200//n_buckets
	print(bucket, len(buckets[bucket]), file=sys.stderr)

	if bucket in include:
		for sentence in include[bucket]:
			print('%d\t%s' % (bucket, sentence))
		per_bucket = per_bucket - len(include[bucket])
		if len(include[bucket]) == 100:
			continue
	
	if per_bucket > len(buckets[bucket]):
		per_bucket = len(buckets[bucket])

	sample = random.sample(buckets[bucket], per_bucket)

	print(bucket, '|', len(include[bucket]),'|',per_bucket,'|', sample[0:3], file=sys.stderr)
	for sentence in sample:
		if bucket in include:
			print('*%d\t%s' % (bucket, sentence))
		else:
			print('%d\t%s' % (bucket, sentence))
