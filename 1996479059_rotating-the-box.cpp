class Solution {
public:
    vector<vector<char>> rotateTheBox(vector<vector<char>>& boxGrid) {
        int n=boxGrid.size();
        int m=boxGrid[0].size();
        int stones=0;
        int empty=0;
        for(int i=0;i<n; i++){
            int available=m-1;
            for(int j=m-1; j>=0; j--){
                if(boxGrid[i][j]=='#'){
                    boxGrid[i][j]='.';
                    boxGrid[i][available]='#';
                    available--;
                }else if(boxGrid[i][j]=='*'){
                    available=j-1;
                }
            }
        }
        vector<vector<char>> rotatedBox(m, vector<char>(n));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                rotatedBox[j][n - 1 - i] = boxGrid[i][j];
            }
        }

        return rotatedBox;
    }
};