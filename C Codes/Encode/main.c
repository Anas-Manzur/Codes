#include <stdio.h>

int main()
{
    int pass,key,en,choice;

    printf("Enter your choice : 1.Encode    2.Decode  ");
    scanf("%d",&choice);
    printf("Enter the password(in numbers) : ");
    scanf("%d",&pass);
    printf("Enter the key(in numbers) : ");
    scanf("%d",&key);


    if(choice==1)
    {
        pass = ~pass;
        pass = pass^key;
        pass = pass<<key;

        printf("The encoded password is : %d",pass);
    }
    if(choice==2)
    {
        pass = pass>>key;
        pass = pass^key;
        pass = ~pass;

        printf("The decoded password is : %d",pass);
    }
    return 0;
}
