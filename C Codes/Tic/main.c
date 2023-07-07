#include <stdio.h>

int check();
void mini(int i,int j,int l,int *q);

int board[3][3]={0,0,0,
                 0,0,0,
                 0,0,0};
int moves[3][3]={0,0,0,
                 0,0,0,
                 0,0,0};

int main()
{
    int r,c,i,j,l=1,low,lr,lc;
    while(check()==0)
    {
        x: printf("\nEnter your opponent's move (R C) : ");
        scanf("%d %d",&r,&c);
        if(board[r-1][c-1]==0)board[r-1][c-1]=1;
        else
        {
            printf("\nInvalid choice");
            goto x;
        }
        for(i=0;i<3;i++)
        {
            for(j=0;j<3;j++)
            {
                if(board[i][j]==0 && moves[i][j]==0)
                {
                    mini(i,j,l,&moves[i][j]);
                }
            }
        }
        for(i=0;i<3;i++)
        {
            for(j=0;j<3;j++)
            {
                if(board[i][j]==0)low=moves[i][j];lr=i;lc=j;
            }
        }
        for(i=0;i<3;i++)
        {
            for(j=0;j<3;j++)
            {
                if(moves[i][j]>low && board[i][j]==0)
                {
                    low=moves[i][j];
                    lr=i;lc=j;
                }
            }
        }
        if(check()!=0)goto z;
        printf("\nThe best move is (R C): %d %d",lr+1,lc+1);
        y: printf("\nEnter your move (R C): ");
        scanf("%d %d",&r,&c);
        if(board[r-1][c-1]==0)board[r-1][c-1]=2;
        else{printf("\nInvalid choice");goto y;}
        z:
        for(i=0;i<3;i++)
        {
            for(j=0;j<3;j++)
            {
                moves[i][j]=0;
            }
        }
    }
    printf("The game is over.");
    return 0;
}
int check()
{
    int i,j;
    for(i=0;i<3;i++)
    {
        if(board[0][i]==1 && board[1][i]==1 && board[2][i]==1)return -100;
        if(board[0][i]==2 && board[1][i]==2 && board[2][i]==2)return 100;
    }
    for(i=0;i<3;i++)
    {
        if(board[i][0]==2 && board[i][1]==2 && board[i][2]==2)return 100;
        if(board[i][0]==1 && board[i][1]==1 && board[i][2]==1)return -100;
    }
    if(board[0][0]==2 && board[1][1]==2 && board[2][2]==2)return 100;
    if(board[0][0]==1 && board[1][1]==1 && board[2][2]==1)return -100;
    if(board[2][0]==1 && board[1][1]==1 && board[0][2]==1)return -100;
    if(board[2][0]==2 && board[1][1]==2 && board[0][2]==2)return 100;
    for(i=0;i<3;i++)
    {
        for(j=0;j<3;j++)
        {
            if(board[i][j]==0)return 0;
        }
    }
}
void mini(int i,int j,int l,int *q)
{
    int m,n,e11,e12,e13,e21,e22,e23,e31,e32,e33,r=0,k;
    l++;
    e11=board[0][0];e12=board[0][1];e13=board[0][2];
    e21=board[1][0];e22=board[1][1];e23=board[1][2];
    e31=board[2][0];e32=board[2][1];e33=board[2][2];
    if(l%2==0)board[i][j]=2;
    else if(l%2==1)board[i][j]=1;
    if(check()==0)
    {
        for(m=0;m<3;m++)
        {
            for(n=0;n<3;n++)
            {
                if(board[m][n]==0)
                {
                    mini(m,n,l,q);
                }
            }
        }
    }
    *q+=check();
    board[0][0]=e11;board[0][1]=e12;board[0][2]=e13;
    board[1][0]=e21;board[1][1]=e22;board[1][2]=e23;
    board[2][0]=e31;board[2][1]=e32;board[2][2]=e33;
}

