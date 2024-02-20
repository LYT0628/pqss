# PQSS
PQSS is a dynamic language for qss, like scss for css.
For more details, see official site: [Sqss | Dynamic Lagrange for qss](lyt0628.icu/docs/sqss).

# Installation
```shell
  pip install pqss
```
or download with Conda
```shell
    conda install pqss
```
Compile code in Commandline:
```shell
pqss -f style.pqss -o style.qss
```
or in python:

```python
import pqss

if __name__ == "__main__":
    source = """
        $a : 5; 
        MyClass { 
            width: $a;
            height: $a;
        }
    """
    qss = pqss.compile_pqss(source)
    print(qss)
```

## Tutorial
### Comment
```sqss
// comment
```
or multiline 
```sqss
/*
 * This is comment for sqss
*/
```
### Variable
```sqss
$a : 5; 
QOushButton { 
    width: $a;
    height: $a; 
}
```
### Embed Ruleset
```sqss 
QMainWindow { 
    width: 600;
    height: 481; 
    Widget {
        background-color: gray;
    }
}
```
### Parent Reference

```sqss
QOushButton { 
    width: 20;
    height: 20;
    &: hover{
        background-color: gray;
    } 
}
```
### Embed Property
```sqss
QPushButton{
    borlder{
        width: 5;
        color: red;
        top{
            width: 3;
            color: yellow;
        }
    }
}
```
## Mixin
```sqss
@mixin fn {
    background: gray;
}
QOushButton { 
    @include fn;
}
```
with arguments:
```sqss
@mixin fn($va0, $var1) {
    background: $var0;
    color: $var1;
}
QOushButton { 
    @include fn(gray, white);
}
```

### Extend
```sqss
QPushButton { 
    width: 25px;
    height: 25px;
    color: white;
}
DisabledButton {
    @extend QPushButton
    background-color: red;
}
```

### Placeholder Selector
```sqss
%error { 
    width: 25px;
    height: 25px;
    color: white;
}
DisabledButton {
    @extend %error
    background-color: red;
}
```

### Import
```sqss
@import "./main.sqss"
```

## Other Resources:
- [VsCode Plugin for PQSS](#)

## Report Bug


## Get Involved

