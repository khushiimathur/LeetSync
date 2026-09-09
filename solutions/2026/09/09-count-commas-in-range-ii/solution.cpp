class Solution {
public:
    long long countCommas(long long n) {
        long long ans =0;
        for(int i=3; i<=15; i+=3){
            if(n>= pow(10, i)){
                ans += (n-pow(10, i)) + 1;
            }
            else break;
        }
        return ans;
    }
};