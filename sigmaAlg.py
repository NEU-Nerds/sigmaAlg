import util
import multiprocessing as mp
import time
import os

BATCH_SIZE = 50000
MAX_SIGMA = 20
PROCESSES = 1

def main():
	# print('hi')
	evens = set([(1,)])
	try:
		os.mkdir("./evens")
	except:
		pass

	for s in range(2, MAX_SIGMA + 1):
		t1 = time.time()
		pHandler = ProccesHandler(evens, PROCESSES)
		for b in util.sigmaBatches(s, BATCH_SIZE):
			pHandler.run(b)
		newEvens = pHandler.getEvens()
		evens.update(newEvens)
		print(f"sigma: {s} \tevens: {len(evens)} in {time.time() - t1}s" )
		util.store(evens, f"./evens/evens_{s}.dat")
		# print(f"newEvens: {newEvens}")
		pHandler.terminate()
	# print(f"evens: {evens}")


#load up new processes with evens set
#gen batches of nodes to check and pass them in
#read the output queue

def nodesLoop(evens, evensQ, nodesQ):
	while True:
		nodes = nodesQ.get()
		newEvens = set()
		for node in nodes:
			# print(f"checking {node}")
			if isEven(evens, node):
				# print(f"is even")
				newEvens.add(node)
		print("putting new evens")
		evensQ.put(newEvens)

		nodesQ.task_done()


def isEven(evens, node):
	# print(f"isEven evens: {evens}")
	for child in util.getChildren(node):
		#if there is an even child
		if child in evens:
			return False
	#no even child so this is even
	return True

class ProccesHandler:
	nodesQ = None
	evensQ = None

	def __init__(self, evens, workers=6):
		self.nodesQ = mp.JoinableQueue()
		self.evensQ = mp.JoinableQueue()
		#states processes
		self.processes = [mp.Process(target=nodesLoop, args=(evens, self.evensQ, self.nodesQ), daemon=True) for i in range(workers)]

		for p in self.processes:
			p.start()

	def run(self, item):
		self.nodesQ.put(item)

	def getEvens(self):
		t = time.time()
		self.nodesQ.join()
		print(f"Waited {time.time()-t}s for queue to empty")
		newEvens = set()
		# print(f"Size: {self.evensQ.qsize()}")
		c = 0
		# running
		while True:
			try:
				e = self.evensQ.get(True, 0.01)
			except:
				break
			newEvens.update(e)
			c += 1
		# while not self.evensQ.empty():
		# 	c += 1
		# 	e = self.evensQ.get()
		# 	newEvens.update(e)
		if c == 0:
			print("\nCOUNT WAS 0\n")
		return newEvens

	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't
		#self.queue.join()
		for p in self.processes:
			p.terminate()


if __name__ == '__main__':
	main()
