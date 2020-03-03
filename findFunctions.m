pkg load symbolic

syms x0 x1 x2 x3 u0 u1 u2 u3
more off
function o = mul(q,p)
  o=[p(1) * q(2) + p(2) * q(1) + p(3) * q(4) - p(4) * q(3);
     p(1) * q(3) - p(2) * q(4) + p(3) * q(1) + p(4) * q(2);
     p(1) * q(4) + p(2) * q(3) - p(3) * q(2) + p(4) * q(1);
     p(1) * q(1) - p(2) * q(2) - p(3) * q(3) - p(4) * q(4)]
end
x=[x0;x1;x2;x3];
u=[u0;u1;u2;u3];

f=mul(u,x)
F=jacobian(f,u)
h=x
H=jacobian(h,u)
