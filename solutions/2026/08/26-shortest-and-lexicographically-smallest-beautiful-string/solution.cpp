class Solution {
public:
    string shortestBeautifulSubstring(string s, int k) {
        queue <int> q;
        int count = 0;
        int l = 0, r = 0;
        int n = s.size();
        string ans = "";
        while(r<n){
            if (s[r] == '0') {
                r++;
                continue;
            }
            if (count < k){
                q.push(r);
                count++;
            }
            if (count == k){
                if (q.back() == r){
                    ans =s.substr(l, r-l+1);
                    cout<<ans<<endl;
                }
                        
                else{
                    l = q.front() + 1;
                    q.pop();
                    q.push(r);
                }
                    while (l != q.front()+1){
                        string ans_ = s.substr(l, r-l+1);
                        cout<<ans_<<endl;
                        if (ans.size() > ans_.size()) ans = ans_;
                        else if (ans.size() == ans_.size()){
                            ans = min(ans, ans_);
                        }
                        l++;
                    }
                    l--;
                
            }
            r++;
             
        }
        
        return ans;
    }
};