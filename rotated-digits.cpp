class Solution {
public:
    int rotatedDigits(int n) {
        
        int count=0;
        for(int i=1; i<=n; i++){
            int temp = i;
            bool has_diff = false;
            bool is_valid = true;
            
            while (temp > 0) {
                int digit = temp % 10;
                // If it contains 3, 4, or 7, the whole number is invalid
                if (digit == 3 || digit == 4 || digit == 7) {
                    is_valid = false;
                    break;
                }
                // If it contains 2, 5, 6, or 9, it will differ from the original
                if (digit == 2 || digit == 5 || digit == 6 || digit == 9) {
                    has_diff = true;
                }
                temp /= 10;
            }
            
            if (is_valid && has_diff) {
                count++;
            }
        }
        return count;
    }
};