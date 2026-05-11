class Solution {
public:
    vector<int> separateDigits(vector<int>& nums) {
        int n=nums.size();
        vector<int> ans;
        stack<int> st;
        for(int i=0; i<n; i++){
            do{
                int d=nums[i]%10;
                st.push(d);
                nums[i]/=10;
            }while(nums[i]>0);
            while(!st.empty()){
                int d=st.top();
                ans.push_back(d);
                st.pop();
            }
        }
        return ans;
    }
};