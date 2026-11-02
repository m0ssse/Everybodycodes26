def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]

def calculate_value(weights, num):
    l = len(weights)
    total = 0
    for i in range(len(num)):
        total+=int(num[~i])*int(weights[(l-i-1)%l])**i
    return total

def find_smallest_representation(weights, num, value):
    for i in range(int(num)):
        val = calculate_value(weights, str(i))
        if val==value:
            return i
    return num

def part1(fname):
    votes = read_input(fname)
    res = 0
    for vote in votes:
        weights, num = vote[4:].split()
        res+=calculate_value(weights, num)
    return res

def part3(fname):
    votes = read_input(fname)
    res = 0
    for vote in votes:
        weights, num = vote[5:].split()
        value = calculate_value(weights, num)
        if find_smallest_representation(weights, num, value)==num:
            res+=value
    return res

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part1("input2.txt"))
    print(part3("input3.txt"))