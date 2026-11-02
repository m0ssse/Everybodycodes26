def read_input(fname):
    with open(fname) as file:
        return [int(x) for x in file.readline().split(",")]

def sqrt(n):
    L = 0
    R = n
    while L<R:
        M = (L+R)//2
        if M**2==n:
            return M
        elif M**2<n:
            L = M+1
        else:
            R = M
    return R

def part1(fname):
    nums = read_input(fname)
    res = 0
    for x in nums:
        res+=sqrt(x)**2-x
    return res

def part2(fname):
    nums = read_input(fname)
    res = 0
    for x in nums:
        n = max(3, (x+3)//4+1)
        res+=4*(n-1)-x
    return res

def part3(fname):
    nums = read_input(fname)
    res = 0
    for x in nums:
        n = 2*(sqrt(x+1)//2)+1 #force n to be n+1 if n is odd
        res += n**2-1-x
    return res

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))