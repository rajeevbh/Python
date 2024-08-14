class Solution:
    def findFacotorial(self,n):
        
        # Initializing DP array with 1 [1,1,1,1,1]
        dp = [1] * (n+1)

        for i in range(2, n + 1):  # value of i from 2 to 6
            dp[i] = i * dp[i-1]
        return dp[i]



def main():
    n = int(input("Enter a number to find the factorial: "))
    sol = Solution()
    result = sol.findFacotorial(n)
    print(f"The factorial of {n} is {result}")

# To run input function
if __name__ == "__main__3":
    main()
