class Solution:
    
    def longestCommonSubstr(self, str1, str2):
        # Lengths of the input strings
        m = len(str1)
        n = len(str2)
        
        # Initialize the DP table with 0
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Variable to store the maximum length of the common substring
        max_len = 0
        
        # Build the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    max_len = max(max_len, dp[i][j])
                else:
                    dp[i][j] = 0
        
        return max_len

def main():
    str1 = str(input("Enter first String: "))
    str2 = str(input("Enter second string: "))
    sol = Solution()
    result = sol.longestCommonSubstr(str1, str2)
    print(f"Length of longest common string is {result}")

if __name__ == "__main__":
    main()