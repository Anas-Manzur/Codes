#include <stdio.h>
#include <math.h>

int main()
{
    int choice,i,num,res=0,rem,r=1,a;

    printf("Enter your conversion : \n1.Dec to Bin\t2.Bin to Dec\t");
    scanf("%d", &choice);
    printf("Enter your number : ");
    scanf("%d", &num);

    if(choice==1)
    {
        a=num;
        for(i=0;r;i++)
        {
            rem=num%2;
            num=num/2;
            res=res+pow(10,i)*rem;
            printf("%d ",res);
            if(num==0||num==1)
            {
                res=res+pow(10,i+1)*num;
                r=0;
                if(a>11)res=res+1;
                if(a>19 && a<24)res=res+1;
            }
        }
        printf("\nThe number is %d",res);
    }
    else if(choice==2)
    {
        for(i=0;i<=sizeof(num);i++)
        {
            rem=num%10;
            num=num/10;
            res=res+pow(2,i)*rem;
        }
        printf("\nThe number is %d",res);
    }
    else printf("\nInvalid choice.");

    return 0;
}
