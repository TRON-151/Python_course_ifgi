def donuts(count):
    # main message
    message = 'Number of donuts: '

    # check if the count is a string or not, if yes then give error
    if (type(count) == str) or (count <= 0):
        return "Error: Please enter a integer"
    
    # if it is less than 0 give error
    if count <= 0:
        return 'Error: Please enter a number bigger than 0'
    
    # if the count is less than 10 or greater than 0, then give desirable output
    elif count < 10 and count > 0: 
        message += str(count)
        return message
    
    # if its more than 10, then output many
    elif count >= 10:
        message += 'many'
        return message
    

def verbing(s):
    #main message
    end_word = 'ing'

    #check the length and ending of the word
    if len(s) >= 3 and s[-3:] != 'ing':
        return s + 'ing'
    
    #add 'ly' if the word ends with 'ing'
    elif s[-3:] == 'ing':
        return s + 'ly'
    
    #return the word if it's length is less than 2
    elif len(s) <=2:
        return s

def remove_adjacent(nums):
    #lets make a new list first
    new_list = []

    #iterate through all elements in the list
    for i in range(len(nums)):

        #append either the elements is first or it doesn't matches with the previous one    
        if i == 0 or nums[i] != nums[i - 1]:
            new_list.append(nums[i])
    return new_list

def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))

    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))

    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))

if __name__ == '__main__':
    main()