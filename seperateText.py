

# Example usage
input_file = 'words.txt'  # Replace with your input file path
output_file = 'hard_words.txt'  # Replace with your desired output file path

print('s')
f = open("word.txt", "r")
lines = f.readlines()
    
print(lines)
# Filter out lines containing words with fewer than 3 letters
result_lines = []
for line in lines:
    print(len(line))
    if len(line) >= 9:
        result_lines.append(line)
    
# Write the filtered lines to the output file
with open(output_file, 'w') as file:
        file.writelines(result_lines)
        
print(f"Filtered content has been saved to {output_file}")
