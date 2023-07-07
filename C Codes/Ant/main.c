#include <stdio.h>
#include <math.h>

int main()
{
    float n,w,e,s,r1=0,r2=0,res,i;
    char d;

    printf("Enter the direction(in mm) serially(e.g. 5 W).\nEnter 1 q when done.\n");

    while(d!='q')
    {
        scanf("%f %c",&i,&d);
        if(d=='N')r1=r1+i;
        else if(d=='S')r1=r1-i;
        else if(d=='E')r2=r2+i;
        else if(d=='W')r2=r2-i;
        else if(d!='q')printf("Invalid direction.\n");
    }
    res=sqrt(pow(r1,2)+pow(r2,2));
    printf("The position of the ant is (%f,%f).\n",r1,r2);
    printf("Where the North and East are considered positive.\n");
    printf("The distance covered by it : %f",res);
    return 0;
}
