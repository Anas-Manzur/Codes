 #include <stdio.h>

 int part(int a[],int p,int q);
 void qsort(int a[],int p,int q);

 int main()
 {
     int n,i;
     printf("Enter the size of the array : ");
     scanf("%d",&n);
     int a[n];
     printf("Enter the Elements : \n");
     for(i=0;i<n;i++)
     {
         scanf("%d",&a[i]);
         fflush(stdin);
     }

     qsort(a,0,n-1);

     printf("The sorted array is : ");
     for(i=0;i<n;i++)printf("%d ",a[i]);

     return 0;
 }

 void qsort(int a[],int p,int q)
 {
     if(p<q)
    {
        int r;
        r=part(a,p,q);
        qsort(a,p,r-1);
        qsort(a,r+1,q);
     }
 }
 int part(int a[],int p,int q)
 {
     int temp,i,j;
     i=p-1;
     for(j=p;j<q;j++)
     {
         if(a[j]<=a[q])
         {
             i++;
             temp=a[j];
             a[j]=a[i];
             a[i]=temp;
         }
     }
     temp=a[i+1];
     a[i+1]=a[q];
     a[q]=temp;
     return (i+1);
 }
