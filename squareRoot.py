class Solution:
    def floorSqrt(self, n):
        if n == 0 or n == 1:
            return n
        
        # Intializing required variables
        low = 1
        high = n
        mid = 0
        ans = 0

        while low <= high:
            mid = (low + high) // 2

            if (mid * mid) == n:
                return mid
        
            if (mid * mid) < n:
                low = mid + 1
                ans = mid
            else:
                high = mid - 1

        return ans


def main():
    # Input function to take user input
    n = int(input("Enter a number to find its floor square root: "))
    
    # Create an instance of the Solution class
    sol = Solution()
    
    # Call the floorSqrt function and display the result
    result = sol.floorSqrt(n)
    print(f"The floor square root of {n} is: {result}")

# Run the input function
if __name__ == "__main__":
    main()

