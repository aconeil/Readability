with open("fi.tsv", "r") as f:
	sents=map(Sent,f)
class Sent:
	def __inti__(self, text, mu=100, sigma=100):
		self.text = text
		self.mu = mu
		self.sigma = sigma
class Sent:
	@property
	def i(self):
		return (self.mu - self.sigma,
		self.mu + self.sigma)
def w(s1, s2):
	l = min(s1.i[1], s2.i[1]) - max(s1.i[0], s2.i[0])
	L = max(s1.i[1], s2.i[1]) - min(s1.i[0], s2.i[0])
	return l/L*4*max(s1.sigma,s2.sigma)
pairs=[(sents[i], sents[j])
	for i in range(len(sents))
	for j in range(i+1, len(sents))]
best_pair = max(pairs, key=lambda p:w(*p))
