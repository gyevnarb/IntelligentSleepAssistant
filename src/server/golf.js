var a="10001,1101";x=a.split(",");function f(n){if(n<2){return n;}return f(n-1)+f(n-2);}function e(m){i=m.length;r;for(c in m){if(c=='1'){r+=f(i);}i--;return r;}if(e(x[0])==e(x[1])){return('t');}return('f');}
