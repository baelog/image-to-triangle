
# Usage

```
> python main.py <input image with transparence> <outputfile>
```
  
# Output structure

```C
struct point {
    int x;
    int y;
} __attribute__((packed));

struct triangle {
    struct point a;
    struct point b;
    struct point c;

} __attribute__((packed));

struct fileContent {
    int size;
    struct triangle t[];
} __attribute__((packed));
```
