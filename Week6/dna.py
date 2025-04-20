import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <sequence.txt>")
        sys.exit(1)

    # Reading the dataset into the variable, headers and data is seperated.
    rows = []
    with open(f"{sys.argv[1]}") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable.
    with open(f"{sys.argv[2]}") as file:
        reader = csv.reader(file)
        sequence = next(reader)

    # Find longest match of each STR in DNA sequence
    result = []
    for i in range(1, len(headers), 1):
        result.append(longest_match(sequence[0], headers[i]))

    # Check database for matching profiles
    for i in range(len(rows)):
        for j in range(1, len(headers)):
            if not (int(rows[i][headers[j]]) == int(result[j-1])):
                match = False
                break
            else:
                match = True
        if (match == True):
            print(rows[i][headers[0]])
            return

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
