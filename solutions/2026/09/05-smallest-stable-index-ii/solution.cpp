class Solution {
    public:
        int firstStableIndex(vector<int>& nums, int k) {
                int n = nums.size();
                        //vector<int> prefix_max(n);
                                vector<int> postfix_min(n);

                                        int prefix_max = INT_MIN;
                                                postfix_min[n-1] = nums[n-1];

                                                        for(int i=1; i<n; i++){
                                                                    postfix_min[n-i-1] = min(postfix_min[n-i], nums[n-i-1]);
                                                                            }

                                                                                    for(int i=0; i<n; i++){
                                                                                                prefix_max = max(prefix_max, nums[i]); 
                                                                                                            if(prefix_max - postfix_min[i] <= k) return i;
                                                                                                                    }
                                                                                                                            return -1;
                                                                                                                                }
                                                                                                                                };

