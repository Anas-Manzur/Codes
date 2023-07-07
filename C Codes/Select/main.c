#include <stdio.h>

int main()
{
    int n,i,j,temp;
    printf("Enter the size of the array : ");
    scanf("%d",&n);
    int arr[n];
    printf("Enter the elements : \n");
    for(i=0;i<n;i++)scanf("%d",&arr[i]);

    for(i=0;i<n;i++)
    {
        for(j=0;j<n;j++)
        {
            if(arr[j]>arr[i])
            {
                temp=arr[i];
                arr[i]=arr[j];
                arr[j]=temp;
            }
        }
    }
    printf("The sorted array is : ");
    for(i=0;i<n;i++)printf("%d ",arr[i]);
    return 0;

}
