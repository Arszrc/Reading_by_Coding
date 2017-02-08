//
// Created by Horo on 2/8/17.
//
#include <stdlib.h>
#include <stdio.h>

#ifndef AvlTree_H

struct AvlNode;
typedef int Elementype;
typedef struct AvlNode *Position;
typedef struct AvlNode *AvlTree;

AvlTree MakeEmpty(AvlTree T) ;
Position Find(Elementype X, AvlTree T);
Position FindMin( AvlTree T);
Position FindMax(AvlTree T);
AvlTree Insert(Elementype X, AvlTree T);
AvlTree Delete(Elementype X, AvlTree T);

#endif


struct AvlNode
{
    Elementype Element;
    AvlTree        Left;
    AvlTree        Right;
    int                Height;
};


static int Height(Position P)
{
    if(P == NULL)
        return -1;
    else
        return P->Height;
}


int Max(int x, int y)
{
    if(x > y)
        return x;
    else
        return y;
}


static Position SingleRotateWithLeft(Position K2)
{
    Position K1;

    K1 = K2->Left;
    K2->Left = K1->Right;
    K1->Right = K2;

    K1->Height = Max(Height(K1->Left), Height(K1->Right)) + 1;
    K2->Height = Max(Height(K2->Left), Height(K2->Right)) + 1;

    return K1;      // New Root
}


static Position SingleRotateWithRight(Position K2)
{
    Position K1;

    K1 = K2->Right;
    K2->Right = K1->Left;
    K1->Left = K2;

    K1->Height = Max(Height(K1->Left), Height(K1->Right)) + 1;
    K2->Height = Max(Height(K2->Left), Height(K2->Right)) + 1;

    return K1;      // New Root
}


static Position DoubleRotateWithLeft(Position K3)
{
    // Rotate between K1 and K2
    K3->Left = SingleRotateWithRight(K3->Left);

    // Rotate between K3 and k3
    return SingleRotateWithLeft(K3);
}


static Position DoubleRotateWithRight(Position K3)
{
    K3->Right = SingleRotateWithLeft(K3->Right);

    return SingleRotateWithRight(K3);
}


AvlTree Insert(Elementype X, AvlTree T)
{
    if(T == NULL)
    {
        T = malloc(sizeof(struct AvlNode));
        if(T == NULL)
            printf("Out of space !");
        else
        {
            T->Element = X;
            T->Height = 0;
            T->Left = T->Right = NULL;
        }
    }
    else if(X < T->Element)
    {
        T->Left = Insert(X, T->Right);
        if(Height(T->Left) - Height(T->Right) == 2)
            if(X < T->Left->Element)
                T = SingleRotateWithLeft(T);
            else
                T = DoubleRotateWithLeft(T);
    }
    else if(X > T->Element)
    {
        T->Right = Insert(X, T->Right);
        if(Height(T->Right) - Height(T->Left) == 2)
            if(X>T->Right->Element)
                T = SingleRotateWithRight(T);
            else
                T = DoubleRotateWithRight(T);
    }
    // Else X is already in the Tree, we do nothing.

    T->Height = Max(Height(T->Left), Height(T->Right)) + 1;

    return T;
}


int main()
{
    AvlTree myTree;
    Insert(1, myTree);
    Insert(23, myTree);

    return 0;
}