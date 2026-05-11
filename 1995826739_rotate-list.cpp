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
    ListNode* rotateRight(ListNode* head, int k) {
        if(head==NULL || head->next==NULL)return head;
        ListNode* copy_head=head;
        int len=1;
        while(copy_head->next){
           copy_head=copy_head->next;
           len++;
        }
        k=k%len;
        if(k==0)return head;

        copy_head->next=head;

        ListNode* new_head=head;

        for(int i=0; i<len-k-1; i++){
            new_head=new_head->next;
        }

        ListNode* ans_head=new_head->next;
        new_head->next=NULL;

        return ans_head;

       
    }
};