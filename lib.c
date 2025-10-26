#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "lib.h"

struct node {struct node* next; i64 x; i64 y; char val;} ;
typedef struct node node;

i64 BOMB = 9;

i64 read_num;
char read_acc;

i64 write_num;
char write_acc;


node** hashmap;
size_t n;
size_t used;

i64 hash(i64 x,i64 y)
{
    return (x*y)%n;
    
}

void startup()
{
    read_num = 0;
    write_num = 0;

    used = 0;
    n = 8;
    hashmap = malloc(sizeof(node*)*n);
    for(size_t x = 0; x < n; x++)
    {
        hashmap[x] = NULL;
    }
}

char* get(i64 x, i64 y)
{
    node* ptr = hashmap[hash(x,y)];
    while(ptr != NULL)
    {
        if(ptr->x == x && ptr->y == y)
        {
            return &ptr->val;
        }
        ptr = ptr->next;
    }
    return NULL;
}

void add(i64 x, i64 y,char c)
{
    char* g = get(x,y);
    if(g == NULL)
    {
        if(used >= n)
        {
            n *= 2;
            used = 0;
            node** old = hashmap;
            hashmap = malloc(sizeof(node*)*n);
            for(size_t x = 0; x < n; x++)
            {
                hashmap[x] = NULL;
            }
            for(size_t x = 0; x < n/2; x++)
            {
                node* ptr = old[x];
                while(ptr != NULL)
                {
                    add(ptr->x,ptr->y,ptr->val);
                    node* temp = ptr;
                    ptr = ptr->next;
                    free(temp);
                }
            }    
            free(old);    
            add(x,y,c);    
        }
        else
        {
            i64 h = hash(x,y);
            node* new = malloc(sizeof(node));
            new->x = x;
            new->y = y;
            new->val = c;
            new->next = hashmap[h];
            hashmap[h] = new;
            used++;
        }
    }
    else
    {
        *g = c;
    }
}



void PLACE(i64 x,i64 y)
{

    char* g = get(x,y);
    if(g == NULL || *g != BOMB){
        add(x,y,BOMB);
        for(int a = x-1; a <= x+1; a++)
        {
            for(int b = y-1; b <= y+1; b++)
            {
                if(a != x || b != y)
                {
                    char* g = get(a,b);
                    if(g == NULL)
                    {
                        add(a,b,1);
                    }
                    else if(*g == BOMB)
                    {}
                    else
                    {
                        (*g)++;
                    }
                }
            }
        }
    }
    else{assert(0&&"ALREADY BOMB");}
}


void FLAG(i64 x,i64 y)
{

    char* g = get(x,y);
    if(g == NULL || *g != BOMB){assert(0&&"NOT A BOMB!");}
    *g = 0;

    for(int a = x-1; a <= x+1; a++)
    {
        for(int b = y-1; b <= y+1; b++)
        {
            if(a != x || b != y)
            {
                char* g2 = get(a,b);
                if(g2 == NULL)
                {
                    add(a,b,1);
                }
                else if(*g2 == BOMB)
                {
                    (*g)++;
                }
                else
                {
                    (*g2)++;
                }
            }
        }
    }

}
i64 TEST(i64 x, i64 y)
{
    char* g = get(x,y);
    if(g == NULL){return 0;}
    if(*g == BOMB)
    {
        assert(0&&"BOMB!");
    }
    return *g;
}


void WRITE(i64 x,i64 y)
{
    char* g = get(x,y);
    int bit;
    if(g == NULL)
    {
        bit = 0;
    }
    else if(*g == BOMB)
    {
        bit = 1;
    }
    else 
    {
        bit = 0;
    }
    write_num++;
    write_acc *= 2;
    write_acc += bit;
    if(write_num == 8)
    {
        //printf("AAA\n");
        putchar(write_acc);
        fflush(stdout);
        //printf("%c\n",write_acc);
        write_num = 0;
    }
}

void READ(i64 x,i64 y)
{
    if(read_num == 0)
    {
        int temp = getchar();
        if (temp == EOF)
        {
            assert(0&&"EOF");
        }
        read_acc = temp;
        read_num = 8;
    }
    read_num--;
    int bit = 1 & read_acc;
    read_acc = read_acc / 2;

    PLACE(x,y);
}


void SYSCALL(i64 x,i64 y)
{
    assert(0&&"not yet implemented");
}