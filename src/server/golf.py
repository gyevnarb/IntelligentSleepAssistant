def f(n):
  if n<2:return n
  else:return f(n-1)+f(n-2)
def e(m):
    i,r=0,0
    for c in str(m)[::-1]:
        if c=='1':r+=f(i)
        i+=1
    return r
x,y=input()
z=e(x)==e(y)and't'or'f'
print z
