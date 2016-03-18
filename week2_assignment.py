"""
Created on Sun Feb 28 23:06:15 2016

@author: andrewscott
Student code for Word Wrangler game
"""

import urllib2
import math
#import codeskulptor
#import poc_wrangler_provided as provided
try:    
    import codeskulptor
    codeskulptor.set_timeout(40)
except ImportError as caught_e:
    print caught_e
try:
    import poc_wrangler_provided as provided
except ImportError as caught_e:
    print caught_e

DEBUG_RD = False
DEBUG_MS = False
DEBUG_GAS = False
DEBUG_LW = False
DEBUG_I = True
#Local wordfile
#WORDFILE = "assets_scrabble_words3.txt"
#codeskulptor wordfile
WORDFILE = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    if len(list1) <= 1:
        if DEBUG_RD:        
            print "base case, returning", list1
        return list1
    else:
        next_iteration = remove_duplicates(list1[:-1])
        if DEBUG_RD:        
            print "next_iteration", next_iteration
        if list1[-1] in next_iteration:
            return remove_duplicates(next_iteration)
        else:
            return remove_duplicates(next_iteration) + [list1[-1]]
    """
    #iterative, not recursive
    if len(list1) == 0:
        return list1
    new_list = []
    new_list.append(list1[0])
    for item in list1[1:]:
        if item != new_list[-1]:
            new_list.append(item)
    return new_list
    
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    
    #strategy: send whole of list1, all of list2 minus last position
    #check if last position of _sent_ amount of list2 is in list 1
    #return it if true
    if len(list2) < 1 or len(list1) < 1:
        return []
    else:
        next_iteration = intersect(list1, list2[:-1])
        print "next_iteration", next_iteration        
        if list2[-1] in list1:
            return next_iteration + [list2[-1]]
        else:
            return next_iteration
    """
    #iterative, not recursive
    intersect_list = []
    outer_list = []
    inner_list = []
    len_list1 = len(list1)
    len_list2 = len(list2)
    start_outer = 0
    start_inner = 0
    inner_start = 0
    if len_list1 <= len_list2:
        outer_list = list1
        inner_list = list2
    else:
        outer_list = list2
        inner_list = list1
    end_outer = len(outer_list)
    end_inner = len(inner_list)
    if DEBUG_I:
        print "end_inner", end_inner
        print "end_outer", end_outer
    """
    Method 2
    #Somehow worse efficiency than index(item)
    for item in outer_list:
        for dummy_idx in range(start_inner, end_inner):
            if item == inner_list[dummy_idx]:
                intersect_list.append(item)
                if DEBUG_I:
                    print "updating start_inner:",dummy_idx
                start_inner = dummy_idx
                
    #Method 1
    #Not terrible efficiency, not amazingly bad
    for item in outer_list:
        if item in inner_list:
            inner_start = inner_list.index(item)
            intersect_list.append(item)
            
    #Method 3 - am best
    for item in outer_list:
        if item in inner_list[start_inner:]:
            intersect_list.append(item)
            start_inner = inner_list.index(item)
            if DEBUG_I:
                print "updating start_inner:", start_inner           

    #Method 4, am try to use generator            
    for item in outer_list:
        for dummy_idx in gen_range(start_inner, end_inner):
            if item == inner_list[dummy_idx]:
                intersect_list.append(item)
                if DEBUG_I:
                    print "updating start_inner:",dummy_idx
                start_inner = dummy_idx
    
    #Method 5 - try to break on find
    for item in outer_list:
        for dummy_idx in range(start_inner, end_inner):
            if item == inner_list[dummy_idx]:
                intersect_list.append(item)
                if DEBUG_I:
                    print "updating start_inner:",dummy_idx
                start_inner = dummy_idx
                break           
    """
    #Method 6 - dict
    #outer_dict = {entry: entry for entry in outer_list}
    outer_dict = {}
    for entry in outer_list:
        outer_dict[entry] = entry
    for entry in inner_list:
        if entry in outer_dict:
            intersect_list.append(entry)
                
    return intersect_list

