import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Missing command line argument.")
        sys.exit(1)
    # TODO: Read database file into a variable
    # List of dictionaries containing a person's name and their respective highest streak of subsequences
    dnalist = []
    # List of subsequences
    sequences = []
    filename = sys.argv[1]
    with open(filename, "r") as file:
        reader = csv.reader(file)
        # Collecting the column names (subsequences) into the list. We skip the first column as it is only the name
        for row in reader:
            for i in range(1, len(row)):
                sequence = row[i]
                sequences.append(sequence)
            # Make sure to break out of loop after first iteration
            break
        # Creation of dictionary for each row
        for row in reader:
            dna = {"name": row[0]}
            for i in range(1, len(row)):
                # We use i - 1 because i is starting at 1. sequences[i-1] is equivalent to the string of that subsequence, making it easier to map subsequences to highest streak later on.
                dna[sequences[i-1]] = int(row[i])
            dnalist.append(dna)
    # TODO: Read DNA sequence file into a variable
    filename = sys.argv[2]
    with open(filename, "r") as file:
        sequence = file.read()
    # TODO: Find longest match of each STR in DNA sequence
    # Create a dictionary with index for each subsequence
    longest_dict = {}
    for i in range(len(sequences)):
        longest_dict[sequences[i]] = longest_match(sequence, sequences[i])
    # TODO: Check database for matching profiles
    # For each person
    for i in range(len(dnalist)):
        # Matches is our way of seeing if a txt file matches up with one of the people's DNA. It resets for each person.
        # If matches is equal to the length of subsequences, we know that each subsequence is matched up and that the person is a match.
        matches = 0
        # For each subsequence
        for j in range(len(sequences)):
            if dnalist[i][sequences[j]] == longest_dict[sequences[j]]:
                matches = matches + 1
                if matches == len(sequences):
                    print(dnalist[i]["name"])
                    sys.exit(0)
    # Print no match if there is no match
    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
