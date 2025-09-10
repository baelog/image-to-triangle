# Description

It creates a list of triangles from a simple image. It will take the outline of the image with a transparency and will give the list of triangles as a binary output file.

It does not filter any color. It's working only with the drawing outline.

If there is more than one drawing, it will work only with the first one.

# Usage

```
> python main.py <input image with transparency> <outputfile>
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
