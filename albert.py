#!/usr//bin/python2.7
import string
import json


def clean(s): return s.translate(
    string.maketrans("", ""), string.punctuation).lower()


verbs = ['will', 'were', 'know']
articles = ['the', 'an', 'of', 'your', 'my', 'our', 'their', 'a']
pronouns = ['i', 'me', 'you', 'he', 'she', 'we', 'they', 'it']
questions = ['what', 'who', 'where', 'how', 'when', 'why']
misc = ['there', 'if', 'let']

binders = [' is ', ' are ', ' was ']


# Attempt to retrieve memory
with open("dictionary.json", "r") as f:
    try:
        learned = json.load(f)
    except ValueError:
        learned = {}

previous_question, foundBinding = False, False
words = verbs + articles + pronouns + questions + misc
said = input('\n? ')

# Tries to find a noun verb noun binding


def attempt_bindings(said):
    for bind in binders:
        learn = said.split(bind)
        if len(learn) != 1:
            return learn

    return said.split(' is ')


# Input loop
while clean(said) != 'quit':
    # Variables
    learn = attempt_bindings(said)
    working = said.split()
    num_words = len(working)
    first = clean(working[0])

    # Preparation
    all_known, attempt_learn = True, True
    can_respond, simple = False, False
    question_response = "You said it was "
    general_response = "Is that like \""

    # Check for question
    if said[-1] == '?':
        attempt_learn = False

    # Check for commands
    elif first == "showbindings":
        simple = True
        print('> Current bindings are: ')
        print(learned)

    elif first == "clearbindings":
        simple = True
        print("> Cleared bindings")
        learned.clear()

    # Check for simple (yes/no)
    elif first == "yes" and num_words == 1:
        simple = True
        if previous_question:
            print("Great, I'm so smart")
        else:
            print("Yes what?")

    elif first == "no" and num_words == 1:
        simple = True
        if previous_question:
            print("Oh well")
        else:
            print("No what?")

    previous_question = False

    # Check for teaching, then learn
    if attempt_learn and len(learn) > 1:
        can_learn = True
        x = clean(learn[0])
        y = clean(learn[1])
        print("I'm trying to learn...")

        for l in learn:
            l = clean(l.strip())

            if l in words:
                can_learn = False

        if can_learn:
            if x == y:
                print("Obviously")
            else:
                learned[x] = y
                learned[y] = x
                print("Okie doke")

        else:
            print("You're not making any sense")

    # Main
    elif not simple:
        for w in working:
            w = clean(w)

            # Build up possible repsonse
            if w in words:
                general_response = general_response + w + " "

            # Is the word known or unknown?
            if w not in words:
                dic_check = learned.get(w, None)

                if dic_check is not None:
                    can_respond = True
                    general_response = general_response + dic_check + " "
                    question_response = question_response + dic_check + " "
                else:
                    all_known = False

                    if attempt_learn:
                        print('What is ' + w + '?')

        # Output
        if all_known and not can_respond:
            print('Huh, okay')

        elif not can_respond and not attempt_learn:
            print("I don't know, you tell me")

        elif not attempt_learn:
            previous_question = True
            print(question_response)

        elif all_known and can_respond:
            previous_question = True
            print(general_response + '\"?')

    # Next loop
    said = input('\n? ')

# User said quit, save dictionary
with open("dictionary.json", "w") as f:
    json.dump(learned, f)

print("Bye!")
