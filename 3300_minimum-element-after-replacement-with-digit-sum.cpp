class Solution {
public:
    int minElement(vector<int>& nums) {
        int ans=INT_MAX;
        int sum=0;
        for(int i=0; i<nums.size(); i++){
            while(nums[i]>0){
            int digit =nums[i]%10;
            nums[i]/=10;
              sum+=digit;
        }
        ans=min(ans,sum);
        sum=0;
        if(ans==0)return 0;
        }
          return ans;
    }
};