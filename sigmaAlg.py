import util
import multiprocessing as mp
import time

BATCH_SIZE = 50000
MAX_SIGMA = 19
PROCESSES = 6

def main():
	# print('hi')
	evens = set([(1,)])

	for s in range(2, MAX_SIGMA + 1):
		t1 = time.time()
		pHandler = ProccesHandler(evens, PROCESSES)
		for b in util.sigmaBatches(s, BATCH_SIZE):
			pHandler.run(b)
		newEvens = pHandler.getEvens()
		evens.update(newEvens)
		print(f"sigma: {s} \tevens: {len(newEvens)} in {time.time() - t1}s" )
		# print(f"newEvens: {newEvens}")
		pHandler.terminate()
	print(f"evens: {evens}")


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
		while not self.evensQ.empty():
			e = self.evensQ.get()
			newEvens.update(e)
		return newEvens

	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't
		#self.queue.join()
		for p in self.processes:
			p.terminate()


if __name__ == '__main__':
	main()
