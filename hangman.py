# ideal hangman player

# oh yeah its regex time
import re

# loading in a really long list of words
dictionary = open('wordlist.txt','r')

alphabet_string = "qwertyuioplkjhgfdsazxcvbnm"

wordlist = ''

letter_scores = {}

for line in dictionary:
	word = line[:-1]
	if word.isalpha():
		wordlist += word + ' '

		for character in word:

			if character in letter_scores:
				letter_scores[character] += 1 

			else:
				letter_scores[character] = 1

# now dict is ordered by the nubmer of occurences
letter_scores = dict(sorted(letter_scores.items(), key=lambda item: item[1], reverse=True))

letter_scores = [item for item in letter_scores.items()]

# change rules at will
num_guesses = 7

def str_isolate(word_string, leave_char):

	new_str = ''

	for letter in word_string:
		if letter == leave_char:
			new_str += leave_char 
		else:
			new_str += "."

	return new_str

def any_chars_in(word, chars):
	return any([char in word for char in chars])

# will try to pick words so as to make it as difficult as possible
def you_are_guesser(num_guesses_remaining, is_guessed, letters_tried, letters_forbidden, word_string):

	if is_guessed:
		print("You got it!")


	elif num_guesses_remaining == 0 and not is_guessed:
		print("bad luck, you didn't get the word")

		answer = re.findall(rf"\b{word_string}\b", wordlist)

		answer = list(filter(lambda word: not ' ' in word and not any_chars_in(word, letters_forbidden), answer))

		# ensure number of occurances is consistent

		num_occurances = {letter: word_string.count(letter) for letter in word_string if letter != "."}
		answer = list(filter(lambda word: all([num_occurances[letter] == word.count(letter) for letter in word if letter in word_string]), answer))

		word_answer = answer[0]
		print("the answer was: " + word_answer)



	# game aint over
	else:

		print("Letters you've guessed: " + str(letters_tried))
		print("Guesses remaining: " + str(num_guesses_remaining))

		print("Here's the word so far: " + word_string)

		remaining = re.findall(rf"\b{word_string}\b", wordlist)

		# make sure it's only a single word
		# make sure no forbidden letters

		remaining = list(filter(lambda word: not ' ' in word and not any_chars_in(word, letters_forbidden), remaining))

		# make sure the number of occurences of all the letters present is the same 

		num_occurances = {letter: word_string.count(letter) for letter in word_string if letter != "."}

		remaining = list(filter(lambda word: all([num_occurances[letter] == word.count(letter) for letter in word if letter in word_string]), remaining))

		if len(remaining) == 0:
			print("no word is that long!")

		# game is over, you won
		elif word_string.count(".") == 0:
			print(remaining[0])
			you_are_guesser(num_guesses_remaining, True, letters_tried, letters_forbidden, remaining[0])

		else:

			letter_guess = None

			while not isinstance(letter_guess, str) or not letter_guess.isalpha() or len(letter_guess) != 1 or letter_guess in letters_tried:
			
				letter_guess = input("What is your guess? (single letters only, no repeats): ")

			# find number of words that cantain that letter, in various combinations

			template_array = [str_isolate(word, letter_guess) for word in remaining]

			frequencies = {}

			for template in template_array:
				if template in frequencies:
					frequencies[template] += 1

				else:

					frequencies[template] = 1

			# find place of that letter with max words like that

			# we do this by stripping the words in with_letter of everything but the letter we're looking for

			# then we see which positioning is the most common

			best_template = max(frequencies, key=lambda template: frequencies[template])

			"""

			# testing the inner workings

			print()
			print(frequencies)
			print()
			print(best_template)
			print()
			print(best_template.count("."))

			"""

			# if the most common is none of that letter at all, then the letter is not there

			if best_template.count(".") == len(best_template):
				print("Sorry, the letter isn't there")

				you_are_guesser(num_guesses_remaining - 1, is_guessed, letters_tried + [letter_guess], letters_forbidden + [letter_guess], word_string)

			# else pick the best way that letter can appear

			else:
				print("Nice, the letter is there")

				# fill in word (i.e. change word_string)

				new_word_string = ''

				for i in range(len(word_string)):
					if word_string[i] == '.':
						new_word_string += best_template[i]
					
					else:
						new_word_string += word_string[i]

				you_are_guesser(num_guesses_remaining, is_guessed, letters_tried + [letter_guess], letters_forbidden, new_word_string)

	


def optimal_machine_guessing(guesses_remaining, known_string, letters_tried, letters_forbidden):

	# choose the letter whose denial would be the most revealing

	return None





def probablistic_machine_guessing(num_guesses):

	def guess():
		nonlocal known_string, is_guessed, num_guesses, letters_forbidden, letters_used

		print("OK, here's what we have so far (dots mean unknown letters)")

		print(known_string)

		possible = re.findall(rf"\b{known_string}\b", wordlist)
		possible = list(filter(lambda word: not ' ' in word and not any_chars_in(word, letters_forbidden), possible))

		letter_freq = {alphabet: 0 for alphabet in alphabet_string}

		for word in possible:
			for letter in alphabet_string:

				if letter in word and letter not in letters_used:
					letter_freq[letter] += 1

		print(letter_freq)

		computer_guess = max(list(letter_freq.items()), key=lambda x: x[1])

		print("I guess: " + computer_guess[0])

		match = input("Was I right? (y/n) ")

		while not match in ["y", "yes"] and not match in ["n", "no"]:

			match = input("Was I right? (y/n) ")

		# if we are right, make necessary adjustments

		if match in ["y", "yes"]:
			print("Type in where the letters are supposed to go")
			print("For example, if the word was 'barred' and you guessed r")
			print("You would write '..rr..'")
			print("Don't worry about the other letters, we'll fill them in")

			template = input("Type in the word template: ")

			while template.count(".") + template.count(computer_guess[0]) != len(template) or len(template) != len(known_string) or any([known_string[i] != "." and template[i] != "." for i in range(len(known_string))]):
				template = input("Type in the word template: ")

			new_known_string = ''

			for i in range(len(known_string)):
				if known_string[i] == '.':
					new_known_string += template[i]
					
				else:
					new_known_string += known_string[i]

			known_string = new_known_string

			print("This is what I know: " + known_string)

			letters_used += [computer_guess[0]]

		else:
			num_guesses -= 1

			letters_forbidden += [computer_guess[0]]
			letters_used += [computer_guess[0]]

	
	is_guessed = False
	letters_forbidden = []
	letters_used = []

	print("Hello human, let's play some hangman")
	print("Think of a single word, any word.")

	letter_num = ""

	while not letter_num.isnumeric():

		letter_num = input("Type the number of letters it has: ")

	letter_num = int(letter_num)

	known_string = ''.join(["." for i in range(letter_num)])

	while num_guesses > 0 and not is_guessed:
		
		guess()

	if num_guesses == 0:
		print("I lost!")

		input("what was the word? ")
		print("ah, ok cool beans")

	if is_guessed:
		print("Gotcha! GG play again sometime")





# you_are_guesser(num_guesses, False, [], [], ".........")

probablistic_machine_guessing(num_guesses)

# optimal_machine_guessing(guesses_remaining, known_string, letters_tried, letters_forbidden)

