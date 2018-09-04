X = [-2 -2 -1 0 0 0 1 1 2];
Y = [-2 2 0 -1 1 2 -3 0 1];
Z = [0 0 0 0 1 1 1 1 1];
hold on
xlim([-3,3])
ylim([-3,3])
plot(X(Z==0),Y(Z==0),'rx','linewidth', 3)
plot(X(Z==1),Y(Z==1),'bo','linewidth', 3)
plot(-0.5,-0.75,'gx','linewidth', 3)