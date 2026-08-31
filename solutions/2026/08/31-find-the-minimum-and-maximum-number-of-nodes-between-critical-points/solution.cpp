/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    vector<int> nodesBetweenCriticalPoints(ListNode* head) {
        ListNode *node = head->next;
        ListNode *prev = head;
        int pos = 1;
        int first = -1;
        int last = -1;
        vector<int> dist = {INT_MAX, INT_MIN};
        //vector<long long> nums;
        while(node->next != NULL){
            if((prev->val < node->val && node->next->val < node->val) || 
            (prev->val > node->val && node->next->val > node->val)){
                if(first == -1) {
                    first = pos;
                    last = pos;
                }
                else{
                    dist[0] = min(dist[0], pos-last);
                    last = pos;
                } 
            }
            
            prev = node;
            node = node->next;
            pos++;
        }
        if(dist[0] == INT_MAX) return {-1,-1};
        dist[1] = last-first;
        return dist;

    }
};