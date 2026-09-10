/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    pair<int, int> func(TreeNode *root, int &count){
        if(root == nullptr) return {0,0};

        auto [count1, num1] = func(root->left, count);
        auto [count2, num2] = func(root->right, count);

        if((count1+count2 + root->val)/(num1+num2+1) == root->val){
            cout<<root->val<<endl;
            count++;
        } 

        return {count1+count2 + root->val, num1+num2+1};
    }
    int averageOfSubtree(TreeNode* root) {
        int count = 0;
        func(root, count);
        return count;
    }
};