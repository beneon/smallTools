延续上一个教程：[Building a graph](https://zhuanlan.zhihu.com/p/34428605)，当时一次只使用一个函数，如果要将多个函数叠加在一起的话，还需要多做一些事情。

## 在函数之间切换

上一个教程末尾，我们建立了一个会动的函数图像。除了正弦波以外其实还可以显示其他函数。基本上，只要通过修改position.y = ... 这个表达式就可以显示各种不同的函数。实际上我们甚至可以在游戏运行的同时修改代码，并且让游戏发生相应的改变。

尽管如此，这样还是不大方便，最好就是有一个类似函数库的东西，我们能通过修改某个参数就完成函数的切换。

### 一个函数，一个方法

要让程序支持多种方法的话，首先要对应每个函数写一个方法。为Graph这个类添加下面的方法：

```c#
void SineFunction(){}
```

接下来给这个方法添加参数，就像给函数添加变量x和t，按照之前的程序写一下方法的内容(返回的值是y值，是float)

```c#
float SineFunction(float x, float t){
    return Mathf.Sin(Mathf.PI * (x+t));
}
```

在上一个tutorial中update中的代码基础上做一下修改（原来的代码comment掉）：

```C#
void Update(){
    for (int i=0; i<points.Length; i++){
        Transform point = points[i];
        Vector3 position = point.localPosition;
        // position.y = Mathf.Sin(Mathf.PI * (position.x + Time.time));
        position.y = SineFunction(position.x, Time.time);
        point.localPosition = position;
    }
}
```

因为每次update，Time.time是不会变化的，没必要放在for循环里面，将Time.time提取出来：

```C#
void Update(){
    float t = Time.time;
    for(int i = 0; i< points.Length; i++){
        Transform point = points[i];
        Vector3 position = point.localPostion;
        position.y = SineFunction(position.x,t);
        point.localPosition = position;
    }
}
```

### 第二个函数

现在添加第二个函数。这次添加一个稍微复杂一点的:

```c#
float MultiSineFunction(float x, float t){
    float y = Mathf.Sin(Mathf.PI * (x+t));
    y += Mathf.Sin(2f * Mathf.PI * (x+t))/2f;
    return y;
}
```

这样我们就有了两个正弦函数的叠加，不过现在的函数y值取值范围就变成了-1.5到1.5了，为了保证函数y的取值范围在-1到1之间（毕竟我们shader就是预着这样子的），需要做一个小变换：

```c#
float y = Mathf.Sin(Mathf.PI * (x+t));
y += Mathf.Sin(2f * Mathf.PI * (x+t))/2f;
y *= 2f/3f;
return y;
```

现在把Update里面关于position.y的表达式从SineFunction变成MultiSineFunction:

```C#
position.y = MultiSineFunction(position.x,t);
```