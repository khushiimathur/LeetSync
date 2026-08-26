class Solution {
public:
    int missingMultiple(vector<int>& nums, int k) {
        unordered_set<int> st;
        for(int i=0; i<nums.size(); i++){
            st.insert(nums[i]);
        }
        int i =1;
        while (true){
            if(st.find(k*i) == st.end()) return k*i;
            i++;
        }
        return -1;
    }
};