def gen_range(start, end):
    for index in range(start, end):
        yield index

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    merged = []
    if len(list1) < 1 or len(list2) <1:
        return list1 + list2
    else:
        ind_1 = 0
        ind_2 = 0
        while ind_1 < len(list1) and ind_2 < len(list2):
            #some appends to lists
            if list1[ind_1] < list2[ind_2]:
                merged.append(list1[ind_1])
                ind_1 += 1
            elif list2[ind_2] < list1[ind_1]:
                merged.append(list2[ind_2])
                ind_2 += 1
            elif list1[ind_1] == list2[ind_2]:
                merged.append(list1[ind_1])
                merged.append(list2[ind_2])
                ind_1 += 1
                ind_2 += 1
            #if reach end of one list, copy the remainder of the other
            if ind_1 >= len(list1) and ind_2 < len(list2):
                merged += list2[ind_2:]
                ind_2 = len(list2)
            elif ind_2 >= len(list2) and ind_1 < len(list1):
                merged += list1[ind_1:]
                ind_1 = len(list1)
    return merged
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    left = []
    right = []
    #merged = []
    if len(list1) <= 1:
        if DEBUG_MS:
            print "returning", list1
        return list1
    else:
        pivot = int(math.floor(len(list1)/2))
        if DEBUG_MS:
            print "pivot", pivot
        #left = merge_sort(list1[:pivot])
        #right = merge_sort(list1[pivot:])
        left = merge_sort(list1[:pivot])
        right = merge_sort(list1[pivot:])
        #return [min(merge_sort(list1[:pivot]))] + [max(merge_sort(list1[pivot:]))]
    if DEBUG_MS:
        print "return merge(", left, "," , right, ")"
    return merge(left, right)
    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if DEBUG_GAS:
        print "WORD", word
    if len(word) < 1:
        if DEBUG_GAS:
            print "BASE ZERO"
            print "len(word)", len(word)
            print "word", word
        return ['']
    if len(word) == 1:
        if DEBUG_GAS:
            print "BASE ONE"
            print "len(word)", len(word)
            print "word", word
        return ['', word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        permutations = []
        if DEBUG_GAS:
            print "rest_strings", rest_strings
            print first, rest
        for item in rest_strings:
            if DEBUG_GAS:
                print "rest_strings item", item
            for dummy_idx in range(len(item)+1):
                if DEBUG_GAS:
                    print "dummy_idx", dummy_idx
                    print "item", item
                permutations.append(str(item[:dummy_idx] + first + item[dummy_idx:]))
        for item in permutations:
            rest_strings.append(item)
        return rest_strings
        
            

# Function to load words from a file

def load_words(filename):
    #print filename
    #url = codeskulptor.file2url(filename)
    #netfile = urllib2.urlopen(url)
    netfile = urllib2.urlopen(filename)
    return [word[:-1] for word in netfile]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

def test_string_insertion(a_string, a_character):
    """
    tests inserting a_character along all positions in a_string
    """
    for position in range(0, len(a_string)+1):
        print a_string[:position] + a_character + a_string[position:]

#print remove_duplicates([1, 1, 2, 3])
#print remove_duplicates([1, 2, 3, 3, 4, 5, 5, 5])
#print remove_duplicates([])
#print intersect([0, 1, 2, 3], [3, 4, 5, 6])
#print intersect([1, 2, 3], [2, 3, 4])
#print intersect([1], [0, 1])
#print merge([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
#print merge([3, 4, 5, 6, 7], [1, 2, 3, 4, 5])
#print merge([], [1, 2, 3, 4, 5])
#print merge([3, 4, 5, 6, 7], [])
#print merge([0, 1, 2], [99, 100, 101])
#print merge_sort([0, 1, 4, 5, 3, 8, 9, 1, 13, 64, 8, 6, 4, 3, 7, 7, 7])
#print merge_sort([9, 8, 7, 6, 3, 2, 1])
#print gen_all_strings("123")
#print gen_all_strings("")
#print gen_all_strings("thequick")
#print test_string_insertion("thequick", 'P')
#print "the quick brown fox jumped"[1:]
#for line in load_words('http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt'):
#    print line
# Uncomment when you are ready to try the game
run()