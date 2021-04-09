import json


def doc_id(pl):
    return pl[0]


def positions(pl):
    return pl[1]


class InvertedIndex:

    """
     Inverted Index for satisfying normal boolean queries.
     This class builds the index by storing the doc_ids of terms.
    """

    def __init__(self):
        self.dictionary = dict()
        self.index_file = "inverted_index.json"


    def add_term(self, term, doc):
        if term not in self.dictionary:
            self.dictionary[term] = []
        if doc not in self.dictionary[term]:
            self.dictionary[term].append(doc)


    def get_postings_list(self, term):
        if term in self.dictionary:
            return self.dictionary[term]

        return []

    def read_index(self):
        with open(self.index_file) as file:
            self.dictionary = json.load(file)

    def intersection(self, list_1, list_2):
        # returns common docs from two sorted postings list
        # by taking intersection between them to support
        # AND queries.

        i = 0
        j = 0
        result_docs = []

        while i < len(list_1) and j < len(list_2):
            if list_1[i] < list_2[j]:
                i = i + 1
            elif list_2[j] < list_1[i]:
                j = j + 1
            else:
                result_docs.append(list_1[i])
                i = i + 1
                j = j + 1

        return result_docs

    def union(self, list_1, list_2):

        """
          Joins two sorted postings list by taking union
          between them to support OR queries.
        """

        i = 0
        j = 0
        result_docs = []

        while i < len(list_1) and j < len(list_2):
            if list_1[i] < list_2[j]:
                result_docs.append(list_1[i])
                i = i + 1
            elif list_2[j] < list_1[i]:
                result_docs.append(list_2[j])
                j = j + 1
            else:
                result_docs.append(list_1[i])
                i = i + 1
                j = j + 1

        while i < len(list_1):
            result_docs.append(list_1[i])
            i += 1

        while j < len(list_2):
            result_docs.append(list_2[j])
            j += 1

        print("ss")
        return result_docs

    def invert(self, posting_list):
        all = range(1, 51)
        result = []
        i = 0
        j = 0
        while j < len(all) and i < len(posting_list):
            if posting_list[i] == all[j]:
                i += 1
                j += 1
            elif all[j] > posting_list[i]:
                i += 1
            else:
                result.append(all[j])
                j += 1

        while j < len(all):
            result.append(all[j])
            j += 1

        return result

    def write_index_to_disk(self):
        with open(self.index_file, "w") as write_file:
            json.dump(self.dictionary, write_file)


class PositionalInvertedIndex(InvertedIndex):

    """
     Positional Inverted Index for satisfying proximity queries.
     Inherits the InvertedIndex class. This class builds the index by storing
     the doc_ids of terms along with their file positions in the positing lists.

    """
    def __init__(self):
        super().__init__()
        self.index_file = "positional_index.json"

    def add_term(self, term, doc_id, position):
        if term not in self.dictionary:
            self.dictionary[term] = []

        exists = False

        for elem in self.dictionary[term]:
            if elem[0] == doc_id:
                exists = True
                break

        if not exists:
            self.dictionary[term].append([doc_id, []])

        self.dictionary[term][-1][1].append(position)

    def positional_intersect(self, list_1, list_2, k):
        i = 0
        j = 0
        result = []

        while i < len(list_1) and j < len(list_2):
            found = 0
            if doc_id(list_1[i]) == doc_id(list_2[j]):
                p1 = 0
                p2 = 0
                positions_1 = positions(list_1[i])
                positions_2 = positions(list_2[j])

                while p1 < len(positions_1):
                    while p2 < len(positions_2):
                        if abs(positions_1[p1] - positions_2[p2]) <= k:
                            result.append(doc_id(list_1[i]))
                            found = 1
                            break
                        elif positions_2[p2] > positions_1[p1]:
                            break
                        p2 += 1

                    if found == 1:
                        break
                    p1 += 1

                i += 1
                j += 1

            elif doc_id(list_1[i]) < doc_id(list_2[j]):
                i += 1

            else:
                j += 1

        return result
