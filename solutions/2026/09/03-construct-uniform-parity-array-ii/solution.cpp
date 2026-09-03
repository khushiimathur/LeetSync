class Solution {
public:
    bool uniformArray(vector<int>& nums1) {
        // int min_even = INT_MAX, min_odd = INT_MAX;
        int n = nums1.size();
        // bool even = false, odd = false;
        bool odd = false;
        int mini = INT_MAX;
        for(int i=0; i<n; i++){
            if (nums1[i] % 2 != 0) odd = true;
            mini = min(mini, nums1[i]);
        }
        // if (even == false || odd == false) return true;
        // if (min_even > min_odd) return true;
        if(odd != false && mini %2 ==0)return false;
        return true;
    }
};