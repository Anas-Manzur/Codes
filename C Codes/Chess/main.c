#include <stdio.h>
#include <stdlib.h>

int main()
{
    int board[10][10]={1,1,1,1,1,1,1,1,1,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,0,0,0,0,0,0,0,0,1,
                       1,1,1,1,1,1,1,1,1,1};
    char ok_col,n_col,b_col,k_col;
    int k_row,ok_row,n_row,b_row,k_colm,ok_colm,n_colm,b_colm,i,j=1,count=1,k=1;

    printf("Enter the position of your king(e.g. A 5) : ");
    scanf("%c %d",&k_col,&k_row);
    fflush(stdin);
    printf("Enter the position of your knight(e.g. A 5) : ");
    scanf("%c %d",&n_col,&n_row);
    fflush(stdin);
    printf("Enter the position of your bishop(e.g. A 5) : ");
    scanf("%c %d",&b_col,&b_row);
    fflush(stdin);
    printf("Enter the position of opponent's king(e.g. A 5) : ");
    scanf("%c %d",&ok_col,&ok_row);

    k_colm=k_col-64;
    n_colm=n_col-64;
    b_colm=b_col-64;
    ok_colm=ok_col-64;

    for(i=1;i<=8;i++)
    {
        j=b_row-(b_colm-i);
        board[j][i]=1;
        j=b_row+(b_colm-i);
        board[j][i]=1;
    }

    for(i=n_row-2;i<=n_row+2;i++)
    {
        if(i!=n_row)
        {
            j=n_colm-count;
            board[i][j]=1;board[i][n_colm+count]=1;
        }
        if(i==n_row)
        {
            board[i][n_colm]=1;
            k=-1;
        }
        count+=k;
    }

    for(i=k_row-1;i<=k_row+1;i++)
    {
        for(j=k_colm-1;j<=k_colm+1;j++)
        {
            board[i][j]=1;
        }
    }
    k=1;
    for(i=ok_row-1;i<=ok_row+1;i++)
    {
        for(j=ok_colm-1;j<=ok_colm+1;j++)
        {
            if(board[i][j]==0)k=0;
        }
    }

    if(k==1)printf("\nCheckmate!!");
    else printf("\nThere is no checkmate.");

    return 0;
}
