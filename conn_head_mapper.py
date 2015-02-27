import json

class ConnHeadMapper(object):

	DEFAULT_MAPPING_FILE = 'conn_head_mapping.json'
	def __init__(self):
		self.mapping = json.loads(open(ConnHeadMapper.DEFAULT_MAPPING_FILE).read())

	def map_raw_connective(self, raw_connective):
		head_connective = self.mapping[raw_connective]
		# find the index of the head connectives
		raw_connective_token_list = raw_connective.lower().split(' ')
		head_connective_token_list = head_connective.split(' ')
		start_point = 0
		indices = []
		for head_connective_token in head_connective_token_list:
			for i in range(start_point, len(raw_connective_token_list)):
				if head_connective_token == raw_connective_token_list[i]:
					indices.append(i)
					start_point = i+1
					break
		assert(len(head_connective_token_list) == len(indices))
		return head_connective, indices	

if __name__ == '__main__':
	chm = ConnHeadMapper()

	raw_connective = "29 years and 11 months to the day after"
	head_connective, indices = chm.map_raw_connective(raw_connective)
	assert(head_connective == "after")
	assert(indices == [8])

	raw_connective = "Largely as a result"
	head_connective, indices = chm.map_raw_connective(raw_connective)
	assert(head_connective == "as a result")
	assert(indices == [1, 2 ,3])
	
